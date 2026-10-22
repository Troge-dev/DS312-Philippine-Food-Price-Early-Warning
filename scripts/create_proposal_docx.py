import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_proposal():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.different_first_page_header_footer = False
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DS312 Final Project Proposal | Phase 1")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = "Calibri"
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(128, 128, 128)
        # Add page field in word if possible, or plain text
        f_field = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(f_field)

    # Palette
    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy
    COLOR_SECONDARY = RGBColor(46, 91, 136)  # Slate Blue
    COLOR_DARK = RGBColor(38, 38, 38)        # Charcoal Text
    COLOR_MUTED = RGBColor(100, 100, 100)    # Gray
    HEX_PRIMARY = "1B365D"
    HEX_LIGHT_BG = "F4F6F9"
    HEX_ALT_BG = "EBF1F5"
    HEX_BORDER = "CCCCCC"

    # Set normal style font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Document Header / Pre-title
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("DATA MINING AND APPLICATION (DS312) — 1ST SEMESTER A.Y. 2026–2027")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = COLOR_SECONDARY

    p_submeta = doc.add_paragraph()
    p_submeta.paragraph_format.space_after = Pt(18)
    r_sub = p_submeta.add_run("Instructor: Prof. Nicole S. Menorias | Project Window: Oct 12 – Dec 5, 2026")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9)
    r_sub.font.color.rgb = COLOR_MUTED

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Staple Food Price Volatility Monitoring & Crisis Early Warning for Philippine Consumer Markets")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub2 = p_sub.add_run("Phase 1 Project Proposal: Business Problem Definition, Dataset Selection, and Data Mining Plan")
    r_sub2.font.name = "Calibri"
    r_sub2.font.size = Pt(13)
    r_sub2.font.italic = True
    r_sub2.font.color.rgb = COLOR_SECONDARY

    # Team & Metadata Card Table
    t_card = doc.add_table(rows=2, cols=2)
    t_card.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_card.autofit = False
    
    col_widths = [Inches(3.25), Inches(3.25)]
    for row in t_card.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    set_cell_background(t_card.rows[0].cells[0], HEX_LIGHT_BG)
    set_cell_background(t_card.rows[0].cells[1], HEX_LIGHT_BG)
    set_cell_background(t_card.rows[1].cells[0], HEX_LIGHT_BG)
    set_cell_background(t_card.rows[1].cells[1], HEX_LIGHT_BG)
    
    for r in t_card.rows:
        for c in r.cells:
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)

    p1 = t_card.rows[0].cells[0].paragraphs[0]
    p1.add_run("Project Focus: ").bold = True
    p1.add_run("Agricultural Price Spikes & Market Volatility")
    
    p2 = t_card.rows[0].cells[1].paragraphs[0]
    p2.add_run("Target Agency: ").bold = True
    p2.add_run("DA, DTI, NFA, and Provincial LGUs")

    p3 = t_card.rows[1].cells[0].paragraphs[0]
    p3.add_run("Primary Dataset: ").bold = True
    p3.add_run("WFP / HDX Philippines Food Prices (238,623 rows)")

    p4 = t_card.rows[1].cells[1].paragraphs[0]
    p4.add_run("Target Complexity Tier: ").bold = True
    p4.add_run("Advanced (7–8 Points)")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Helper function for headings
    def add_custom_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.bold = True
        if level == 1:
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            run.font.size = Pt(15)
            run.font.color.rgb = COLOR_PRIMARY
            # Add bottom accent line
        elif level == 2:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run.font.size = Pt(12.5)
            run.font.color.rgb = COLOR_SECONDARY
        elif level == 3:
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_DARK
        return p

    # 1. Executive Summary
    add_custom_heading("1. Executive Summary", 1)
    doc.add_paragraph(
        "Food security and commodity price stability are central to the socioeconomic welfare of the Philippines. "
        "Staple foods—particularly rice, vegetables (such as onions and tomatoes), pork, poultry, and fish—represent "
        "a disproportionately high share of the consumption basket for low- and middle-income Filipino households. "
        "Historical crises, including the 2018 national rice shortage and the 2022–2023 onion price surge (where retail "
        "prices breached ₱1,000/kg), highlight critical vulnerabilities in the domestic supply chain: extreme geographic price "
        "disparities, speculative hoarding, severe middleman markups, and delayed policy interventions."
    )
    doc.add_paragraph(
        "This project proposes an end-to-end data mining initiative using the United Nations World Food Programme (WFP) "
        "Food Prices database for the Philippines, hosted on the Humanitarian Data Exchange (HDX). Spanning over 26 years "
        "(January 2000 to August 2026) and comprising 238,623 transaction records across 17 administrative regions, 79 provinces, "
        "and 108 major wet markets, this dataset provides empirical granularity across 73 agricultural commodities. "
        "By integrating market geographic data and applying both unsupervised spatial-temporal clustering (to isolate market "
        "vulnerability archetypes) and supervised classification/regression (to forecast localized price shocks 30–60 days in advance), "
        "our team aims to equip regulatory bodies (DA, DTI, NFA) with an actionable, data-driven early warning system."
    )

    # 2. Problem Statement and Business Context
    add_custom_heading("2. Problem Statement and Business Context", 1)
    doc.add_paragraph(
        "In the Philippines, agricultural commodity price monitoring has historically relied on post-hoc reporting through "
        "periodic Philippine Statistics Authority (PSA) bulletins and manual market price boards overseen by the Department of "
        "Agriculture (DA) Agribusiness and Marketing Assistance Service (AMAS). While informative, these conventional methods "
        "are inherently reactive: regulatory actions—such as imposing Suggested Retail Prices (SRPs), releasing buffer stocks "
        "via the National Food Authority (NFA), or authorizing emergency tariff cuts under Republic Act 11203 (Rice Tariffication Law)—"
        "are typically deployed weeks or months after consumer price shocks have already inflicted severe financial damage."
    )
    doc.add_paragraph(
        "Furthermore, the archipelago's unique geography introduces severe inter-island logistics friction. A price shock "
        "originating from typhoon damage in Central Luzon (the country's 'rice granary') propagates unevenly across island provinces "
        "(such as Palawan, Mindoro, and the Bangsamoro region). Retail markups compared to farm gate prices often reflect middleman "
        "inefficiencies rather than genuine production shortages. Regulators lack an analytical framework that can simultaneously:"
    )
    
    bullets = [
        ("Segment and rank regional wet markets ", "based on structural price volatility, geographic isolation, and exposure to supply chain shocks."),
        ("Provide early warning alerts ", "for impending price spikes at least 1–2 months prior to peak inflation, giving policymakers lead time to manage imports and release strategic reserves."),
        ("Distinguish normal seasonal fluctuations ", "from artificial price gouging or systemic supply-chain failures.")
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = COLOR_PRIMARY
        bp.add_run(b_desc)

    # 3. Business Problem Canvas
    add_custom_heading("3. Business Problem Canvas", 1)
    doc.add_paragraph(
        "In accordance with Section 3 of the DS312 Project Guide, the proposed initiative is structured across the seven "
        "dimensions of the Business Problem Canvas below:"
    )

    canvas_table = doc.add_table(rows=8, cols=2)
    canvas_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    canvas_table.autofit = False
    
    c_widths = [Inches(2.2), Inches(4.3)]
    for row in canvas_table.rows:
        for idx, w in enumerate(c_widths):
            row.cells[idx].width = w

    canvas_data = [
        ("Canvas Dimension", "Group Definition & Scope"),
        ("Context / Organization", 
         "Department of Agriculture (DA), Department of Trade and Industry (DTI - Fair Trade Group), "
         "National Food Authority (NFA), and Provincial / Municipal Price Coordinating Councils (LPCCs)."),
        ("Problem Statement", 
         "Agricultural price monitoring in the Philippines is predominantly retrospective. Regulators lack automated, "
         "forward-looking tools to identify which markets are high-risk price amplifiers and to anticipate staple food "
         "price spikes before they severely reduce household purchasing power."),
        ("Stakeholders", 
         "1. Policy Makers (DA/DTI): Set Suggested Retail Prices (SRP), import quotas, and tariff interventions.\n"
         "2. Market Administrators & LGUs: Direct local market inspections and investigate hoarding.\n"
         "3. Farmers & Consumer Advocacy Groups: Utilize transparent fair-price thresholds to prevent exploitation."),
        ("Business Questions\n(Core Questions Answerable by Data)", 
         "1. Market Vulnerability Archetypes: Which Philippine wet markets act as 'price leaders' (shock originators) versus 'price followers' (lagged shock absorbers)?\n"
         "2. Price Spike Prediction: Can we predict whether a staple commodity (e.g., well-milled rice, red onions) in a given province will experience a critical price shock (>20% monthly increase or >2σ volatility) 30–60 days ahead?\n"
         "3. Value-Chain Friction: How does the spread between Farm Gate, Wholesale, and Retail prices vary across regions and commodity categories?\n"
         "4. Climate & Temporal Seasonality: What seasonal patterns and typhoon-quarter markers systematically precede sustained price surges?"),
        ("Success Criteria", 
         "1. Unsupervised Clustering: Produce 3–5 distinct, statistically separated market risk profiles (Silhouette Score ≥ 0.45) with intuitive geographic and operational interpretations.\n"
         "2. Supervised Prediction: Achieve an AUC-ROC ≥ 0.80 and Precision-Recall AUC significantly outperforming baseline (>0.40 over a ~10% rare-event baseline) on 30-day price spike early warning.\n"
         "3. Operational Usability: Synthesize findings into actionable policy recommendations and a visual risk-monitoring prototype."),
        ("Task Types\n(Data Mining & ML Families)", 
         "Two Distinct Technique Families:\n"
         "• Technique Family 1 (Unsupervised Learning): Time-Series / Spatial-Temporal Market Clustering (K-Means / Agglomerative Clustering / DBSCAN).\n"
         "• Technique Family 2 (Supervised Learning): Cost-Sensitive Binary Classification & Gradient Boosted Regression (Logistic Regression Baseline vs. Random Forest & LightGBM/XGBoost)."),
        ("Risks and Limitations", 
         "• Data Reporting Gaps: Certain provincial wet markets have irregular historical collection intervals.\n"
         "• Exogenous Factors: Typhoon tracks, global crude oil prices, and fertilizer subsidies are not fully captured within the raw table and must be proxied via temporal lags.\n"
         "• Currency & Inflation Drifts: Spanning 26 years requires real price deflation (CPI base adjustment) or rolling relative ratios to prevent historical nominal distortion.")
    ]

    for r_idx, (dim, val) in enumerate(canvas_data):
        row = canvas_table.rows[r_idx]
        cell_dim = row.cells[0]
        cell_val = row.cells[1]
        
        p_dim = cell_dim.paragraphs[0]
        p_val = cell_val.paragraphs[0]
        
        p_dim.add_run(dim)
        p_val.add_run(val)
        
        set_cell_margins(cell_dim, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cell_val, top=80, bottom=80, left=120, right=120)
        
        if r_idx == 0:
            set_cell_background(cell_dim, HEX_PRIMARY)
            set_cell_background(cell_val, HEX_PRIMARY)
            p_dim.runs[0].font.bold = True
            p_dim.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            p_val.runs[0].font.bold = True
            p_val.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            p_dim.runs[0].font.bold = True
            p_dim.runs[0].font.color.rgb = COLOR_PRIMARY
            bg = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell_dim, bg)
            set_cell_background(cell_val, bg)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4. Evaluation of Candidate Datasets
    add_custom_heading("4. Evaluation of Candidate Datasets (Phase 1 Selection)", 1)
    doc.add_paragraph(
        "To ensure compliance with the DS312 Final Project rubric, the team brainstormed and evaluated three distinct "
        "candidate datasets from established open data portals. As required, standard overused teaching datasets "
        "(Titanic, Iris, Boston Housing, Wine, MNIST) were strictly excluded. Below is the multi-criteria evaluation matrix:"
    )

    eval_table = doc.add_table(rows=6, cols=4)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_table.autofit = False
    
    e_widths = [Inches(1.8), Inches(1.6), Inches(1.6), Inches(1.5)]
    for row in eval_table.rows:
        for idx, w in enumerate(e_widths):
            row.cells[idx].width = w

    eval_headers = ["Selection Criterion", "Candidate 1 (Selected):\nWFP Philippine Food Prices", "Candidate 2 (Alternative A):\nHotel Booking Demand", "Candidate 3 (Alternative B):\nOpenAQ Metro Manila Air Quality"]
    for c_idx, h_text in enumerate(eval_headers):
        cell = eval_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.add_run(h_text)
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    eval_rows = [
        ("Public Source & Volume", 
         "WFP / HDX (Direct CSV)\n238,623 rows × 16 cols (Primary)\n132 rows × 7 cols (Markets)",
         "Kaggle / ScienceDirect\n119,390 rows × 32 cols\nSingle table",
         "OpenAQ API / Kaggle\n~80,000 hourly rows × 14 cols\nTime-series sensor feeds"),
        ("Authentic Messiness & Imperfections", 
         "High: Commodity labeling variations, multi-tier price types (Farm/Wholesale/Retail), price shocks (onion crisis ₱1,200/kg), irregular reporting cadences.",
         "Moderate: Negative ADR outliers (-$6.38), phantom bookings (0 guests), missing company (94%), agent IDs.",
         "High: Negative sensor readings, stuck instrument plateaus (72h flatlines), unit conversions (ppm vs µg/m³)."),
        ("Two Data Mining Families Fit", 
         "Excellent:\n1. Unsupervised: Market Volatility & Geographic Clustering\n2. Supervised: Price Shock Prediction & Lagged Forecasting",
         "Excellent:\n1. Unsupervised: Guest Persona RFM Clustering\n2. Supervised: Cancellation Risk Prediction",
         "Good:\n1. Unsupervised: Sensor Anomaly Detection\n2. Supervised: Next-day PM2.5 Regression"),
        ("Local Philippine Policy Impact", 
         "Maximum (10/10): Directly addresses national food security, inflation, and agricultural protection (DA/DTI/NFA).",
         "Moderate (5/10): Generalized international hospitality operations (Portugal hotel chains).",
         "High (9/10): Metro Manila urban environmental health and DENR clean air compliance."),
        ("Verdict & Recommendation", 
         "SELECTED PRIMARY:\nHits 8/8 Advanced Complexity Tier, high societal relevance, robust 26-year longitudinal scale.",
         "Documented Alternative 1:\nExcellent technical fallback; pristine single CSV structure.",
         "Documented Alternative 2:\nHigh environmental value; requires heavier sensor-cleaning logic.")
    ]

    for r_idx, r_data in enumerate(eval_rows, start=1):
        for c_idx, text in enumerate(r_data):
            cell = eval_table.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            p.add_run(text)
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_PRIMARY
            bg = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 5. Dataset Description & Data Dictionary
    add_custom_heading("5. Dataset Description & Data Dictionary", 1)
    doc.add_paragraph(
        "The primary data asset for this study is the official United Nations World Food Programme (WFP) Vulnerability "
        "Analysis and Mapping (VAM) database for the Philippines, distributed via the Humanitarian Data Exchange (HDX). "
        "The collection consists of two relational CSV files:"
    )

    p_f1 = doc.add_paragraph(style='List Bullet')
    p_f1.add_run("wfp_food_prices_phl.csv: ").bold = True
    p_f1.add_run("Main longitudinal transactional table containing 238,623 observations, 16 features, spanning January 15, 2000 to August 15, 2026. File size: 31.34 MB.")

    p_f2 = doc.add_paragraph(style='List Bullet')
    p_f2.add_run("wfp_markets_phl.csv: ").bold = True
    p_f2.add_run("Market metadata table containing 132 unique monitored wet markets, their administrative hierarchical linkage (Admin 1, Admin 2), and verified geospatial coordinates (latitude, longitude). File size: 0.01 MB.")

    doc.add_paragraph(
        "The dataset is published under the Creative Commons Attribution 4.0 International (CC-BY 4.0) license, "
        "permitting academic and non-commercial analytical use. Below is the comprehensive Data Dictionary:"
    )

    dict_table = doc.add_table(rows=17, cols=5)
    dict_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dict_table.autofit = False
    
    d_widths = [Inches(1.5), Inches(1.0), Inches(1.1), Inches(1.0), Inches(1.9)]
    for row in dict_table.rows:
        for idx, w in enumerate(d_widths):
            row.cells[idx].width = w

    dict_headers = ["Attribute Name", "Storage Type", "Domain / Values", "Missing %", "Operational Description"]
    for c_idx, h_text in enumerate(dict_headers):
        cell = dict_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.add_run(h_text)
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    dict_data = [
        ("date", "String (Date)", "2000-01-15 to 2026-08-15", "0.0%", "Date of monthly price capture (mid-month standardized)."),
        ("admin1", "String (Categorical)", "17 Regions", "0.0%", "First-level administrative region (e.g., NCR, Central Luzon, ARMM)."),
        ("admin2", "String (Categorical)", "79 Provinces", "0.0%", "Second-level administrative province (e.g., Nueva Ecija, Cebu, Davao)."),
        ("market", "String (Categorical)", "108 Market Names", "0.0%", "Specific wet market, trading post, or municipal monitoring hub."),
        ("market_id", "Integer (Key)", "167 to 3450", "0.0%", "Unique relational identifier for the physical market entity."),
        ("latitude", "Float (Geospatial)", "4.82° to 18.57° N", "0.0%", "Geographic latitude coordinate of the monitored market."),
        ("longitude", "Float (Geospatial)", "119.98° to 126.04° E", "0.0%", "Geographic longitude coordinate of the monitored market."),
        ("category", "String (Categorical)", "6 Macro Categories", "0.0%", "Macro food category (Vegetables/fruits, Meat/fish/eggs, Cereals/tubers)."),
        ("commodity", "String (Categorical)", "73 Specific Items", "0.0%", "Specific agricultural commodity name (e.g., 'Rice (regular, milled)')."),
        ("commodity_id", "Integer (Key)", "Unique IDs", "0.0%", "Standardized WFP commodity taxonomy code."),
        ("unit", "String (Categorical)", "KG, Unit, 750 ML", "0.0%", "Measurement packaging unit for the observed price."),
        ("priceflag", "String (Categorical)", "actual, aggregate", "0.0%", "Indicates whether price is directly surveyed or spatially aggregated."),
        ("pricetype", "String (Categorical)", "Retail, Wholesale, Farm Gate", "0.0%", "Supply chain tier (Retail = 231k, Wholesale = 6k, Farm Gate = 664)."),
        ("currency", "String (Categorical)", "PHP", "0.0%", "Monetary currency unit (Philippine Peso throughout)."),
        ("price", "Float (Continuous)", "₱1.60 to ₱1,216.67", "0.0%", "Observed commodity price in Philippine Pesos."),
        ("usdprice", "Float (Continuous)", "$0.03 to $22.12", "0.0%", "Exchange-rate adjusted price in United States Dollars.")
    ]

    for r_idx, r_data in enumerate(dict_data, start=1):
        for c_idx, text in enumerate(r_data):
            cell = dict_table.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            p.add_run(text)
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_PRIMARY
            bg = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 6. Dataset Complexity Statement (Scoring Tier Defense)
    add_custom_heading("6. Dataset Complexity Statement (Scoring Tier: Advanced, 7–8/8 Points)", 1)
    doc.add_paragraph(
        "In compliance with Section 3 of the project guide, our group formally justifies positioning this project "
        "within the 'Advanced' Dataset Quality and Complexity Tier (7–8 points). The complexity of this dataset is genuine, "
        "organic to public-sector food monitoring systems, and requires rigorous, multi-faceted preprocessing:"
    )

    c_points = [
        ("Multi-Source & Relational Integration: ", 
         "The project requires joining the 238,623-row transactional price stream with the market geographic metadata table "
         "using market_id as the primary key. In Phase 2, we will validate key alignment, eliminate boundary discrepancies, and "
         "engineer spatial distance matrices (e.g., straight-line and road-network distance from each provincial wet market to "
         "the National Capital Region consumption core)."),
        ("Longitudinal Scale & High Dimensionality: ", 
         "Spanning 319 consecutive monthly periods (2000–2026) across 108 markets and 73 commodities, the data forms an "
         "unbalanced three-dimensional panel: Market × Commodity × Time. Handling this requires sophisticated panel-data transformations, "
         "rolling lag constructions (1-month, 3-month, 12-month returns), and time-series feature decomposition."),
        ("Categorical Granularity & Taxonomy Harmonization: ", 
         "The dataset records 6 distinct commodity variations for rice alone: 'Rice (regular, milled)', 'Rice (well milled)', "
         "'Rice (milled, superior)', 'Rice (premium)', 'Rice (special)', and 'Rice (paddy)'. Developing a domain-grounded commodity "
         "crosswalk (aligning with DA/PSA standards) is an essential, high-order data curation task that prevents fragmented modeling."),
        ("Mixed Supply Chain Tiers & Unit Discrepancies: ", 
         "The dataset captures prices across three distinct supply-chain tiers: Retail (231,877 records), Wholesale (6,082 records), "
         "and Farm Gate (664 records), with varying units ('KG', 'Unit', '750 ML'). Reconciling these tiers to analyze middleman margins "
         "requires group-level index standardization."),
        ("Genuine Real-World Outliers & Extreme Volatility: ", 
         "The price distribution spans from ₱1.60 to ₱1,216.67 (mean = ₱131.98, std = ₱119.67). Extreme observations—such as the "
         "2022–2023 onion crisis where Red Onion prices spiked from ₱80/kg to over ₱1,000/kg—represent vital macroeconomic signals rather "
         "than clerical measurement errors. In Phase 2, our outlier treatment will distinguish authentic crisis shocks from erroneous data entry.")
    ]

    for p_title, p_desc in c_points:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(p_title)
        r.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        p.add_run(p_desc)

    # 7. Preliminary Data Mining Plan
    add_custom_heading("7. Preliminary Data Mining Plan", 1)
    doc.add_paragraph(
        "To satisfy the Phase 1 rubric requirement of naming at least two distinct data mining technique families, "
        "our analytical framework combines Unsupervised Discovery with Supervised Predictive Modeling:"
    )

    add_custom_heading("7.1 Technique Family 1: Unsupervised Spatial-Temporal Clustering", 2)
    doc.add_paragraph(
        "• Algorithm Family: K-Means Clustering, Hierarchical Agglomerative Clustering (with Ward's linkage), and DBSCAN.\n"
        "• Purpose & Justification: Provincial wet markets do not respond to national macroeconomic shocks uniformly. By summarizing "
        "each market across engineered volatility indicators (rolling standard deviation of price changes, average retail-to-wholesale markup, "
        "frequency of extreme price spikes, and distance to agricultural supply hubs), clustering algorithms will segment Philippine markets "
        "into 3–5 behavioral archetypes (e.g., 'Volatile Island Importers', 'Stable Agricultural Granaries', 'Metro Manila Demand Centers').\n"
        "• Validation & Evaluation: Silhouette Analysis, Davies-Bouldin Index, and qualitative validation with regional DA trade profiles."
    )

    add_custom_heading("7.2 Technique Family 2: Supervised Classification & Early Warning Modeling", 2)
    doc.add_paragraph(
        "• Algorithm Family: Cost-Sensitive Logistic Regression (Baseline) vs. Random Forest Classifier and Gradient Boosted Trees (LightGBM / XGBoost).\n"
        "• Target Variable Definition: Binary price shock indicator (Price_Shock_t+1 = 1 if Month-over-Month price increase ≥ 20% or exceeds 2 historical standard deviations; 0 otherwise).\n"
        "• Leakage Prevention Strategy: Standard random k-fold cross-validation is strictly invalid for time-series panel data because future prices would leak into historical training sets. We will enforce an expanding-window temporal cross-validation (TimeSeriesSplit): training on 2000–2021, tuning on 2022–2023, and blind out-of-time testing on 2024–2026.\n"
        "• Evaluation Metrics: Precision, Recall (critical because failing to predict a rice crisis has high societal cost), Area Under the Precision-Recall Curve (PR-AUC), and Brier Score."
    )

    # 8. Preview of Phase 3 EDA & Statistical Hypothesis Testing
    add_custom_heading("8. Preview of Phase 3 EDA & Statistical Hypotheses", 1)
    doc.add_paragraph(
        "The dataset provides natural foundations for the mandatory Phase 3 statistical hypothesis tests (Page 5 of guide):"
    )

    h1 = doc.add_paragraph(style='List Bullet')
    h1.add_run("Hypothesis 1 (Two-Sample Welch's t-test / Mann-Whitney U): ").bold = True
    h1.add_run("H0: The mean monthly price volatility (coefficient of variation) of staple rice in island provinces (e.g., Palawan, Basilan, Sulu) is equal to that of mainland agricultural provinces (e.g., Nueva Ecija, Isabela). Ha: Island provinces experience significantly higher rice price volatility due to maritime logistics friction (α = 0.05).")

    h2 = doc.add_paragraph(style='List Bullet')
    h2.add_run("Hypothesis 2 (One-Way ANOVA / Kruskal-Wallis Test): ").bold = True
    h2.add_run("H0: The percentage spread between wholesale and retail prices is invariant across major commodity categories (Cereals, Vegetables, Meat). Ha: Perishable vegetables exhibit a significantly higher retail markup spread than staple cereals (α = 0.05).")

    # 9. Project Timeline & Work Breakdown Structure
    add_custom_heading("9. Project Execution Timeline & Milestones", 1)
    doc.add_paragraph(
        "The team's execution schedule strictly tracks the DS312 Project Guide milestones across all five phases:"
    )

    time_table = doc.add_table(rows=6, cols=4)
    time_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    time_table.autofit = False
    
    t_widths = [Inches(1.2), Inches(2.2), Inches(1.5), Inches(1.6)]
    for row in time_table.rows:
        for idx, w in enumerate(t_widths):
            row.cells[idx].width = w

    t_headers = ["Phase", "Core Focus & Key Tasks", "Course Dates", "Submission Deadline"]
    for c_idx, h_text in enumerate(t_headers):
        cell = time_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.add_run(h_text)
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

    timeline_data = [
        ("Phase 1", "Dataset Selection, Business Problem Canvas, Data Dictionary, Candidate Comparison, Initial Ingestion", "Oct 12 – Oct 24", "Sun, Oct 25, 2026\n(Reports: Oct 28)"),
        ("Phase 2", "Data Profiling, Missing Value Treatment, Outlier Resolution, Relational Joins, Preprocessing Log, Processed CSV", "Oct 26 – Nov 7", "Sun, Nov 8, 2026\n(Reports: Nov 11)"),
        ("Phase 3", "Exploratory Data Analysis, 8+ Purposeful Visualizations, 2 Hypothesis Tests (t-test, ANOVA), Modeling Implications", "Nov 9 – Nov 14", "Sun, Nov 15, 2026\n(Reports: Nov 18)"),
        ("Phase 4", "Model Training (Clustering + Classification), Baseline Comparison, Hyperparameter Tuning, Business Interpretation", "Nov 16 – Nov 28", "Sun, Nov 29, 2026\n(Reports: Dec 2)"),
        ("Phase 5", "Master Jupyter Notebook, A1 Project Poster, 12-Slide PowerPoint Presentation, Final Project Defense", "Nov 30 – Dec 5", "Per Class Schedule\n(Dec 1–5, 2026)")
    ]

    for r_idx, r_data in enumerate(timeline_data, start=1):
        for c_idx, text in enumerate(r_data):
            cell = time_table.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            p.add_run(text)
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = COLOR_PRIMARY
            bg = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 10. Individual Narrative Report Strategy (Rubric Protection)
    add_custom_heading("10. Individual Contribution & Accountability Strategy", 1)
    doc.add_paragraph(
        "To guarantee that each group member achieves the maximum 20/20 on the individual narrative reports (Section 8.1 of guide), "
        "the team will operate under a transparent Git-based workflow with distinct task assignments per phase:"
    )

    roles = [
        ("Data Engineering & Preprocessing Lead: ", "Maintains the data pipeline, relational joins between price and market tables, and the comprehensive Preprocessing Log."),
        ("Exploratory Analysis & Visualization Specialist: ", "Implements statistical hypothesis testing (Welch's t-test, ANOVA), generates the 8+ interpreted visualizations, and builds geospatial maps."),
        ("Machine Learning & Modeling Lead: ", "Architects the time-series cross-validation splits, builds the baseline models, tunes Gradient Boosted Trees and K-Means clusters, and evaluates performance metrics."),
        ("Business Translation & Quality Assurance Lead: ", "Ensures zero data leakage, aligns model outputs with practical DA/DTI policy mechanisms, and drafts executive narrative summaries.")
    ]
    for r_title, r_desc in roles:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(r_title)
        r.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        p.add_run(r_desc)

    doc.add_paragraph(
        "Every phase submission will be cross-referenced with individual Git commit hashes and Jupyter cell annotations "
        "to ensure 100% concordance with submitted narrative reports."
    )

    # Save document
    output_path = "reports/DS312_Phase1_Project_Proposal_Food_Security.docx"
    doc.save(output_path)
    print(f"Successfully generated proposal: {output_path}")

if __name__ == "__main__":
    create_proposal()
