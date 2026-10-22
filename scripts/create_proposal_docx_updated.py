import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_times_black_proposal():
    doc = docx.Document()
    
    # Page setup - 1 inch margins all sides
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.different_first_page_header_footer = False
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DS312 Final Project Proposal | Phase 1: Food Security")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(9)
        hrun.font.color.rgb = RGBColor(0, 0, 0)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(10)
        frun.font.color.rgb = RGBColor(0, 0, 0)
        f_field = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(f_field)

    COLOR_BLACK = RGBColor(0, 0, 0)
    HEX_HEADER_BG = "EAEAEA"
    HEX_ALT_BG = "F7F7F7"

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = COLOR_BLACK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    def add_para(text="", style='Normal', bold=False, italic=False, size=Pt(12), space_before=Pt(0), space_after=Pt(6), align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph(style=style)
        p.alignment = align
        p.paragraph_format.space_before = space_before
        p.paragraph_format.space_after = space_after
        p.paragraph_format.line_spacing = 1.15
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = size
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = COLOR_BLACK
        return p

    def add_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK
        if level == 1:
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            r.font.size = Pt(15)
        elif level == 2:
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            r.font.size = Pt(13)
        elif level == 3:
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            r.font.size = Pt(12)
            r.font.italic = True
        return p

    # Document Header / Course Information
    add_para("DATA MINING AND APPLICATION (DS312) — 1ST SEMESTER A.Y. 2026–2027", bold=True, size=Pt(10), space_after=Pt(2))
    add_para("Instructor: Prof. Nicole S. Menorias | Project Window: October 12 – December 5, 2026", size=Pt(10), italic=True, space_after=Pt(14))

    # Title & Subtitle
    add_para("Staple Food Price Volatility Monitoring & Crisis Early Warning for Philippine Consumer Markets", bold=True, size=Pt(18), space_after=Pt(4))
    add_para("Phase 1 Final Project Proposal: Business Problem Definition, Dataset Selection, and Data Mining Plan", italic=True, size=Pt(12), space_after=Pt(12))

    # Project Information Card Table
    card_table = doc.add_table(rows=2, cols=2)
    card_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    card_table.autofit = False
    set_table_borders(card_table, color="B0B0B0", sz="6")
    
    col_widths = [Inches(3.25), Inches(3.25)]
    for row in card_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    for r in card_table.rows:
        for c in r.cells:
            set_cell_background(c, HEX_ALT_BG)
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    p1 = card_table.rows[0].cells[0].paragraphs[0]
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run("Project Focus: ")
    r1.font.name = "Times New Roman"
    r1.font.bold = True
    r1.font.color.rgb = COLOR_BLACK
    r1_b = p1.add_run("Palengke Food Basket Price Shock Forecasting")
    r1_b.font.name = "Times New Roman"
    r1_b.font.color.rgb = COLOR_BLACK

    p2 = card_table.rows[0].cells[1].paragraphs[0]
    p2.paragraph_format.space_after = Pt(2)
    r2 = p2.add_run("Target Regulatory Stakeholders: ")
    r2.font.name = "Times New Roman"
    r2.font.bold = True
    r2.font.color.rgb = COLOR_BLACK
    r2_b = p2.add_run("DA, DTI, NFA, and Provincial LGUs")
    r2_b.font.name = "Times New Roman"
    r2_b.font.color.rgb = COLOR_BLACK

    p3 = card_table.rows[1].cells[0].paragraphs[0]
    p3.paragraph_format.space_after = Pt(2)
    r3 = p3.add_run("Primary Data Asset: ")
    r3.font.name = "Times New Roman"
    r3.font.bold = True
    r3.font.color.rgb = COLOR_BLACK
    r3_b = p3.add_run("UN WFP / HDX Philippine Food Prices (238,623 rows)")
    r3_b.font.name = "Times New Roman"
    r3_b.font.color.rgb = COLOR_BLACK

    p4 = card_table.rows[1].cells[1].paragraphs[0]
    p4.paragraph_format.space_after = Pt(2)
    r4 = p4.add_run("Target Complexity Tier: ")
    r4.font.name = "Times New Roman"
    r4.font.bold = True
    r4.font.color.rgb = COLOR_BLACK
    r4_b = p4.add_run("Advanced (7–8 Points)")
    r4_b.font.name = "Times New Roman"
    r4_b.font.color.rgb = COLOR_BLACK

    add_para("", space_after=Pt(8))

    # 1. Executive Summary
    add_heading("1. Executive Summary", 1)
    add_para(
        "Food security, price stability, and fair supply-chain margins are paramount to Philippine national welfare. "
        "Staple foods—specifically rice, highland vegetables (onions, cabbage, tomatoes), and fresh animal proteins (pork, poultry, eggs)—"
        "command the largest single share of the consumer expenditure basket among low- and middle-income Filipino families. "
        "Macroeconomic disruptions, such as the 2018 national rice crisis, post-typhoon vegetable inflation in Benguet, African Swine Fever (ASF) "
        "shocks in the livestock corridor, and the 2022–2023 onion crisis (where retail prices exceeded ₱1,000/kg), demonstrate that "
        "agricultural price spikes create immediate, severe welfare losses."
    )
    add_para(
        "This project establishes a proactive data mining system leveraging the official United Nations World Food Programme (WFP) "
        "Food Prices database for the Philippines, distributed via the Humanitarian Data Exchange (HDX). Spanning over 26 years "
        "(January 2000 to August 2026) and encompassing 238,623 observations across 108 wet markets in 79 provinces, the data tracks 73 commodities "
        "at Farm Gate, Wholesale, and Retail levels. Rather than relying on traditional retrospective econometrics, our team applies "
        "Unsupervised Spatial-Temporal Clustering (to profile market vulnerability archetypes) and Supervised Gradient-Boosted Classification "
        "(to forecast localized price shocks 30–60 days in advance), delivering an actionable early-warning decision instrument for the "
        "Department of Agriculture (DA) and the Department of Trade and Industry (DTI)."
    )

    # 2. Problem Statement & Context
    add_heading("2. Problem Statement & Policy Context", 1)
    add_para(
        "Agricultural commodity monitoring in the Philippines has historically been retrospective. Official surveillance conducted by the "
        "Philippine Statistics Authority (PSA) and the Department of Agriculture Agribusiness and Marketing Assistance Service (AMAS) relies "
        "primarily on manual price enumerations, localized market boards, and backward-looking price bulletins. Consequently, policy interventions—"
        "such as mandating Suggested Retail Prices (SRP), authorizing emergency National Food Authority (NFA) buffer stock releases, or adjusting "
        "import tariff rates under Republic Act 11203 (Rice Tariffication Law)—are typically implemented weeks or months after consumer purchasing "
        "power has already been eroded."
    )
    add_para(
        "Moreover, the archipelagic geography of the Philippines creates severe inter-island logistics bottlenecks. A production shock in an agricultural "
        "basin like Central Luzon or Cagayan Valley transmits unequally across maritime transport routes to island provinces such as Palawan, Mindoro, "
        "and the Bangsamoro Autonomous Region in Muslim Mindanao (BARMM). Regulatory agencies currently lack an automated system that can:"
    )

    bullets = [
        ("Identify and cluster market vulnerability archetypes: ", "Distinguishing between regional price leaders (where price shocks originate) and price followers (island or deficit hubs that absorb shocks with a lag)."),
        ("Provide forward-looking early warnings: ", "Detecting early momentum in monthly price trajectories to forecast impending price surges (>20% month-over-month increase) at least 30 to 60 days ahead."),
        ("Monitor middleman margin expansion: ", "Quantifying the marketing spread between Farm Gate, Wholesale, and Retail tiers to isolate artificial price gouging from legitimate transport and production cost increases.")
    ]
    for b_title, b_desc in bullets:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(b_title)
        r_t.font.name = "Times New Roman"
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_BLACK
        r_d = p.add_run(b_desc)
        r_d.font.name = "Times New Roman"
        r_d.font.color.rgb = COLOR_BLACK

    # 3. Methodological Contrast with Existing Literature
    add_heading("3. Methodological Contrast with Existing Literature", 1)
    add_para(
        "A critical distinction must be drawn between this project and existing academic and policy literature. While our work is grounded in the "
        "economic frameworks established by institutions such as the Philippine Institute for Development Studies (PIDS, e.g., Dr. Roehlano Briones) "
        "and the University of the Philippines Los Baños (UPLB Department of Agricultural Economics), our methodology directly contrasts with "
        "traditional approaches in four key areas:"
    )

    contrast_table = doc.add_table(rows=5, cols=3)
    contrast_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    contrast_table.autofit = False
    set_table_borders(contrast_table, color="B0B0B0", sz="4")

    c_widths = [Inches(1.8), Inches(2.4), Inches(2.4)]
    for row in contrast_table.rows:
        for idx, w in enumerate(c_widths):
            row.cells[idx].width = w

    headers_contrast = ["Analytical Dimension", "Traditional Studies (PIDS, UPLB, DA)", "Proposed DS312 Data Mining Project"]
    for c_idx, h_text in enumerate(headers_contrast):
        cell = contrast_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.bold = True
        r.font.color.rgb = COLOR_BLACK
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    contrast_data = [
        ("Analytical Horizon", 
         "Retrospective & Explanatory: Uses cointegration, Granger causality, and Vector Error Correction Models (VECM) to explain why past crises happened.",
         "Forward-Looking & Predictive: Formulates price shock detection as an out-of-time early-warning prediction task 30–60 days ahead."),
        ("Commodity Scope", 
         "Single-Commodity Focus: Over 85% of domestic studies focus exclusively on rice (paddy vs. milled), omitting perishables and protein.",
         "Integrated Palengke Basket: Evaluates an 8-commodity basket spanning durable grains, volatile highland vegetables, and core animal proteins."),
        ("Functional Modeling", 
         "Linear Econometric Assumptions: Assumes linear price transmission, which breaks down during acute supply shocks and policy shifts.",
         "Non-Linear Machine Learning: Applies Gradient Boosted Decision Trees (LightGBM/XGBoost) and Random Forests to model non-linear shock thresholds."),
        ("Regional Segmentation", 
         "Pre-Determined Administrative Groupings: Manually partitions the country into broad macro-regions (Luzon/Visayas/Mindanao) or 2–3 selected cities.",
         "Data-Driven Unsupervised Clustering: Uses K-Means and Hierarchical Clustering across all 108 markets based on empirical volatility signatures.")
    ]

    for r_idx, (dim, trad, prop) in enumerate(contrast_data, start=1):
        row = contrast_table.rows[r_idx]
        bg = HEX_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate([dim, trad, prop]):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.color.rgb = COLOR_BLACK
            if c_idx == 0:
                r.font.bold = True

    add_para("", space_after=Pt(8))

    # 4. The Curated "Palengke Food Basket" Framework
    add_heading("4. The Curated 'Palengke Food Basket' Framework", 1)
    add_para(
        "To maximize analytical depth while maintaining rigorous feature engineering standards, the project filters the 73 available raw items "
        "into a focused, highly dense analytical core of 8 representative commodities (~60,157 observations). These commodities capture three "
        "distinct economic and logistical behavioral classes:"
    )

    basket_bullets = [
        ("Class 1: Staple Grains (Durable & Regulated) — ", "Rice (regular, milled) [9,920 records] and Rice (well milled) [6,300 records]. Characteristics: Long shelf life, heavy government monitoring, strategic NFA buffer reserves, and high sensitivity to import tariff modifications under RA 11203."),
        ("Class 2: Volatile Highland Vegetables (Perishable & Climate-Sensitive) — ", "Onions (red) [6,787 records], Tomatoes [7,779 records], and Cabbage [7,543 records]. Characteristics: Short shelf life, no long-term cold chain storage, violent post-typhoon price surges, and acute import-licensing dependency (as witnessed during the 2022–2023 onion crisis)."),
        ("Class 3: Core Animal Proteins (Disease & Feed-Sensitive) — ", "Meat (pork) [8,262 records], Meat (chicken, whole) [6,867 records], and Chicken Eggs [6,699 records]. Characteristics: Vulnerability to biological epidemics (African Swine Fever, Avian Influenza), reliance on imported soybean/corn animal feed, and strict cold-chain requirements.")
    ]
    for b_title, b_desc in basket_bullets:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(b_title)
        r_t.font.name = "Times New Roman"
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_BLACK
        r_d = p.add_run(b_desc)
        r_d.font.name = "Times New Roman"
        r_d.font.color.rgb = COLOR_BLACK

    # 5. Business Problem Canvas
    add_heading("5. Business Problem Canvas", 1)
    add_para("In accordance with Section 3 of the DS312 Project Guide, the proposed study is structured across the seven required dimensions:")

    canvas_table = doc.add_table(rows=8, cols=2)
    canvas_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    canvas_table.autofit = False
    set_table_borders(canvas_table, color="B0B0B0", sz="4")

    cw = [Inches(2.2), Inches(4.4)]
    for row in canvas_table.rows:
        for idx, w in enumerate(cw):
            row.cells[idx].width = w

    canvas_data = [
        ("Canvas Dimension", "Group Definition & Operational Scope"),
        ("Context / Organization", 
         "Department of Agriculture (DA), Department of Trade and Industry (DTI - Fair Trade Enforcement Bureau), National Food Authority (NFA), and Provincial/City Local Price Coordinating Councils (LPCCs)."),
        ("Problem Statement", 
         "Agricultural price monitoring in the Philippines is predominantly retrospective. Authorities lack an automated early-warning framework to detect structural market vulnerabilities, quantify middleman margins, and anticipate staple food price shocks before consumer purchasing power is compromised."),
        ("Stakeholders", 
         "1. Policy Makers (DA, DTI, NFA): Setting Suggested Retail Prices (SRP), adjusting tariff quotas, and authorizing buffer stock injections.\n"
         "2. Local Market Administrators & LGUs: Conducting targeted palengke inspections and monitoring regional price gouging.\n"
         "3. Farmers & Consumer Advocacy Groups: Utilizing transparent market margin benchmarks to prevent farm-gate exploitation."),
        ("Business Questions\n(Core Questions Answerable by Data)", 
         "1. Market Vulnerability Archetypes: Which Philippine wet markets act as price leaders (shock originators) versus price followers (lagged shock absorbers)?\n"
         "2. Price Shock Early Warning: Can we predict whether a staple commodity in a given province will experience a critical price shock (>20% monthly increase or >2σ historical volatility) 30–60 days ahead?\n"
         "3. Value-Chain Friction: How do margins between Farm Gate, Wholesale, and Retail prices vary across geographic regions and commodity classes?\n"
         "4. Temporal Seasonality & Lag Effects: What seasonal indicators and typhoon-quarter lag patterns systematically precede sustained food inflation?"),
        ("Success Criteria", 
         "1. Unsupervised Clustering: Uncover 3–5 statistically distinct market clusters (Silhouette Score ≥ 0.45) with meaningful logistical interpretations.\n"
         "2. Supervised Early Warning: Achieve an AUC-ROC ≥ 0.80 and Precision-Recall AUC significantly outperforming the ~10% minority baseline (>0.40) on 30-day price shock prediction.\n"
         "3. Policy Usability: Deliver concrete regulatory decision rules tied directly to model outputs."),
        ("Task Types\n(Dual Data Mining Families)", 
         "• Technique Family 1 (Unsupervised Learning): Spatial-Temporal Market Clustering (K-Means, Agglomerative Hierarchical Clustering, DBSCAN).\n"
         "• Technique Family 2 (Supervised Learning): Cost-Sensitive Binary Classification & Gradient-Boosted Trees (Logistic Regression Baseline vs. Random Forest & LightGBM/XGBoost)."),
        ("Risks and Limitations", 
         "• Irregular reporting cadences across remote provincial wet markets.\n"
         "• Exogenous shocks (typhoon landfall paths, global crude oil prices, fertilizer subsidies) must be approximated via temporal lag features.\n"
         "• Spanning 26 years requires nominal price standardization (CPI adjustment or rolling relative price ratios) to prevent historical nominal distortion.")
    ]

    for r_idx, (dim, val) in enumerate(canvas_data):
        row = canvas_table.rows[r_idx]
        cell_dim, cell_val = row.cells[0], row.cells[1]
        set_cell_margins(cell_dim, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell_val, top=70, bottom=70, left=100, right=100)
        
        p_d = cell_dim.paragraphs[0]
        p_d.paragraph_format.space_after = Pt(2)
        r_d = p_d.add_run(dim)
        r_d.font.name = "Times New Roman"
        r_d.font.bold = True
        r_d.font.color.rgb = COLOR_BLACK
        
        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(2)
        p_v.paragraph_format.line_spacing = 1.15
        r_v = p_v.add_run(val)
        r_v.font.name = "Times New Roman"
        r_v.font.color.rgb = COLOR_BLACK

        if r_idx == 0:
            set_cell_background(cell_dim, HEX_HEADER_BG)
            set_cell_background(cell_val, HEX_HEADER_BG)
        else:
            bg = HEX_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell_dim, bg)
            set_cell_background(cell_val, bg)

    add_para("", space_after=Pt(8))

    # 6. Evaluation of Candidate Datasets
    add_heading("6. Evaluation of Candidate Datasets (Phase 1 Selection)", 1)
    add_para(
        "To fulfill the Phase 1 requirement of evaluating 2–3 candidate datasets while strictly avoiding overused teaching datasets "
        "(Titanic, Iris, Boston Housing, Wine, MNIST), our group conducted a comparative evaluation across three realistic options:"
    )

    eval_table = doc.add_table(rows=6, cols=4)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eval_table.autofit = False
    set_table_borders(eval_table, color="B0B0B0", sz="4")

    ew = [Inches(1.8), Inches(1.6), Inches(1.6), Inches(1.6)]
    for row in eval_table.rows:
        for idx, w in enumerate(ew):
            row.cells[idx].width = w

    eval_headers = ["Criterion", "Candidate 1 (Selected):\nWFP Philippine Food Prices", "Candidate 2 (Alternative A):\nHotel Booking Demand", "Candidate 3 (Alternative B):\nOpenAQ Metro Manila Air"]
    for c_idx, h_text in enumerate(eval_headers):
        cell = eval_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_BLACK
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)

    eval_rows = [
        ("Public Source & Scale", 
         "WFP / HDX (Direct CSV)\n238,623 rows × 16 cols (Prices)\n132 rows × 7 cols (Markets)",
         "Kaggle / ScienceDirect\n119,390 rows × 32 cols\nSingle table",
         "OpenAQ API / Kaggle\n~80,000 hourly rows × 14 cols\nSensor time-series"),
        ("Authentic Messiness & Imperfections", 
         "High: Multi-tier supply pricing (Farm/Wholesale/Retail), 73 commodity variations, genuine crisis price shocks (onion crisis ₱1,200/kg), irregular reporting cadences.",
         "Moderate: Negative room rates (-$6.38), 180 phantom bookings (0 guests), missing company (94%), agent IDs.",
         "High: Negative sensor readings (-3.7 µg/m³), instrument flatline plateaus (72h frozen values), mixed units (ppm vs µg/m³)."),
        ("Two Data Mining Families Fit", 
         "Excellent:\n1. Unsupervised: Market Volatility & Geographic Clustering\n2. Supervised: Price Shock Prediction & Early Warning",
         "Excellent:\n1. Unsupervised: Guest Persona RFM Clustering\n2. Supervised: Booking Cancellation Prediction",
         "Good:\n1. Unsupervised: Sensor Anomaly Detection\n2. Supervised: Next-day PM2.5 Regression"),
        ("Philippine Societal Relevance", 
         "Maximum (10/10): Directly addresses national food inflation, rice tariffication, and DA/DTI consumer protection.",
         "Moderate (5/10): Generalized European hospitality operations (Portugal resort/city hotels).",
         "High (9/10): Metro Manila urban environmental health and clean air standards."),
        ("Final Verdict", 
         "SELECTED PRIMARY:\nHits 8/8 Advanced Complexity Tier, high societal relevance, robust 26-year longitudinal scale.",
         "Documented Alternative 1:\nExcellent technical fallback; pristine single CSV structure.",
         "Documented Alternative 2:\nHigh environmental value; requires heavier sensor-cleaning logic.")
    ]

    for r_idx, r_data in enumerate(eval_rows, start=1):
        bg = HEX_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(r_data):
            cell = eval_table.rows[r_idx].cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_BLACK
            if c_idx == 0:
                r.font.bold = True

    add_para("", space_after=Pt(8))

    # 7. Dataset Description & Data Dictionary
    add_heading("7. Dataset Description & Data Dictionary", 1)
    add_para(
        "The project utilizes the official United Nations World Food Programme (WFP) Vulnerability Analysis and Mapping (VAM) database for the Philippines, "
        "downloaded directly from the Humanitarian Data Exchange (HDX). The dataset is distributed under the Creative Commons Attribution 4.0 "
        "International (CC-BY 4.0) license and consists of two relational CSV tables:"
    )

    p_f1 = doc.add_paragraph(style='List Bullet')
    p_f1.paragraph_format.space_after = Pt(2)
    r = p_f1.add_run("wfp_food_prices_phl.csv: ")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    r2 = p_f1.add_run("Main longitudinal transactional table containing 238,623 observations, 16 features, spanning January 15, 2000 to August 15, 2026 (File size: 31.34 MB).")
    r2.font.name = "Times New Roman"
    r2.font.color.rgb = COLOR_BLACK

    p_f2 = doc.add_paragraph(style='List Bullet')
    p_f2.paragraph_format.space_after = Pt(6)
    r = p_f2.add_run("wfp_markets_phl.csv: ")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    r2 = p_f2.add_run("Market metadata table containing 132 unique monitored wet markets, administrative hierarchy, and geospatial coordinates (File size: 0.01 MB).")
    r2.font.name = "Times New Roman"
    r2.font.color.rgb = COLOR_BLACK

    add_para("Below is the comprehensive technical Data Dictionary for the primary price stream:", space_after=Pt(4))

    dict_table = doc.add_table(rows=17, cols=5)
    dict_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dict_table.autofit = False
    set_table_borders(dict_table, color="B0B0B0", sz="4")

    dw = [Inches(1.4), Inches(1.1), Inches(1.1), Inches(0.9), Inches(2.1)]
    for row in dict_table.rows:
        for idx, w in enumerate(dw):
            row.cells[idx].width = w

    dict_headers = ["Attribute", "Data Type", "Domain / Values", "Missing %", "Operational Definition"]
    for c_idx, h_text in enumerate(dict_headers):
        cell = dict_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_BLACK
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)

    dict_data = [
        ("date", "object (Date)", "2000-01-15 to 2026-08-15", "0.0%", "Date of monthly price capture (mid-month standardized)."),
        ("admin1", "object (Categorical)", "17 Regions", "0.0%", "First-level administrative region (e.g., NCR, Central Luzon, ARMM)."),
        ("admin2", "object (Categorical)", "79 Provinces", "0.0%", "Second-level administrative province (e.g., Nueva Ecija, Cebu, Davao)."),
        ("market", "object (Categorical)", "108 Market Names", "0.0%", "Specific wet market, trading post, or municipal monitoring hub."),
        ("market_id", "int64 (Key)", "167 to 3450", "0.0%", "Unique relational identifier for the physical market entity."),
        ("latitude", "float64 (Geospatial)", "4.82° to 18.57° N", "0.0%", "Geographic latitude coordinate of the monitored market."),
        ("longitude", "float64 (Geospatial)", "119.98° to 126.04° E", "0.0%", "Geographic longitude coordinate of the monitored market."),
        ("category", "object (Categorical)", "6 Macro Categories", "0.0%", "Macro food category (Vegetables/fruits, Meat/fish/eggs, Cereals/tubers)."),
        ("commodity", "object (Categorical)", "73 Specific Items", "0.0%", "Specific agricultural commodity name (e.g., 'Rice (regular, milled)')."),
        ("commodity_id", "int64 (Key)", "Unique IDs", "0.0%", "Standardized WFP commodity taxonomy code."),
        ("unit", "object (Categorical)", "KG, Unit, 750 ML", "0.0%", "Measurement packaging unit for the observed price."),
        ("priceflag", "object (Categorical)", "actual, aggregate", "0.0%", "Indicates whether price was surveyed directly or aggregated spatially."),
        ("pricetype", "object (Categorical)", "Retail, Wholesale, Farm Gate", "0.0%", "Supply chain tier (Retail = 231k, Wholesale = 6k, Farm Gate = 664)."),
        ("currency", "object (Categorical)", "PHP", "0.0%", "Monetary currency unit (Philippine Peso throughout)."),
        ("price", "float64 (Continuous)", "₱1.60 to ₱1,216.67", "0.0%", "Observed commodity price in Philippine Pesos."),
        ("usdprice", "float64 (Continuous)", "$0.03 to $22.12", "0.0%", "Exchange-rate adjusted price in United States Dollars.")
    ]

    for r_idx, r_data in enumerate(dict_data, start=1):
        bg = HEX_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(r_data):
            cell = dict_table.rows[r_idx].cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_BLACK
            if c_idx == 0:
                r.font.bold = True

    add_para("", space_after=Pt(8))

    # 8. Dataset Complexity Statement
    add_heading("8. Dataset Complexity Statement (Advanced Tier: 7–8 Points)", 1)
    add_para(
        "In accordance with Page 2 of the DS312 Project Guide, our group formally justifies positioning this project within the "
        "'Advanced' Dataset Quality and Complexity Tier (7–8 points). The complexity of this data is genuine, reflects authentic public-sector "
        "monitoring challenges, and requires non-trivial data science methods:"
    )

    c_points = [
        ("Multiple Relational Tables & Geospatial Integration: ", 
         "The project integrates the primary 238,623-row transactional price stream with the market metadata table using market_id. "
         "In Phase 2, the team will resolve boundary discrepancies and engineer spatial features (e.g., Euclidean and road-distance vectors from "
         "provincial wet markets to Metro Manila and regional shipping ports)."),
        ("High-Order Longitudinal Panel Structure: ", 
         "Spanning 319 consecutive monthly periods across 108 wet markets and 73 commodities, the data represents an unbalanced panel "
         "(Market × Commodity × Time). Handling this requires panel-data alignment, rolling window statistical transformations (1-month, 3-month, "
         "12-month returns), and time-series decomposition."),
        ("Categorical Granularity & Taxonomy Harmonization: ", 
         "The dataset records 6 distinct commodity variations for rice alone: 'Rice (regular, milled)', 'Rice (well milled)', "
         "'Rice (milled, superior)', 'Rice (premium)', 'Rice (special)', and 'Rice (paddy)'. Developing a domain-grounded commodity crosswalk "
         "aligned with DA/PSA standards is an essential data curation step."),
        ("Multi-Tier Supply Chain Economics & Unit Conversions: ", 
         "The dataset records prices across Retail (231,877 records), Wholesale (6,082 records), and Farm Gate (664 records), with varying units "
         "('KG', 'Unit', '750 ML'). Reconciling these tiers to analyze middleman margins requires group-level index standardization."),
        ("Authentic Macroeconomic Outliers: ", 
         "Prices range from ₱1.60 to ₱1,216.67. Real-world crisis shocks—such as the 2022–2023 onion crisis where Red Onion prices spiked to over "
         "₱1,000/kg—represent vital macroeconomic signals rather than clerical measurement errors. In Phase 2, our outlier treatment will model "
         "volatility shocks without blindly deleting authentic crisis events.")
    ]
    for p_title, p_desc in c_points:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(p_title)
        r_t.font.name = "Times New Roman"
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_BLACK
        r_d = p.add_run(p_desc)
        r_d.font.name = "Times New Roman"
        r_d.font.color.rgb = COLOR_BLACK

    # 9. Preliminary Data Mining Plan
    add_heading("9. Preliminary Data Mining Plan", 1)
    add_para(
        "To fulfill the Phase 1 rubric requirement of naming at least two candidate techniques from distinct families with clear justifications, "
        "our analytical framework combines Unsupervised Discovery with Supervised Predictive Modeling:"
    )

    add_heading("9.1 Technique Family 1: Unsupervised Spatial-Temporal Market Clustering", 2)
    add_para(
        "• Algorithms: K-Means Clustering, Agglomerative Hierarchical Clustering (Ward's linkage), and DBSCAN.\n"
        "• Purpose & Justification: Provincial wet markets do not respond to macroeconomic shocks uniformly. By summarizing each market across engineered "
        "volatility indicators (rolling standard deviation of price changes, average retail-to-wholesale markup, frequency of price spike occurrences, "
        "and geographic distance to agricultural hubs), clustering algorithms will segment Philippine markets into 3–5 behavioral archetypes "
        "(e.g., 'Volatile Island Importers', 'Stable Agricultural Granaries', 'Metro Manila Demand Centers').\n"
        "• Validation & Evaluation: Silhouette Analysis, Davies-Bouldin Index, and qualitative validation against regional DA trade profiles."
    )

    add_heading("9.2 Technique Family 2: Supervised Classification & Early Warning Modeling", 2)
    add_para(
        "• Algorithms: Cost-Sensitive Logistic Regression (Baseline) vs. Random Forest Classifier and Gradient Boosted Trees (LightGBM / XGBoost).\n"
        "• Target Variable Definition: Binary price shock indicator (Price_Shock_t+1 = 1 if Month-over-Month price increase ≥ 20% or exceeds 2 historical standard deviations; 0 otherwise).\n"
        "• Leakage Prevention Strategy: Standard random k-fold cross-validation is strictly invalid for time-series panel data because future prices would leak into historical training sets. We will enforce an expanding-window temporal cross-validation (TimeSeriesSplit): training on 2000–2021, tuning on 2022–2023, and blind out-of-time testing on 2024–2026.\n"
        "• Evaluation Metrics: Precision, Recall (critical because failing to predict a rice crisis has high societal cost), Area Under the Precision-Recall Curve (PR-AUC), and Brier Score."
    )

    # 10. Preview of Phase 3 EDA & Statistical Hypotheses
    add_heading("10. Preview of Phase 3 EDA & Statistical Hypotheses", 1)
    add_para("The dataset directly supports the mandatory Phase 3 statistical hypothesis testing requirements (Page 5 of guide):")

    h1 = doc.add_paragraph(style='List Bullet')
    h1.paragraph_format.space_after = Pt(3)
    h1.paragraph_format.line_spacing = 1.15
    r = h1.add_run("Hypothesis 1 (Two-Sample Welch's t-test / Mann-Whitney U): ")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    r2 = h1.add_run("H0: The mean monthly price volatility (coefficient of variation) of staple rice in island provinces (e.g., Palawan, Basilan, Sulu) is equal to that of mainland agricultural provinces (e.g., Nueva Ecija, Isabela). Ha: Island provinces experience significantly higher rice price volatility due to maritime transport friction (α = 0.05).")
    r2.font.name = "Times New Roman"
    r2.font.color.rgb = COLOR_BLACK

    h2 = doc.add_paragraph(style='List Bullet')
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.line_spacing = 1.15
    r = h2.add_run("Hypothesis 2 (One-Way ANOVA / Kruskal-Wallis Test): ")
    r.font.name = "Times New Roman"
    r.font.bold = True
    r.font.color.rgb = COLOR_BLACK
    r2 = h2.add_run("H0: The percentage spread between wholesale and retail prices is invariant across major commodity categories (Cereals, Vegetables, Meat). Ha: Perishable vegetables exhibit a significantly higher retail markup spread than staple cereals (α = 0.05).")
    r2.font.name = "Times New Roman"
    r2.font.color.rgb = COLOR_BLACK

    # 11. Project Timeline & Milestones
    add_heading("11. Project Execution Timeline & Milestones", 1)
    add_para("The group execution schedule aligns strictly with the official DS312 course calendar across all five phases:")

    time_table = doc.add_table(rows=6, cols=4)
    time_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    time_table.autofit = False
    set_table_borders(time_table, color="B0B0B0", sz="4")

    tw = [Inches(1.2), Inches(2.2), Inches(1.5), Inches(1.7)]
    for row in time_table.rows:
        for idx, w in enumerate(tw):
            row.cells[idx].width = w

    t_headers = ["Phase", "Core Focus & Key Tasks", "Course Dates", "Submission Deadline"]
    for c_idx, h_text in enumerate(t_headers):
        cell = time_table.rows[0].cells[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_BLACK
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)

    timeline_data = [
        ("Phase 1", "Dataset Selection, Business Problem Canvas, Data Dictionary, Candidate Comparison, Initial Ingestion", "Oct 12 – Oct 24", "Sun, Oct 25, 2026\n(Narrative: Oct 28)"),
        ("Phase 2", "Data Profiling, Missing Value Treatment, Outlier Resolution, Relational Joins, Preprocessing Log, Processed CSV", "Oct 26 – Nov 7", "Sun, Nov 8, 2026\n(Narrative: Nov 11)"),
        ("Phase 3", "Exploratory Data Analysis, 8+ Purposeful Visualizations, 2 Hypothesis Tests (t-test, ANOVA), Modeling Implications", "Nov 9 – Nov 14", "Sun, Nov 15, 2026\n(Narrative: Nov 18)"),
        ("Phase 4", "Model Training (Clustering + Classification), Baseline Comparison, Hyperparameter Tuning, Business Interpretation", "Nov 16 – Nov 28", "Sun, Nov 29, 2026\n(Narrative: Dec 2)"),
        ("Phase 5", "Master Jupyter Notebook, A1 Project Poster, 12-Slide PowerPoint Presentation, Final Project Defense", "Nov 30 – Dec 5", "Per Class Schedule\n(Dec 1–5, 2026)")
    ]

    for r_idx, r_data in enumerate(timeline_data, start=1):
        bg = HEX_ALT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(r_data):
            cell = time_table.rows[r_idx].cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_BLACK
            if c_idx == 0:
                r.font.bold = True

    add_para("", space_after=Pt(8))

    # 12. Individual Narrative Report Strategy
    add_heading("12. Individual Contribution & Accountability Strategy", 1)
    add_para(
        "To ensure every team member secures the maximum 20/20 points on the individual narrative reports (Section 8.1 of guide), "
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
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(r_title)
        r_t.font.name = "Times New Roman"
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_BLACK
        r_d = p.add_run(r_desc)
        r_d.font.name = "Times New Roman"
        r_d.font.color.rgb = COLOR_BLACK

    add_para(
        "Every phase submission will be cross-referenced with individual Git commit hashes and Jupyter cell annotations "
        "to ensure 100% concordance with submitted narrative reports."
    )

    # Save document
    output_primary = "reports/DS312_Phase1_Project_Proposal_Food_Security_Times_New_Roman.docx"
    doc.save(output_primary)
    print(f"Successfully generated proposal: {output_primary}")

    # Also attempt to overwrite the original if not locked by Word
    target_original = "reports/DS312_Phase1_Project_Proposal_Food_Security.docx"
    try:
        import shutil
        shutil.copyfile(output_primary, target_original)
        print(f"Successfully updated original file: {target_original}")
    except PermissionError:
        print(f"Note: {target_original} is currently open in Microsoft Word. Updated version saved to {output_primary}.")

if __name__ == "__main__":
    build_times_black_proposal()
