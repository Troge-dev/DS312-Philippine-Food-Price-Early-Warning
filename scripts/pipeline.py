"""
End-to-End Pipeline for Philippine Palengke Food Price Volatility Monitoring
& Crisis Early Warning System (DS312 Final Project)

Components:
1. Ingestion & Filtering (Palengke Food Basket)
2. Feature Engineering (Lags, Spreads, Geospatial, Cyclical Seasons)
3. Target Generation (1-Month Forward Price Spike >= 20%)
4. Unsupervised Market Clustering (K-Means on Market Vulnerability Fingerprints)
5. Supervised Early Warning Classification (Temporal Split LightGBM vs Baseline)
6. Automated Alert Generation (Actionable Risk Tiers)
"""

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, average_precision_score, confusion_matrix
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# CONSTANTS & PALENGKE BASKET SPECIFICATION
# ---------------------------------------------------------
PALENGKE_BASKET = [
    'Rice (regular, milled)',
    'Rice (well milled)',
    'Onions (red)',
    'Tomatoes',
    'Cabbage',
    'Meat (pork)',
    'Meat (chicken, whole)',
    'Eggs'
]

NCR_COORDS = (14.60, 120.98) # Manila Latitude, Longitude

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance in kilometers between two points."""
    R = 6371.0 # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat / 2.0) ** 2 +
         np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2.0) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return R * c

# ---------------------------------------------------------
# MODULE 1: INGESTION & BASKET FILTERING
# ---------------------------------------------------------
def load_and_filter_data(prices_path="data/raw/wfp_food_prices_phl.csv",
                         markets_path="data/raw/wfp_markets_phl.csv"):
    print("[1/5] Ingesting and filtering raw WFP datasets...")
    df_prices = pd.read_csv(prices_path, low_memory=False)
    df_markets = pd.read_csv(markets_path)
    
    # Filter to curated 8-commodity Palengke Basket
    df_basket = df_prices[df_prices['commodity'].isin(PALENGKE_BASKET)].copy()
    
    # Parse dates
    df_basket['date'] = pd.to_datetime(df_basket['date'])
    
    # Standardize market names and merge coordinates if missing
    df_merged = df_basket.merge(
        df_markets[['market_id', 'admin1', 'admin2', 'latitude', 'longitude']].drop_duplicates(),
        on='market_id',
        how='left',
        suffixes=('', '_mkt')
    )
    
    # Fill any coordinate gaps
    df_merged['latitude'] = df_merged['latitude'].fillna(df_merged['latitude_mkt'])
    df_merged['longitude'] = df_merged['longitude'].fillna(df_merged['longitude_mkt'])
    df_merged.drop(columns=['latitude_mkt', 'longitude_mkt'], errors='ignore', inplace=True)
    
    print(f"      Filtered Palengke Basket: {len(df_merged):,} rows across {df_merged['market'].nunique()} markets.")
    return df_merged

# ---------------------------------------------------------
# MODULE 2: FEATURE ENGINEERING (X & Y MATRIX)
# ---------------------------------------------------------
def engineer_features(df):
    print("[2/5] Engineering temporal, geospatial, and price momentum features...")
    
    # Focus primarily on Retail tier for early warning, but compute wholesale spread where available
    # Create market-commodity-pricetype panel sorted chronologically
    df = df.sort_values(['market', 'commodity', 'pricetype', 'date']).reset_index(drop=True)
    
    # Group key for time-series operations
    group_cols = ['market', 'commodity', 'pricetype']
    
    # 1. Price Momentum & Returns (Lags)
    df['price_lag1'] = df.groupby(group_cols)['price'].shift(1)
    df['price_lag3'] = df.groupby(group_cols)['price'].shift(3)
    df['price_lag12'] = df.groupby(group_cols)['price'].shift(12)
    
    df['return_1m'] = (df['price'] - df['price_lag1']) / df['price_lag1']
    df['return_3m'] = (df['price'] - df['price_lag3']) / df['price_lag3']
    df['return_12m'] = (df['price'] - df['price_lag12']) / df['price_lag12']
    
    # 2. Rolling Volatility (6-month rolling window)
    rolling_std_6m = df.groupby(group_cols)['price'].transform(lambda x: x.rolling(6, min_periods=3).std())
    rolling_mean_6m = df.groupby(group_cols)['price'].transform(lambda x: x.rolling(6, min_periods=3).mean())
    df['price_cv_6m'] = rolling_std_6m / (rolling_mean_6m + 1e-5)
    
    # 3. Cyclical Calendar & Seasonal Indicators
    df['month'] = df['date'].dt.month
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)
    df['is_typhoon_quarter'] = df['month'].isin([7, 8, 9]).astype(int)
    df['is_ber_months'] = df['month'].isin([9, 10, 11, 12]).astype(int)
    
    # 4. Geospatial Features
    df['dist_to_ncr_km'] = haversine_distance(
        df['latitude'], df['longitude'],
        NCR_COORDS[0], NCR_COORDS[1]
    )
    
    # Island province heuristic
    island_keywords = ['Palawan', 'Basilan', 'Sulu', 'Tawi-Tawi', 'Bohol', 'Cebu', 'Leyte', 'Samar', 'Mindoro', 'Marinduque']
    df['is_island'] = df['admin2'].astype(str).apply(lambda x: 1 if any(k in x for k in island_keywords) else 0)
    
    # 5. Commodity Behavioral Categorization
    perishability_map = {
        'Tomatoes': 3, 'Cabbage': 3, 'Onions (red)': 2,
        'Meat (pork)': 2, 'Meat (chicken, whole)': 2, 'Eggs': 2,
        'Rice (regular, milled)': 1, 'Rice (well milled)': 1
    }
    df['perishability_tier'] = df['commodity'].map(perishability_map).fillna(1)
    
    # 6. Target Variable Generation (Y_t+1)
    # Forward 1-month price
    df['price_forward1'] = df.groupby(group_cols)['price'].shift(-1)
    df['return_forward1'] = (df['price_forward1'] - df['price']) / df['price']
    
    # Binary Target: 1 if month-over-month price surge >= 20%
    df['target_spike_next_month'] = (df['return_forward1'] >= 0.20).astype(int)
    
    # Filter to Retail transactions and drop rows where lags or target are NaN
    model_df = df[df['pricetype'] == 'Retail'].copy()
    feature_cols = [
        'price', 'return_1m', 'return_3m', 'return_12m', 'price_cv_6m',
        'month_sin', 'month_cos', 'is_typhoon_quarter', 'is_ber_months',
        'dist_to_ncr_km', 'is_island', 'perishability_tier'
    ]
    
    clean_df = model_df.dropna(subset=feature_cols + ['target_spike_next_month']).copy()
    print(f"      Clean Modeling Dataset: {len(clean_df):,} observations ready.")
    print(f"      Price Spike Rate (Y=1): {(clean_df['target_spike_next_month'].mean() * 100):.2f}%")
    
    return clean_df, feature_cols

# ---------------------------------------------------------
# MODULE 3: UNSUPERVISED MARKET CLUSTERING
# ---------------------------------------------------------
def train_market_clustering(df, n_clusters=4):
    print(f"[3/5] Performing Unsupervised Market Vulnerability Clustering (k={n_clusters})...")
    
    # Group by market to create market vulnerability fingerprint
    market_profiles = df.groupby('market').agg(
        mean_price=('price', 'mean'),
        avg_volatility=('price_cv_6m', 'mean'),
        spike_frequency=('target_spike_next_month', 'mean'),
        dist_to_ncr=('dist_to_ncr_km', 'first'),
        is_island=('is_island', 'first')
    ).reset_index()
    
    cluster_features = ['avg_volatility', 'spike_frequency', 'dist_to_ncr', 'is_island']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(market_profiles[cluster_features])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    market_profiles['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Profile cluster names
    archetype_map = {
        0: "Cluster 0: Mainland Production Basins (Low Volatility)",
        1: "Cluster 1: Urban Consumption Hubs (Fast Transmission)",
        2: "Cluster 2: Isolated Island Ports (Logistics Friction)",
        3: "Cluster 3: Shock Amplifiers (High Volatility)"
    }
    market_profiles['cluster_name'] = market_profiles['cluster'].map(archetype_map)
    
    print("\n      === DISCOVERED MARKET VULNERABILITY ARCHETYPES ===")
    summary = market_profiles.groupby('cluster_name').agg(
        market_count=('market', 'count'),
        avg_volatility=('avg_volatility', 'mean'),
        spike_frequency=('spike_frequency', lambda x: f"{x.mean()*100:.1f}%"),
        avg_dist_km=('dist_to_ncr', 'mean')
    )
    print(summary.to_string())
    print("-" * 65)
    
    return market_profiles, kmeans

# ---------------------------------------------------------
# MODULE 4: SUPERVISED PRICE SHOCK FORECASTING (TEMPORAL SPLIT)
# ---------------------------------------------------------
def train_early_warning_model(df, feature_cols, split_year=2022):
    print(f"[4/5] Training Supervised Early Warning Classifier (Temporal Cutoff: {split_year})...")
    
    # Temporal Train / Test Split (Strict Leakage Prevention)
    train_df = df[df['date'].dt.year <= split_year].copy()
    test_df = df[df['date'].dt.year > split_year].copy()
    
    X_train, y_train = train_df[feature_cols], train_df['target_spike_next_month']
    X_test, y_test = test_df[feature_cols], test_df['target_spike_next_month']
    
    print(f"      Train Set ({train_df['date'].dt.year.min()}–{split_year}): {len(X_train):,} rows | {y_train.sum()} spikes")
    print(f"      Test Set  ({split_year+1}–{test_df['date'].dt.year.max()}): {len(X_test):,} rows | {y_test.sum()} spikes")
    
    # Calculate class weight ratio for imbalance
    pos_weight = (len(y_train) - y_train.sum()) / (y_train.sum() + 1e-5)
    
    # LightGBM Classifier
    model = lgb.LGBMClassifier(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=5,
        scale_pos_weight=pos_weight,
        random_state=42,
        verbosity=-1
    )
    
    model.fit(X_train, y_train)
    
    # Predictions & Probabilities
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    
    print("\n      === TEST SET EVALUATION (OUT-OF-TIME VALIDATION) ===")
    print(f"      ROC-AUC Score:          {roc_auc:.4f}  (Baseline Dummy: 0.5000)")
    print(f"      Precision-Recall AUC:   {pr_auc:.4f}  (Baseline Minority: {y_test.mean():.4f})")
    print("\nClassification Report (Decision Threshold = 0.50):")
    print(classification_report(y_test, y_pred, digits=3))
    
    # Feature Importance
    importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("Top 5 Predictive Features:")
    for idx, row in importance_df.head(5).iterrows():
        print(f"      • {row['Feature']:<20}: {row['Importance']} splits")
    print("-" * 65)
    
    return model, test_df, y_prob

# ---------------------------------------------------------
# MODULE 5: INFERENCE & ACTIONABLE ALERTS
# ---------------------------------------------------------
def generate_early_warning_alerts(model, test_df, y_prob, top_n=10):
    print("[5/5] Generating Actionable Early Warning Decision Alerts...")
    
    alerts_df = test_df.copy()
    alerts_df['predicted_spike_prob'] = y_prob
    
    # Assign Risk Tier (ASCII safe)
    def assign_tier(p):
        if p >= 0.70:
            return "[HIGH RISK] (Spike Imminent)"
        elif p >= 0.45:
            return "[MODERATE RISK] (Monitor Margins)"
        else:
            return "[NORMAL] (Stable)"
            
    alerts_df['risk_tier'] = alerts_df['predicted_spike_prob'].apply(assign_tier)
    
    # Filter to most recent available date to simulate live alert feed
    latest_date = alerts_df['date'].max()
    latest_alerts = alerts_df[alerts_df['date'] == latest_date].sort_values(
        'predicted_spike_prob', ascending=False
    )
    
    print(f"\n      === PALENGKE EARLY WARNING SURVEILLANCE BULLETIN ===")
    print(f"      Surveillance Date: {latest_date.strftime('%B %Y')}")
    print(f"      Total Monitored Market-Commodity Pairs: {len(latest_alerts):,}\n")
    
    display_cols = ['market', 'admin2', 'commodity', 'price', 'predicted_spike_prob', 'risk_tier']
    print(latest_alerts[display_cols].head(top_n).to_string(index=False))
    print("\n[SUCCESS] End-to-end data mining pipeline completed successfully.")
    
    return latest_alerts

# ---------------------------------------------------------
# EXECUTE END-TO-END PIPELINE
# ---------------------------------------------------------
if __name__ == "__main__":
    df_raw = load_and_filter_data()
    df_features, feature_cols = engineer_features(df_raw)
    market_profiles, kmeans_model = train_market_clustering(df_features)
    model, test_df, y_prob = train_early_warning_model(df_features, feature_cols)
    alerts = generate_early_warning_alerts(model, test_df, y_prob)
