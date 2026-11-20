"""
scripts/render_layer_04.py
Layer 4: Data Collection & External Integration Layer (Cyan)
Exact architecture extracted from reference.
"""

import os
from pathlib import Path
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Users/AkashDeep/AppData/Local/Temp")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

from layer_helpers import save_all_formats

MMD_CONTENT = """flowchart TD
    %% =========================================================================
    %% LAYER 4: DATA COLLECTION & EXTERNAL INTEGRATION (CYAN)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef cyanNode fill:#ECFEFF,stroke:#0891B2,stroke-width:2.5px,color:#155E75,font-size:14px;
    classDef cloudNode fill:#CFFAFE,stroke:#0E7490,stroke-width:3px,color:#164E63,font-weight:bold,font-size:15px;
    classDef aiNode fill:#E0F2FE,stroke:#0284C7,stroke-width:2.5px,color:#075985,font-weight:bold,font-size:14px;
    classDef boundaryInL3 fill:#FFF7ED,stroke:#EA580C,stroke-width:2px,stroke-dasharray: 5 5,color:#9A3412,font-size:13px;
    classDef boundaryOutL5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,stroke-dasharray: 5 5,color:#064E3B,font-size:13px;
    classDef boundaryInL5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,stroke-dasharray: 5 5,color:#064E3B,font-size:13px;

    IN_L3_SEARCH[["From Layer 3: Request Validation<br/>(Valid Search Request)"]]:::boundaryInL3

    subgraph L4_CORE["LAYER 4: DATA COLLECTION & EXTERNAL INTEGRATION"]
        SRV_SEARCH["Search Service Orchestrator<br/>(services/search_service.py)"]:::cyanNode
        SRV_PUBMED["PubMed Service<br/>(services/pubmed_service.py)"]:::cyanNode
        API_NCBI["NCBI Entrez E-Utilities API<br/>(esearch.fcgi & efetch.fcgi)"]:::cloudNode
        XML_PARSER["ElementTree XML Parser<br/>(Extract PMID, Title, Abstract, Journal, Year, Authors, Affiliations)"]:::cyanNode
        ENRICH_AFF["Affiliation Enricher Fallback<br/>(services/pubmed_affiliation_enricher.py)"]:::cyanNode
        RERANKER["MedCPT Semantic Reranker<br/>(services/reranker_service.py - PyTorch & Transformers)"]:::aiNode
    end

    subgraph OUT_L5["OUTPUTS TO LAYER 5 (DATA CLEANING)"]
        OUT_L5_DEDUP_XML[["To Layer 5: Deduplication Engine<br/>(Raw Parsed Papers)"]]:::boundaryOutL5
        OUT_L5_DEDUP_AFF[["To Layer 5: Deduplication Engine<br/>(Enriched Affiliations)"]]:::boundaryOutL5
        OUT_L5_EXTRACT[["To Layer 5: Country Extractor Utility<br/>(Semantically Re-ranked Papers)"]]:::boundaryOutL5
    end

    IN_L5_DEDUP[["From Layer 5: Deduplication Engine<br/>(Deduplicated Records for Re-ranking)"]]:::boundaryInL5

    %% Internal Connections
    IN_L3_SEARCH --> SRV_SEARCH
    SRV_SEARCH --> SRV_PUBMED
    SRV_PUBMED <-->|HTTP GET/POST| API_NCBI
    SRV_PUBMED --> XML_PARSER

    XML_PARSER -->|Missing Affiliation| ENRICH_AFF
    XML_PARSER --> OUT_L5_DEDUP_XML
    ENRICH_AFF --> OUT_L5_DEDUP_AFF

    %% Reranker Flow (Cross-Layer with Layer 5)
    IN_L5_DEDUP --> RERANKER
    RERANKER --> OUT_L5_EXTRACT
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ECFEFF"/>
      <stop offset="100%" stop-color="#CFFAFE"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0E7490"/>
      <stop offset="100%" stop-color="#0891B2"/>
    </linearGradient>
    <marker id="arrowCyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0891B2"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#EA580C"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#ECFEFF"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#A5F3FC" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 4: DATA COLLECTION &amp; EXTERNAL INTEGRATION
  </text>
  <text x="1060" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#CFFAFE">
    Color Theme: Cyan | Scope: PubMed E-Utilities Ingestion &amp; MedCPT Reranker
  </text>

  <!-- Top-Left Input: Boundary from Layer 3 -->
  <g filter="url(#shadow)">
    <rect x="60" y="145" width="380" height="75" rx="10" fill="#FFF7ED" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="250" y="177" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      From Layer 3: Request Validation
    </text>
    <text x="250" y="200" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (Valid Search Query Parameters)
    </text>
  </g>

  <!-- Layer 4 Core Container -->
  <rect x="50" y="240" width="1030" height="670" rx="14" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="80" y="270" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#0E7490">
    4. DATA COLLECTION &amp; EXTERNAL INTEGRATION (Internal Architecture)
  </text>

  <!-- 1. Search Service Orchestrator -->
  <g filter="url(#shadow)">
    <rect x="80" y="300" width="440" height="85" rx="10" fill="url(#cyanGrad)" stroke="#0891B2" stroke-width="2.5"/>
    <text x="300" y="337" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#155E75" text-anchor="middle">
      Search Service Orchestrator
    </text>
    <text x="300" y="362" font-family="monospace" font-size="12" fill="#0E7490" text-anchor="middle">
      (services/search_service.py)
    </text>
  </g>
  <line x1="250" y1="220" x2="250" y2="300" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

  <!-- 2. PubMed Service -->
  <g filter="url(#shadow)">
    <rect x="80" y="440" width="440" height="85" rx="10" fill="url(#cyanGrad)" stroke="#0891B2" stroke-width="2.5"/>
    <text x="300" y="477" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#155E75" text-anchor="middle">
      PubMed Service
    </text>
    <text x="300" y="502" font-family="monospace" font-size="12" fill="#0E7490" text-anchor="middle">
      (services/pubmed_service.py)
    </text>
  </g>
  <line x1="300" y1="385" x2="300" y2="440" stroke="#0891B2" stroke-width="2.5" marker-end="url(#arrowCyan)"/>

  <!-- 3. External API: NCBI Entrez E-Utilities -->
  <g filter="url(#shadow)">
    <rect x="600" y="440" width="440" height="85" rx="12" fill="#CFFAFE" stroke="#0E7490" stroke-width="3"/>
    <text x="820" y="477" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#164E63" text-anchor="middle">
      NCBI Entrez E-Utilities API
    </text>
    <text x="820" y="502" font-family="monospace" font-size="13" fill="#0891B2" text-anchor="middle">
      (esearch.fcgi &amp; efetch.fcgi)
    </text>
  </g>
  <line x1="520" y1="475" x2="600" y2="475" stroke="#0E7490" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <line x1="600" y1="490" x2="520" y2="490" stroke="#0E7490" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <text x="560" y="465" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#0E7490" text-anchor="middle">
    HTTP GET/POST
  </text>

  <!-- 4. ElementTree XML Parser -->
  <g filter="url(#shadow)">
    <rect x="80" y="580" width="440" height="100" rx="10" fill="url(#cyanGrad)" stroke="#0891B2" stroke-width="2.5"/>
    <text x="300" y="615" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#155E75" text-anchor="middle">
      ElementTree XML Parser
    </text>
    <text x="300" y="640" font-family="system-ui, sans-serif" font-size="12" fill="#0E7490" text-anchor="middle">
      Extract PMID, Title, Abstract, Journal,
    </text>
    <text x="300" y="660" font-family="system-ui, sans-serif" font-size="12" fill="#0E7490" text-anchor="middle">
      Publication Year, Authors, Affiliations
    </text>
  </g>
  <line x1="300" y1="525" x2="300" y2="580" stroke="#0891B2" stroke-width="2.5" marker-end="url(#arrowCyan)"/>

  <!-- 5. Affiliation Enricher Fallback -->
  <g filter="url(#shadow)">
    <rect x="600" y="580" width="440" height="100" rx="10" fill="url(#cyanGrad)" stroke="#0891B2" stroke-width="2.5"/>
    <text x="820" y="620" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#155E75" text-anchor="middle">
      Affiliation Enricher Fallback
    </text>
    <text x="820" y="650" font-family="monospace" font-size="12" fill="#0E7490" text-anchor="middle">
      (services/pubmed_affiliation_enricher.py)
    </text>
  </g>
  <line x1="520" y1="630" x2="600" y2="630" stroke="#0891B2" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <text x="560" y="620" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#0891B2" text-anchor="middle">
    Missing Affiliation
  </text>

  <!-- 6. MedCPT Semantic Reranker (Bottom) -->
  <g filter="url(#shadow)">
    <rect x="80" y="760" width="960" height="90" rx="12" fill="#E0F2FE" stroke="#0284C7" stroke-width="2.5"/>
    <text x="560" y="798" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#075985" text-anchor="middle">
      MedCPT Semantic Reranker
    </text>
    <text x="560" y="825" font-family="monospace" font-size="12" fill="#0369A1" text-anchor="middle">
      (services/reranker_service.py - PyTorch &amp; Transformers ncbi/MedCPT)
    </text>
  </g>

  <!-- Right: Outputs & Inputs with Layer 5 -->
  <rect x="1110" y="240" width="440" height="670" rx="14" fill="#ECFDF5" stroke="#059669" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="1135" y="270" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#065F46">
    INTERACTIONS &harr; WITH LAYER 5 (DATA CLEANING)
  </text>

  <!-- Output 1: Parsed XML to Layer 5 Dedup -->
  <g filter="url(#shadow)">
    <rect x="1130" y="310" width="400" height="85" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1330" y="347" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#065F46" text-anchor="middle">
      To Layer 5: Deduplication Engine
    </text>
    <text x="1330" y="372" font-family="monospace" font-size="12" fill="#059669" text-anchor="middle">
      (Raw Extracted Paper Records)
    </text>
  </g>
  <path d="M 520 600 L 1100 600 L 1100 352 L 1130 352" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Output 2: Enriched Affiliations to Layer 5 Dedup -->
  <g filter="url(#shadow)">
    <rect x="1130" y="440" width="400" height="85" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1330" y="477" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#065F46" text-anchor="middle">
      To Layer 5: Deduplication Engine
    </text>
    <text x="1330" y="502" font-family="monospace" font-size="12" fill="#059669" text-anchor="middle">
      (Enriched Affiliation Metadata)
    </text>
  </g>
  <line x1="1040" y1="630" x2="1100" y2="630" stroke="#059669" stroke-width="2"/>
  <path d="M 1100 630 L 1100 482 L 1130 482" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Input from Layer 5 to Reranker -->
  <g filter="url(#shadow)">
    <rect x="1130" y="600" width="400" height="85" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1330" y="637" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#065F46" text-anchor="middle">
      From Layer 5: Deduplication Engine
    </text>
    <text x="1330" y="662" font-family="monospace" font-size="11" fill="#059669" text-anchor="middle">
      (Deduplicated Records for Re-ranking)
    </text>
  </g>
  <path d="M 1130 642 L 1070 642 L 1070 780 L 1040 780" fill="none" stroke="#0284C7" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrowCyan)"/>

  <!-- Output from Reranker to Layer 5 Country Extractor -->
  <g filter="url(#shadow)">
    <rect x="1130" y="760" width="400" height="85" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1330" y="797" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#065F46" text-anchor="middle">
      To Layer 5: Country Extractor Utility
    </text>
    <text x="1330" y="822" font-family="monospace" font-size="11" fill="#059669" text-anchor="middle">
      (Semantically Ranked Paper Records)
    </text>
  </g>
  <line x1="1040" y1="802" x2="1130" y2="802" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
</svg>
"""

