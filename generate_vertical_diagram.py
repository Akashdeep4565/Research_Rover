"""
Research Rover - Corrected Vertical Workflow Diagram Generator (Perfected Non-Overlapping Layout)
Produces:
1. diagram/research_rover_vertical_diagram.mmd (Pure valid Mermaid TD source)
2. diagram/research_rover_vertical_diagram.svg (Clean Miro-style standalone SVG)
3. diagram/research_rover_vertical_diagram.png (High-Resolution 300 DPI PNG)
"""

import os
import sys

# Ensure output directory exists
OUT_DIR = r"E:\Research_Rover\diagram"
os.makedirs(OUT_DIR, exist_ok=True)

# Set clean matplotlib config directory
os.environ["MPLCONFIGDIR"] = r"E:\Research_Rover\scratch"
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch


# ==============================================================================
# 1. GENERATE MERMAID WORKFLOW (.mmd)
# ==============================================================================
def generate_mermaid():
    mmd_content = """%% ====================================================================
%% Project: Research Rover
%% Diagram: End-to-End Vertical System Workflow & Architecture
%% Structure: Vertical Top-to-Bottom (flowchart TD)
%% Visual Style: Miro Clean Pastel Theme
%% ====================================================================

%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#B3ACFF',
    'primaryTextColor': '#1E1E1E',
    'primaryBorderColor': '#1E1E1E',
    'lineColor': '#1E1E1E',
    'secondaryColor': '#82D2FD',
    'tertiaryColor': '#FFDA54',
    'background': '#FFFFFF',
    'edgeLabelBackground': '#FFFFFF',
    'clusterBkg': '#F8FAFC',
    'clusterBorder': '#CBD5E1',
    'fontSize': '13px',
    'fontFamily': 'system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif'
  }
}}%%

flowchart TD

    %% -------------------------------------------------------------
    %% Class Definitions (Fully CSS Compliant - No rx/ry attributes)
    %% -------------------------------------------------------------
    classDef startEnd fill:#FFDA54,stroke:#1E1E1E,stroke-width:2px,color:#1E1E1E,font-weight:bold;
    classDef process fill:#B3ACFF,stroke:#1E1E1E,stroke-width:2px,color:#1E1E1E,font-weight:600;
    classDef decision fill:#82D2FD,stroke:#1E1E1E,stroke-width:2px,color:#1E1E1E,font-weight:bold;
    classDef errorState fill:#FFB3B3,stroke:#1E1E1E,stroke-width:2px,color:#1E1E1E,font-weight:600;

    %% =============================================================
    %% STAGE 1: USER INTERACTION
    %% =============================================================
    subgraph STAGE1 ["STAGE 1: USER INTERACTION"]
        Start(["Open Research Rover"]):::startEnd
        EnterQuery["Enter Research Query"]:::process
        ConfigOpts["Select Search Options<br/>(Unified, PubMed, OpenAlex)"]:::process
        SubmitReq["Submit Search Request"]:::process
    end

    %% =============================================================
    %% STAGE 2: SEARCH & API ORCHESTRATION
    %% =============================================================
    subgraph STAGE2 ["STAGE 2: SEARCH & API ORCHESTRATION"]
        FastAPI["FastAPI Orchestrator<br/>(Async Background Job)"]:::process
        QueryAPIs["Query Scholarly APIs<br/>(PubMed & OpenAlex)"]:::process
        DecAPI{"API Request<br/>Successful?"}:::decision
        ApiError["Display API Error<br/>& Prompt Retry"]:::errorState
    end

    %% =============================================================
    %% STAGE 3: DATA COLLECTION
    %% =============================================================
    subgraph STAGE3 ["STAGE 3: DATA COLLECTION"]
        FetchRecs["Retrieve Papers<br/>& Raw Metadata"]:::process
        DecPapers{"Research Papers<br/>Found?"}:::decision
        NoPapers["Display No-Results<br/>Message"]:::errorState
    end

    %% =============================================================
    %% STAGE 4: DEDUPLICATION & DATA ENRICHMENT
    %% =============================================================
    subgraph STAGE4 ["STAGE 4: DEDUPLICATION & DATA ENRICHMENT"]
        Dedup["Deduplicate & Merge Papers<br/>(Match DOI, PMID, Title)"]:::process
        ExtractAffil["Extract Affiliations<br/>& Normalize Countries (ISO-3)"]:::process
        SaveCSV["Save Standardized<br/>Corpus (CSV)"]:::process
    end

    %% =============================================================
    %% STAGE 5: BIBLIOMETRIC ANALYSIS & NETWORK CONSTRUCTION
    %% =============================================================
    subgraph STAGE5 ["STAGE 5: BIBLIOMETRIC ANALYSIS & NETWORK CONSTRUCTION"]
        Analytics["Compute Bibliometrics<br/>(Keywords & Country Frequencies)"]:::process
        BuildNet["Construct Networks<br/>(Co-occurrence & Collab Models)"]:::process
        DecAnalysis{"Analysis<br/>Successful?"}:::decision
        FallbackView["Fallback to Basic<br/>Metadata View"]:::errorState
    end

    %% =============================================================
    %% STAGE 6: AI RESEARCH ASSISTANT
    %% =============================================================
    subgraph STAGE6 ["STAGE 6: AI RESEARCH ASSISTANT"]
        AIChat["AI Research Assistant<br/>(Vector Q&A with Citations)"]:::process
    end

    %% =============================================================
    %% STAGE 7: VISUALIZATION & OUTPUT
    %% =============================================================
    subgraph STAGE7 ["STAGE 7: VISUALIZATION & OUTPUT"]
        RenderViz["Render Visualizations<br/>(Word Cloud, Charts, Maps)"]:::process
        ExploreCards["Explore Paper Cards<br/>(Abstracts, DOIs, OA Links)"]:::process
        DownloadPDF["Download OA PDFs<br/>(Safe Proxy Stream)"]:::process
        End(["Explore Insights<br/>& Export Data"]):::startEnd
    end

    %% =============================================================
    %% WORKFLOW CONNECTIONS & DECISION BRANCHES
    %% =============================================================
    Start --> EnterQuery
    EnterQuery --> ConfigOpts
    ConfigOpts --> SubmitReq
    SubmitReq --> FastAPI
    FastAPI --> QueryAPIs
    QueryAPIs --> DecAPI

    DecAPI -- No --> ApiError
    ApiError -.->|Retry Query| EnterQuery
    DecAPI -- Yes --> FetchRecs

    FetchRecs --> DecPapers
    DecPapers -- No --> NoPapers
    NoPapers -.->|Refine Search| EnterQuery
    DecPapers -- Yes --> Dedup

    Dedup --> ExtractAffil
    ExtractAffil --> SaveCSV

    SaveCSV --> Analytics
    Analytics --> BuildNet
    BuildNet --> DecAnalysis

    DecAnalysis -- No --> FallbackView
    FallbackView --> AIChat
    DecAnalysis -- Yes --> AIChat

    AIChat --> RenderViz
    RenderViz --> ExploreCards
    ExploreCards --> DownloadPDF
    DownloadPDF --> End
"""
    mmd_path = os.path.join(OUT_DIR, "research_rover_vertical_diagram.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"--> Saved Mermaid MMD: {mmd_path}")


# ==============================================================================
# 2. GENERATE STANDALONE CLEAN SVG (.svg)
# ==============================================================================
def generate_svg():
    width = 1200
    height = 3600
    cx = 570
    x_err = 940
    x_loop = 1120

    # Colors
    c_bg = "#FFFFFF"
    c_stage_bg = "#F8FAFC"
    c_stage_border = "#E2E8F0"
    c_stage_badge = "#475569"
    c_stage_badge_bg = "#F1F5F9"
    c_start_end = "#FFDA54"
    c_process = "#B3ACFF"
    c_decision = "#82D2FD"
    c_error = "#FFB3B3"
    c_border = "#1E1E1E"
    c_text = "#1E1E1E"
    c_arrow = "#1E1E1E"
    c_green = "#059669"
    c_red = "#DC2626"

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <defs>')
    # Marker for solid arrows
    svg.append('    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">')
    svg.append(f'      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="{c_arrow}" />')
    svg.append('    </marker>')
    # Marker for retry dashed arrows
    svg.append('    <marker id="arrow-dashed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">')
    svg.append(f'      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#DC2626" />')
    svg.append('    </marker>')
    # Marker for fallback dashed arrow
    svg.append('    <marker id="arrow-fallback" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">')
    svg.append(f'      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#6B7280" />')
    svg.append('    </marker>')
    # Subtle drop shadow filter
    svg.append('    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">')
    svg.append('      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000000" flood-opacity="0.06"/>')
    svg.append('    </filter>')
    svg.append('  </defs>')

    # Background
    svg.append(f'  <rect width="{width}" height="{height}" fill="{c_bg}" />')

    # Header Card
    svg.append('  <!-- HEADER -->')
    svg.append(f'  <rect x="50" y="30" width="1100" height="92" rx="16" fill="#F8FAFC" stroke="{c_stage_border}" stroke-width="2" filter="url(#shadow)" />')
    svg.append(f'  <rect x="75" y="52" width="48" height="48" rx="12" fill="{c_start_end}" stroke="{c_border}" stroke-width="2" />')
    svg.append(f'  <text x="99" y="82" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="20" font-weight="900" fill="{c_border}" text-anchor="middle">RR</text>')
    svg.append(f'  <text x="145" y="68" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="24" font-weight="800" fill="{c_text}">Research Rover | System Workflow &amp; Process Block Diagram</text>')
    svg.append(f'  <text x="145" y="96" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="14" font-weight="500" fill="#64748B">Standard Top-to-Bottom Architecture Pipeline (Stages 1–7) &bull; Clean Miro Edition &bull; M.Tech Defense</text>')

    # Helper for Stage Box
    def stage_box(y, h, stage_num, title):
        res = []
        res.append(f'  <!-- STAGE {stage_num}: {title} -->')
        res.append(f'  <rect x="50" y="{y}" width="1100" height="{h}" rx="18" fill="{c_stage_bg}" stroke="{c_stage_border}" stroke-width="1.5" />')
        badge_text = f"STAGE {stage_num}: {title.upper()}"
        bw = max(260, len(badge_text) * 7.5 + 36)
        res.append(f'  <rect x="75" y="{y + 16}" width="{bw}" height="28" rx="14" fill="{c_stage_badge_bg}" stroke="{c_stage_border}" stroke-width="1" />')
        res.append(f'  <text x="{75 + bw/2}" y="{y + 35}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="12" font-weight="700" fill="{c_stage_badge}" text-anchor="middle" letter-spacing="0.5">{badge_text}</text>')
        return "\n".join(res)

    # Helper for Process Box
    def process_box(x, y, w, h, title, subtitle=None, fill=c_process, is_pill=False):
        res = []
        rx = 26 if is_pill else 14
        res.append(f'  <rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c_border}" stroke-width="2" filter="url(#shadow)" />')
        if subtitle:
            res.append(f'  <text x="{x}" y="{y - 5}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="15" font-weight="700" fill="{c_text}" text-anchor="middle">{title}</text>')
            res.append(f'  <text x="{x}" y="{y + 16}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="12" font-weight="500" fill="#2E2E2E" text-anchor="middle">{subtitle}</text>')
        else:
            res.append(f'  <text x="{x}" y="{y + 5}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="15" font-weight="700" fill="{c_text}" text-anchor="middle">{title}</text>')
        return "\n".join(res)

    # Helper for Decision Diamond
    def decision_diamond(x, y, w, h, title1, title2=None):
        res = []
        pts = f"{x},{y - h/2} {x + w/2},{y} {x},{y + h/2} {x - w/2},{y}"
        res.append(f'  <polygon points="{pts}" fill="{c_decision}" stroke="{c_border}" stroke-width="2" filter="url(#shadow)" />')
        if title2:
            res.append(f'  <text x="{x}" y="{y - 4}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="14" font-weight="800" fill="{c_text}" text-anchor="middle">{title1}</text>')
            res.append(f'  <text x="{x}" y="{y + 15}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="14" font-weight="800" fill="{c_text}" text-anchor="middle">{title2}</text>')
        else:
            res.append(f'  <text x="{x}" y="{y + 5}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="14" font-weight="800" fill="{c_text}" text-anchor="middle">{title1}</text>')
        return "\n".join(res)

    # Helper for Vertical Arrow
    def v_arrow(x, y1, y2, label=None, label_color=c_green):
        res = []
        res.append(f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c_arrow}" stroke-width="2" marker-end="url(#arrow)" />')
        if label:
            ly = (y1 + y2) / 2
            res.append(f'  <rect x="{x - 22}" y="{ly - 10}" width="44" height="20" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />')
            res.append(f'  <text x="{x}" y="{ly + 4}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="11" font-weight="800" fill="{label_color}" text-anchor="middle">{label}</text>')
        return "\n".join(res)

    # Helper for Branch Out to Right
    def h_branch_right(x1, y1, x2, y2, label="No"):
        res = []
        res.append(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c_arrow}" stroke-width="2" marker-end="url(#arrow)" />')
        lx = (x1 + x2) / 2
        res.append(f'  <rect x="{lx - 16}" y="{y1 - 10}" width="32" height="20" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1" />')
        res.append(f'  <text x="{lx}" y="{y1 + 4}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="11" font-weight="800" fill="{c_red}" text-anchor="middle">{label}</text>')
        return "\n".join(res)

    # ==========================================================================
    # STAGE 1: User Interaction (Y: 150 to 580)
    # ==========================================================================
    s1_y = 150
    s1_h = 430
    svg.append(stage_box(s1_y, s1_h, 1, "User Interaction"))
    y_start = 225
    y_query = 315
    y_opts = 410
    y_sub = 505
    svg.append(process_box(cx, y_start, 320, 52, "Open Research Rover", None, c_start_end, is_pill=True))
    svg.append(v_arrow(cx, y_start + 26, y_query - 27))
    svg.append(process_box(cx, y_query, 340, 54, "Enter Research Query", "Scientific Topic, Author, or Keywords"))
    svg.append(v_arrow(cx, y_query + 27, y_opts - 30))
    svg.append(process_box(cx, y_opts, 340, 60, "Select Search Options", "Unified, PubMed, OpenAlex &bull; Date &bull; Limit"))
    svg.append(v_arrow(cx, y_opts + 30, y_sub - 27))
    svg.append(process_box(cx, y_sub, 340, 54, "Submit Search Request", "Dispatches API Parameters &amp; Initializes Job"))

    # Arrow S1 -> S2
    y_fastapi = 665
    svg.append(v_arrow(cx, y_sub + 27, y_fastapi - 30))

    # ==========================================================================
    # STAGE 2: Search & API Orchestration (Y: 605 to 1120)
    # ==========================================================================
    s2_y = 605
    s2_h = 515
    svg.append(stage_box(s2_y, s2_h, 2, "Search & API Orchestration"))
    y_queryapis = 770
    y_decapi = 910
    svg.append(process_box(cx, y_fastapi, 340, 60, "FastAPI Orchestrator", "Async Background Execution &amp; Real-Time Progress Polling"))
    svg.append(v_arrow(cx, y_fastapi + 30, y_queryapis - 30))
    svg.append(process_box(cx, y_queryapis, 340, 60, "Query Scholarly APIs", "Parallel NCBI PubMed E-Utilities &amp; OpenAlex REST API"))
    svg.append(v_arrow(cx, y_queryapis + 30, y_decapi - 50))
    svg.append(decision_diamond(cx, y_decapi, 220, 100, "API Request", "Successful?"))
    # Branch No -> ApiError
    svg.append(h_branch_right(cx + 110, y_decapi, x_err - 130, y_decapi, "No"))
    svg.append(process_box(x_err, y_decapi, 260, 58, "Display API Error", "&amp; Prompt Retry / Query Refine", c_error))

    # Arrow S2 -> S3 (Yes branch)
    y_fetch = 1205
    svg.append(v_arrow(cx, y_decapi + 50, y_fetch - 30, "Yes", c_green))

    # ==========================================================================
    # STAGE 3: Data Collection (Y: 1145 to 1590)
    # ==========================================================================
    s3_y = 1145
    s3_h = 445
    svg.append(stage_box(s3_y, s3_h, 3, "Data Collection"))
    y_decpapers = 1345
    svg.append(process_box(cx, y_fetch, 340, 60, "Retrieve Papers", "&amp; Raw Scholarly Metadata Records"))
    svg.append(v_arrow(cx, y_fetch + 30, y_decpapers - 50))
    svg.append(decision_diamond(cx, y_decpapers, 220, 100, "Research Papers", "Found?"))
    # Branch No -> NoPapers
    svg.append(h_branch_right(cx + 110, y_decpapers, x_err - 130, y_decpapers, "No"))
    svg.append(process_box(x_err, y_decpapers, 260, 58, "Display No-Results", "Suggest Synonyms &amp; Broaden Dates", c_error))

    # Arrow S3 -> S4 (Yes branch)
    y_dedup = 1675
    svg.append(v_arrow(cx, y_decpapers + 50, y_dedup - 30, "Yes", c_green))

    # ==========================================================================
    # STAGE 4: Deduplication & Data Enrichment (Y: 1615 to 2055)
    # ==========================================================================
    s4_y = 1615
    s4_h = 440
    svg.append(stage_box(s4_y, s4_h, 4, "Deduplication & Data Enrichment"))
    y_affil = 1775
    y_savecsv = 1875
    svg.append(process_box(cx, y_dedup, 340, 60, "Deduplicate &amp; Merge Papers", "Cross-Match DOI, PMID &amp; Canonical Title Key"))
    svg.append(v_arrow(cx, y_dedup + 30, y_affil - 30))
    svg.append(process_box(cx, y_affil, 340, 60, "Extract Affiliations", "&amp; Normalize Countries to ISO-3166 Alpha-3"))
    svg.append(v_arrow(cx, y_affil + 30, y_savecsv - 30))
    svg.append(process_box(cx, y_savecsv, 340, 60, "Save Standardized Corpus", "Persist Structured CSV Dataset in data/ Directory"))

    # Arrow S4 -> S5
    y_analytics = 2145
    svg.append(v_arrow(cx, y_savecsv + 30, y_analytics - 30))

    # ==========================================================================
    # STAGE 5: Bibliometric Analysis & Network Construction (Y: 2080 to 2620)
    # ==========================================================================
    s5_y = 2080
    s5_h = 540
    svg.append(stage_box(s5_y, s5_h, 5, "Bibliometric Analysis & Network Construction"))
    y_buildnet = 2250
    y_decanalysis = 2390
    svg.append(process_box(cx, y_analytics, 340, 60, "Compute Bibliometrics", "Keyword Frequency Ranking &amp; Country Distributions"))
    svg.append(v_arrow(cx, y_analytics + 30, y_buildnet - 30))
    svg.append(process_box(cx, y_buildnet, 340, 60, "Construct Networks", "Co-occurrence Graph &amp; International Collab Models"))
    svg.append(v_arrow(cx, y_buildnet + 30, y_decanalysis - 50))
    svg.append(decision_diamond(cx, y_decanalysis, 220, 100, "Analysis", "Successful?"))
    # Branch No -> FallbackView
    svg.append(h_branch_right(cx + 110, y_decanalysis, x_err - 130, y_decanalysis, "No"))
    svg.append(process_box(x_err, y_decanalysis, 260, 58, "Fallback View", "Basic Tabular Metadata Display", c_error))

    # Arrow S5 -> S6 (Yes branch)
    y_aichat = 2705
    svg.append(v_arrow(cx, y_decanalysis + 50, y_aichat - 30, "Yes", c_green))

    # Fallback connector into AI Chat
    svg.append(f'  <path d="M {x_err} {y_decanalysis + 29} L {x_err} {y_aichat} L {cx + 170} {y_aichat}" fill="none" stroke="#6B7280" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-fallback)" />')

    # ==========================================================================
    # STAGE 6: AI Research Assistant (Y: 2645 to 2825)
    # ==========================================================================
    s6_y = 2645
    s6_h = 180
    svg.append(stage_box(s6_y, s6_h, 6, "AI Research Assistant"))
    svg.append(process_box(cx, y_aichat, 340, 60, "AI Research Assistant", "RAG Pipeline &bull; FAISS Embeddings &bull; Grounded Q&amp;A"))

    # Arrow S6 -> S7
    y_renderviz = 2905
    svg.append(v_arrow(cx, y_aichat + 30, y_renderviz - 30))

    # ==========================================================================
    # STAGE 7: Visualization & Output (Y: 2845 to 3530)
    # ==========================================================================
    s7_y = 2845
    s7_h = 685
    svg.append(stage_box(s7_y, s7_h, 7, "Visualization & Output"))
    y_cards = 3025
    y_download = 3145
    y_end = 3265
    svg.append(process_box(cx, y_renderviz, 340, 60, "Render Visualizations", "Interactive Word Cloud, Charts &amp; Choropleth Map"))
    svg.append(v_arrow(cx, y_renderviz + 30, y_cards - 30))
    svg.append(process_box(cx, y_cards, 340, 60, "Explore Paper Cards", "Paper Cards, Abstract Drawer &amp; Direct OA Links"))
    svg.append(v_arrow(cx, y_cards + 30, y_download - 30))
    svg.append(process_box(cx, y_download, 340, 60, "Download OA PDFs", "Secure Streaming Proxy &amp; Document Verification"))
    svg.append(v_arrow(cx, y_download + 30, y_end - 27))
    svg.append(process_box(cx, y_end, 340, 54, "Explore Insights &amp; Export Data", None, c_start_end, is_pill=True))

    # ==========================================================================
    # RETRY LOOPBACK CONNECTORS (Dashed lines back to Stage 1 EnterQuery)
    # ==========================================================================
    svg.append('  <!-- RETRY LOOPBACK PATHS -->')
    # Loopback from ApiError up to EnterQuery
    svg.append(f'  <path d="M {x_err + 130} {y_decapi} L {x_loop} {y_decapi} L {x_loop} {y_query} L {cx + 170} {y_query}" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#arrow-dashed)" />')
    # Loopback from NoPapers joining the loop rail
    svg.append(f'  <path d="M {x_err + 130} {y_decpapers} L {x_loop} {y_decpapers} L {x_loop} {y_decapi}" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="6,4" />')
    # Loopback Label
    svg.append(f'  <rect x="{x_loop - 46}" y="{y_query - 25}" width="92" height="20" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />')
    svg.append(f'  <text x="{x_loop}" y="{y_query - 11}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="10" font-weight="700" fill="#DC2626" text-anchor="middle">RETRY QUERY</text>')

    svg.append('</svg>')

    svg_content = "\n".join(svg)
    svg_path = os.path.join(OUT_DIR, "research_rover_vertical_diagram.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"--> Saved Standalone SVG: {svg_path}")


# ==============================================================================
# 3. GENERATE HIGH-RESOLUTION PNG (.png) VIA MATPLOTLIB
# ==============================================================================
def generate_png():
    fig_w, fig_h = 13.5, 37.5
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Coordinate limits: X in [0, 100], Y in [0, 100]
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette (Pastel Miro Style)
    c_start_end = "#FFDA54"  # Warm Pastel Yellow
    c_process = "#B3ACFF"    # Pastel Lavender
    c_decision = "#82D2FD"   # Sky Blue
    c_error = "#FFB3B3"      # Soft Coral / Pastel Red
    c_border = "#1E1E1E"     # Dark Charcoal
    c_text = "#1E1E1E"
    c_stage_bg = "#F8FAFC"
    c_stage_border = "#E2E8F0"
    c_green = "#059669"
    c_red = "#DC2626"

    # Header Card
    header_box = FancyBboxPatch((4.5, 96.2), 91.0, 2.6,
                                boxstyle="round,pad=0.2,rounding_size=0.8",
                                facecolor="#F8FAFC", edgecolor=c_stage_border, linewidth=1.5, zorder=2)
    ax.add_patch(header_box)
    logo_box = FancyBboxPatch((6.0, 96.6), 2.4, 1.8,
                              boxstyle="round,pad=0.1,rounding_size=0.4",
                              facecolor=c_start_end, edgecolor=c_border, linewidth=1.5, zorder=3)
    ax.add_patch(logo_box)
    ax.text(7.2, 97.5, "RR", fontsize=11, fontweight='bold', color=c_border, ha='center', va='center', zorder=4)
    ax.text(10.0, 97.9, "Research Rover | System Workflow & Process Block Diagram", fontsize=14.5, fontweight='bold', color=c_text, va='center', zorder=4)
    ax.text(10.0, 96.9, "Standard Top-to-Bottom Architecture Pipeline (Stages 1–7) • Clean Miro Edition • M.Tech Defense", fontsize=9.2, color="#64748B", va='center', zorder=4)

    # Helper: Stage Container with guaranteed non-overlapping top banner
    def draw_stage(y_top, height, stage_num, stage_title):
        y_bottom = y_top - height
        sb = FancyBboxPatch((4.5, y_bottom), 91.0, height,
                            boxstyle="round,pad=0.2,rounding_size=0.9",
                            facecolor=c_stage_bg, edgecolor=c_stage_border, linewidth=1.2, zorder=1)
        ax.add_patch(sb)
        badge_text = f"STAGE {stage_num}: {stage_title.upper()}"
        bw = max(28.0, len(badge_text) * 0.68 + 2.5)
        badge = FancyBboxPatch((6.5, y_top - 1.35), bw, 0.85,
                              boxstyle="round,pad=0.1,rounding_size=0.4",
                              facecolor="#F1F5F9", edgecolor=c_stage_border, linewidth=1, zorder=2)
        ax.add_patch(badge)
        ax.text(6.5 + bw/2, y_top - 0.92, badge_text, fontsize=7.6, fontweight='bold', color="#475569", ha='center', va='center', zorder=3)

    # Helper: Process Box
    def draw_box(x, y, w, h, title, subtitle=None, color=c_process, is_pill=False):
        rs = 1.0 if is_pill else 0.5
        p = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle=f"round,pad=0.1,rounding_size={rs}",
                           facecolor=color, edgecolor=c_border, linewidth=1.6, zorder=5)
        ax.add_patch(p)
        if subtitle:
            ax.text(x, y + 0.32, title, fontsize=9.6, fontweight='bold', color=c_text, ha='center', va='center', zorder=6)
            ax.text(x, y - 0.42, subtitle, fontsize=7.6, color="#374151", ha='center', va='center', zorder=6)
        else:
            ax.text(x, y, title, fontsize=10.0, fontweight='bold', color=c_text, ha='center', va='center', zorder=6)

    # Helper: Decision Diamond
    def draw_diamond(x, y, w, h, title1, title2):
        pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
        poly = Polygon(pts, closed=True, facecolor=c_decision, edgecolor=c_border, linewidth=1.6, zorder=5)
        ax.add_patch(poly)
        ax.text(x, y + 0.28, title1, fontsize=9.2, fontweight='bold', color=c_text, ha='center', va='center', zorder=6)
        ax.text(x, y - 0.32, title2, fontsize=9.2, fontweight='bold', color=c_text, ha='center', va='center', zorder=6)

    # Helper: Vertical Arrow
    def draw_v_arrow(x, y_start, y_end, label=None, label_color=c_green):
        arrow = FancyArrowPatch((x, y_start), (x, y_end),
                                arrowstyle='-|>', mutation_scale=13,
                                color=c_border, linewidth=1.6, zorder=4)
        ax.add_patch(arrow)
        if label:
            ly = (y_start + y_end) / 2
            bb = FancyBboxPatch((x - 1.8, ly - 0.4), 3.6, 0.8,
                                boxstyle="round,pad=0.05,rounding_size=0.2",
                                facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.8, zorder=7)
            ax.add_patch(bb)
            ax.text(x, ly, label, fontsize=8, fontweight='bold', color=label_color, ha='center', va='center', zorder=8)

    # Helper: Branch to Right
    def draw_h_branch(x1, y1, x2, y2, label="No"):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle='-|>', mutation_scale=13,
                                color=c_border, linewidth=1.6, zorder=4)
        ax.add_patch(arrow)
        lx = (x1 + x2) / 2
        bb = FancyBboxPatch((lx - 1.4, y1 - 0.4), 2.8, 0.8,
                            boxstyle="round,pad=0.05,rounding_size=0.2",
                            facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.8, zorder=7)
        ax.add_patch(bb)
        ax.text(lx, y1, label, fontsize=8, fontweight='bold', color=c_red, ha='center', va='center', zorder=8)

    cx = 48.0   # Center X for vertical backbone
    rx = 78.0   # Right side branch X
    bw = 30.0   # Standard Process Box Width
    bh = 1.6    # Standard Process Box Height
    loop_x = 92.5 # Red dashed loopback rail

    # ==========================================================================
    # STAGE 1: User Interaction (Y: 83.5 to 95.5)
    # ==========================================================================
    draw_stage(95.5, 12.0, 1, "User Interaction")
    y_start = 93.2
    y_query = 90.4
    y_opts  = 87.4
    y_sub   = 84.4
    draw_box(cx, y_start, 26.0, 1.4, "Open Research Rover", None, c_start_end, is_pill=True)
    draw_v_arrow(cx, y_start - 0.7, y_query + 0.8)
    draw_box(cx, y_query, bw, bh, "Enter Research Query", "Scientific Topic, Author, or Medical Terms")
    draw_v_arrow(cx, y_query - 0.8, y_opts + 0.8)
    draw_box(cx, y_opts, bw, bh, "Select Search Options", "Unified, PubMed, OpenAlex • Date Bounds • Result Limit")
    draw_v_arrow(cx, y_opts - 0.8, y_sub + 0.8)
    draw_box(cx, y_sub, bw, bh, "Submit Search Request", "Dispatches API Parameters & Initializes Job")

    # Arrow S1 -> S2
    y_fastapi = 79.5
    draw_v_arrow(cx, y_sub - 0.8, y_fastapi + 0.8)

    # ==========================================================================
    # STAGE 2: Search & API Orchestration (Y: 68.5 to 82.5)
    # ==========================================================================
    draw_stage(82.5, 14.0, 2, "Search & API Orchestration")
    y_queryapis = 76.0
    y_decapi = 72.0
    draw_box(cx, y_fastapi, bw, bh, "FastAPI Orchestrator", "Async Background Execution & Real-Time Progress Polling")
    draw_v_arrow(cx, y_fastapi - 0.8, y_queryapis + 0.8)
    draw_box(cx, y_queryapis, bw, bh, "Query Scholarly APIs", "Parallel NCBI PubMed E-Utilities & OpenAlex REST API")
    draw_v_arrow(cx, y_queryapis - 0.8, y_decapi + 1.4)
    draw_diamond(cx, y_decapi, 18.0, 2.8, "API Request", "Successful?")
    # Branch No
    draw_h_branch(cx + 9.0, y_decapi, rx - 10.0, y_decapi, "No")
    draw_box(rx, y_decapi, 20.0, bh, "Display API Error", "& Prompt Retry / Query Refine", c_error)

    # Arrow S2 -> S3 (Yes branch)
    y_fetch = 64.6
    draw_v_arrow(cx, y_decapi - 1.4, y_fetch + 0.8, "Yes", c_green)

    # ==========================================================================
    # STAGE 3: Data Collection (Y: 56.5 to 67.5)
    # ==========================================================================
    draw_stage(67.5, 11.0, 3, "Data Collection")
    y_decpapers = 60.6
    draw_box(cx, y_fetch, bw, bh, "Retrieve Papers", "& Raw Scholarly Metadata Records")
    draw_v_arrow(cx, y_fetch - 0.8, y_decpapers + 1.4)
    draw_diamond(cx, y_decpapers, 18.0, 2.8, "Research Papers", "Found?")
    # Branch No
    draw_h_branch(cx + 9.0, y_decpapers, rx - 10.0, y_decpapers, "No")
    draw_box(rx, y_decpapers, 20.0, bh, "Display No-Results", "Suggest Synonyms & Broaden Dates", c_error)

    # Arrow S3 -> S4 (Yes branch)
    y_dedup = 52.4
    draw_v_arrow(cx, y_decpapers - 1.4, y_dedup + 0.8, "Yes", c_green)

    # ==========================================================================
    # STAGE 4: Deduplication & Data Enrichment (Y: 43.5 to 55.5)
    # ==========================================================================
    draw_stage(55.5, 12.0, 4, "Deduplication & Data Enrichment")
    y_affil = 49.2
    y_savecsv = 46.0
    draw_box(cx, y_dedup, bw, bh, "Deduplicate & Merge Papers", "Cross-Match DOI, PMID & Canonical Title Key")
    draw_v_arrow(cx, y_dedup - 0.8, y_affil + 0.8)
    draw_box(cx, y_affil, bw, bh, "Extract Affiliations", "& Normalize Countries to ISO-3166 Alpha-3")
    draw_v_arrow(cx, y_affil - 0.8, y_savecsv + 0.8)
    draw_box(cx, y_savecsv, bw, bh, "Save Standardized Corpus", "Persist Structured CSV Dataset in data/ Directory")

    # Arrow S4 -> S5
    y_analytics = 39.2
    draw_v_arrow(cx, y_savecsv - 0.8, y_analytics + 0.8)

    # ==========================================================================
    # STAGE 5: Bibliometric Analysis & Network Construction (Y: 28.0 to 42.5)
    # Clear gap between badge at 41.5 and box at 39.2
    # ==========================================================================
    draw_stage(42.5, 14.5, 5, "Bibliometric Analysis & Network Construction")
    y_buildnet = 35.6
    y_decanalysis = 31.6
    draw_box(cx, y_analytics, bw, bh, "Compute Bibliometrics", "Keyword Frequency Ranking & Country Distributions")
    draw_v_arrow(cx, y_analytics - 0.8, y_buildnet + 0.8)
    draw_box(cx, y_buildnet, bw, bh, "Construct Networks", "Co-occurrence Graph & International Collab Models")
    draw_v_arrow(cx, y_buildnet - 0.8, y_decanalysis + 1.4)
    draw_diamond(cx, y_decanalysis, 18.0, 2.8, "Analysis", "Successful?")
    # Branch No
    draw_h_branch(cx + 9.0, y_decanalysis, rx - 10.0, y_decanalysis, "No")
    draw_box(rx, y_decanalysis, 20.0, bh, "Fallback View", "Basic Tabular Metadata Display", c_error)

    # Arrow S5 -> S6 (Yes branch)
    y_aichat = 23.5
    draw_v_arrow(cx, y_decanalysis - 1.4, y_aichat + 0.8, "Yes", c_green)

    # Fallback connector into AI Chat
    ax.plot([rx, rx, cx + bw/2], [y_decanalysis - bh/2, y_aichat, y_aichat],
            linestyle='--', color="#6B7280", linewidth=1.5, zorder=4)
    arrow_fb = FancyArrowPatch((cx + bw/2 + 1.5, y_aichat), (cx + bw/2, y_aichat),
                              arrowstyle='-|>', mutation_scale=12,
                              color="#6B7280", linewidth=1.5, zorder=4)
    ax.add_patch(arrow_fb)

    # ==========================================================================
    # STAGE 6: AI Research Assistant (Y: 20.5 to 27.0)
    # ==========================================================================
    draw_stage(27.0, 6.5, 6, "AI Research Assistant")
    draw_box(cx, y_aichat, bw, bh, "AI Research Assistant", "RAG Pipeline • FAISS Embeddings • Grounded Q&A")

    # Arrow S6 -> S7
    y_renderviz = 16.2
    draw_v_arrow(cx, y_aichat - 0.8, y_renderviz + 0.8)

    # ==========================================================================
    # STAGE 7: Visualization & Output (Y: 1.5 to 19.5)
    # ==========================================================================
    draw_stage(19.5, 18.0, 7, "Visualization & Output")
    y_cards = 12.6
    y_download = 9.0
    y_end = 5.0
    draw_box(cx, y_renderviz, bw, bh, "Render Visualizations", "Interactive Word Cloud, Charts & Choropleth Map")
    draw_v_arrow(cx, y_renderviz - 0.8, y_cards + 0.8)
    draw_box(cx, y_cards, bw, bh, "Explore Paper Cards", "Paper Cards, Abstract Drawer & Direct OA Links")
    draw_v_arrow(cx, y_cards - 0.8, y_download + 0.8)
    draw_box(cx, y_download, bw, bh, "Download OA PDFs", "Secure Streaming Proxy & Document Verification")
    draw_v_arrow(cx, y_download - 0.8, y_end + 0.7)
    draw_box(cx, y_end, 28.0, 1.4, "Explore Insights & Export Data", None, c_start_end, is_pill=True)

    # ==========================================================================
    # RETRY LOOPBACK ROUTING (Continuous Dashed Red Line back to EnterQuery)
    # ==========================================================================
    # Path from ApiError up to EnterQuery
    ax.plot([rx + 10.0, loop_x, loop_x, cx + bw/2],
            [y_decapi, y_decapi, y_query, y_query],
            linestyle='--', color=c_red, linewidth=1.5, zorder=4)
    # Path from NoPapers connecting up into the loop rail
    ax.plot([rx + 10.0, loop_x, loop_x],
            [y_decpapers, y_decpapers, y_decapi],
            linestyle='--', color=c_red, linewidth=1.5, zorder=4)
    # Arrow into EnterQuery
    arrow_retry = FancyArrowPatch((cx + bw/2 + 1.5, y_query), (cx + bw/2, y_query),
                                 arrowstyle='-|>', mutation_scale=12,
                                 color=c_red, linewidth=1.5, zorder=4)
    ax.add_patch(arrow_retry)
    lbl_box = FancyBboxPatch((loop_x - 3.5, y_query + 0.5), 7.0, 0.8,
                             boxstyle="round,pad=0.05,rounding_size=0.2",
                             facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.8, zorder=7)
    ax.add_patch(lbl_box)
    ax.text(loop_x, y_query + 0.9, "RETRY QUERY", fontsize=7.2, fontweight='bold', color=c_red, ha='center', va='center', zorder=8)

    plt.tight_layout()
    png_path = os.path.join(OUT_DIR, "research_rover_vertical_diagram.png")
    plt.savefig(png_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"--> Saved High-Res PNG: {png_path}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("GENERATING CORRECTED VERTICAL RESEARCH ROVER WORKFLOW DIAGRAM")
    print("=" * 70)
    generate_mermaid()
    generate_svg()
    generate_png()
    print("=" * 70)
    print("SUCCESS: Generated all 3 deliverables in diagram/ folder.")
    print("=" * 70)
