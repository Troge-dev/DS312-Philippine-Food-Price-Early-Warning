"""
Data Downloader for DS312 Final Project
Dataset: WFP / Humanitarian Data Exchange (HDX) Philippines Food Prices & Markets
"""
import os
import requests

DATA_URLS = {
    "wfp_food_prices_phl.csv": "https://data.humdata.org/dataset/ea251823-8694-47b4-82d0-7d27f00e8aba/resource/9a842d72-0d7d-4922-ad0e-eb8106c1ab0e/download/wfp_food_prices_phl.csv",
    "wfp_markets_phl.csv": "https://data.humdata.org/dataset/ea251823-8694-47b4-82d0-7d27f00e8aba/resource/a87d0698-ee0b-40c8-96c3-d1ec4616d7bf/download/wfp_markets_phl.csv"
}

def download_data(output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for filename, url in DATA_URLS.items():
        dest = os.path.join(output_dir, filename)
        if os.path.exists(dest):
            size_mb = os.path.getsize(dest) / (1024 * 1024)
            print(f"[EXISTS] {dest} ({size_mb:.2f} MB)")
            continue
            
        print(f"[DOWNLOADING] {filename} from HDX...")
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                f.write(chunk)
                
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"[SAVED] {dest} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    download_data()