def generate_layer_04():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#ECFEFF')
    ax.set_facecolor('#ECFEFF')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#A5F3FC", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#0E7490", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 4: DATA COLLECTION & EXTERNAL INTEGRATION",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Cyan | M.Tech Architecture Specification",
            fontsize=11, color="#CFFAFE", va='center', ha='right')

    # Input Boundary from L3
    in_l3 = FancyBboxPatch((60, 750), 380, 65, boxstyle="round,pad=6,rounding_size=8",
                           facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=2, linestyle="--")
    ax.add_patch(in_l3)
    ax.text(250, 792, "From Layer 3: Request Validation", fontsize=11, fontweight='bold', color="#9A3412", ha='center')
    ax.text(250, 770, "(Valid Search Query Parameters)", fontsize=9, fontfamily='monospace', color="#C2410C", ha='center')

    # Core Container: Layer 4
    c_box = FancyBboxPatch((50, 40), 1030, 680, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(80, 690, "4. DATA COLLECTION & EXTERNAL INTEGRATION (Internal Architecture)",
            fontsize=12, fontweight='bold', color="#0E7490")

    # 1. Search Service Orchestrator
    srv_search = FancyBboxPatch((80, 570), 440, 75, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2.5)
    ax.add_patch(srv_search)
    ax.text(300, 615, "Search Service Orchestrator", fontsize=13, fontweight='bold', color="#155E75", ha='center')
    ax.text(300, 592, "(services/search_service.py)", fontsize=10, fontfamily='monospace', color="#0E7490", ha='center')
    ax.annotate('', xy=(250, 645), xytext=(250, 750),
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=2.5, mutation_scale=12))

    # 2. PubMed Service
    srv_pubmed = FancyBboxPatch((80, 440), 440, 75, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2.5)
    ax.add_patch(srv_pubmed)
    ax.text(300, 485, "PubMed Service", fontsize=13, fontweight='bold', color="#155E75", ha='center')
    ax.text(300, 462, "(services/pubmed_service.py)", fontsize=10, fontfamily='monospace', color="#0E7490", ha='center')
    ax.annotate('', xy=(300, 515), xytext=(300, 570),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2, mutation_scale=12))

    # 3. NCBI Entrez E-Utilities API
    ncbi_api = FancyBboxPatch((600, 440), 440, 75, boxstyle="round,pad=8,rounding_size=10",
                              facecolor="#CFFAFE", edgecolor="#0E7490", linewidth=3)
    ax.add_patch(ncbi_api)
    ax.text(820, 485, "NCBI Entrez E-Utilities API", fontsize=14, fontweight='bold', color="#164E63", ha='center')
    ax.text(820, 462, "(esearch.fcgi & efetch.fcgi)", fontsize=11, fontfamily='monospace', color="#0891B2", ha='center')

    # Bidirectional arrows between PubMed and NCBI
    ax.annotate('', xy=(600, 485), xytext=(520, 485),
                arrowprops=dict(arrowstyle="<->", color="#0E7490", lw=2.5, mutation_scale=12))
    ax.text(560, 495, "HTTP GET/POST", fontsize=9, fontweight='bold', color="#0E7490", ha='center')

    # 4. ElementTree XML Parser
    xml_parser = FancyBboxPatch((80, 290), 440, 95, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2.5)
    ax.add_patch(xml_parser)
    ax.text(300, 355, "ElementTree XML Parser", fontsize=13, fontweight='bold', color="#155E75", ha='center')
    ax.text(300, 332, "Extract PMID, Title, Abstract, Journal,", fontsize=10, color="#0E7490", ha='center')
    ax.text(300, 312, "Year, Authors, Affiliations", fontsize=10, color="#0E7490", ha='center')
    ax.annotate('', xy=(300, 385), xytext=(300, 440),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2, mutation_scale=12))

    # 5. Affiliation Enricher Fallback
    enrich_aff = FancyBboxPatch((600, 290), 440, 95, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2.5)
    ax.add_patch(enrich_aff)
    ax.text(820, 350, "Affiliation Enricher Fallback", fontsize=13, fontweight='bold', color="#155E75", ha='center')
    ax.text(820, 325, "(services/pubmed_affiliation_enricher.py)", fontsize=10, fontfamily='monospace', color="#0E7490", ha='center')
    ax.annotate('', xy=(600, 337), xytext=(520, 337),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2, mutation_scale=12))
    ax.text(560, 345, "Missing Affiliation", fontsize=8, fontweight='bold', color="#0891B2", ha='center')

    # 6. MedCPT Semantic Reranker
    reranker = FancyBboxPatch((80, 80), 960, 75, boxstyle="round,pad=8,rounding_size=10",
                              facecolor="#E0F2FE", edgecolor="#0284C7", linewidth=2.5)
    ax.add_patch(reranker)
    ax.text(560, 125, "MedCPT Semantic Reranker", fontsize=14, fontweight='bold', color="#075985", ha='center')
    ax.text(560, 102, "(services/reranker_service.py - PyTorch & Transformers ncbi/MedCPT)", fontsize=10, fontfamily='monospace', color="#0369A1", ha='center')

    # Right Container: Interactions with Layer 5
    out_box = FancyBboxPatch((1110, 40), 440, 680, boxstyle="round,pad=8,rounding_size=12",
                             facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.5, linestyle="--")
    ax.add_patch(out_box)
    ax.text(1135, 690, "INTERACTIONS ↔ WITH LAYER 5 (DATA CLEANING)",
            fontsize=11, fontweight='bold', color="#065F46")

    # Outputs to L5
    out1 = FancyBboxPatch((1130, 540), 400, 75, boxstyle="round,pad=6,rounding_size=8",
                          facecolor="#FFFFFF", edgecolor="#059669", linewidth=2, linestyle="--")
    ax.add_patch(out1)
    ax.text(1330, 585, "To Layer 5: Deduplication Engine", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(1330, 562, "(Raw Parsed Paper Records)", fontsize=9, fontfamily='monospace', color="#059669", ha='center')

    out2 = FancyBboxPatch((1130, 400), 400, 75, boxstyle="round,pad=6,rounding_size=8",
                          facecolor="#FFFFFF", edgecolor="#059669", linewidth=2, linestyle="--")
    ax.add_patch(out2)
    ax.text(1330, 445, "To Layer 5: Deduplication Engine", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(1330, 422, "(Enriched Affiliation Metadata)", fontsize=9, fontfamily='monospace', color="#059669", ha='center')

    in_dedup = FancyBboxPatch((1130, 240), 400, 75, boxstyle="round,pad=6,rounding_size=8",
                              facecolor="#FFFFFF", edgecolor="#059669", linewidth=2, linestyle="--")
    ax.add_patch(in_dedup)
    ax.text(1330, 285, "From Layer 5: Deduplication Engine", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(1330, 262, "(Deduplicated Records for Re-ranking)", fontsize=9, fontfamily='monospace', color="#059669", ha='center')

    out_rerank = FancyBboxPatch((1130, 80), 400, 75, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#FFFFFF", edgecolor="#059669", linewidth=2, linestyle="--")
    ax.add_patch(out_rerank)
    ax.text(1330, 125, "To Layer 5: Country Extractor Utility", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(1330, 102, "(Semantically Re-ranked Papers)", fontsize=9, fontfamily='monospace', color="#059669", ha='center')

    # Arrows for cross-layer
    ax.plot([520, 1080, 1080], [350, 350, 577], color="#059669", lw=2)
    ax.annotate('', xy=(1130, 577), xytext=(1080, 577),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))

    ax.plot([1040, 1090, 1090], [337, 337, 437], color="#059669", lw=2)
    ax.annotate('', xy=(1130, 437), xytext=(1090, 437),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))

    ax.annotate('', xy=(1040, 130), xytext=(1130, 277),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=2, linestyle="--", mutation_scale=12))

    ax.annotate('', xy=(1130, 117), xytext=(1040, 117),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2.5, mutation_scale=12))

    save_all_formats("layer_04_data_collection", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_04()
