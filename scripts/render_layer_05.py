"""
scripts/render_layer_05.py
Layer 5: Data Cleaning & Enrichment Layer (Green)
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
    %% LAYER 5: DATA CLEANING & ENRICHMENT (GREEN)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef greenNode fill:#ECFDF5,stroke:#059669,stroke-width:2.5px,color:#064E3B,font-size:14px;
    classDef storageNode fill:#D1FAE5,stroke:#047857,stroke-width:3px,color:#065F46,font-weight:bold,font-size:15px;
    classDef boundaryInL4 fill:#ECFEFF,stroke:#0891B2,stroke-width:2px,stroke-dasharray: 5 5,color:#155E75,font-size:13px;
    classDef boundaryOutL4 fill:#ECFEFF,stroke:#0891B2,stroke-width:2px,stroke-dasharray: 5 5,color:#155E75,font-size:13px;
    classDef boundaryOutL6 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,stroke-dasharray: 5 5,color:#581C87,font-size:13px;

    subgraph IN_L4["INPUTS FROM LAYER 4 (DATA COLLECTION)"]
        IN_L4_XML[["From Layer 4: XML Parser<br/>(Extracted Raw Papers)"]]:::boundaryInL4
        IN_L4_AFF[["From Layer 4: Affiliation Fallback<br/>(Enriched Metadata)"]]:::boundaryInL4
    end

    subgraph L5_CORE["LAYER 5: DATA CLEANING & ENRICHMENT"]
        DEDUP["Deduplication Engine<br/>(Deduplicate by PMID, DOI, and Title)"]:::greenNode
        EXTRACT_CTRY["Country Extractor Utility<br/>(utils/country_extractor.py - Regex & ISO 3166-1 Map)"]:::greenNode
        CSV_LOADER["CSV Loader & Writer<br/>(utils/csv_loader.py - UTF-8-BOM / Latin-1 Fallbacks)"]:::greenNode
        DATA_STORE[("Local CSV Data Storage<br/>data/*.csv")]:::storageNode
    end

    OUT_L4_RERANK[["To Layer 4: MedCPT Semantic Reranker<br/>(Deduplicated Records)"]]:::boundaryOutL4
    IN_L4_RERANKED[["From Layer 4: MedCPT Semantic Reranker<br/>(Ranked Records)"]]:::boundaryInL4

    subgraph OUT_L6["OUTPUTS TO LAYER 6 (ANALYSIS ENGINES)"]
        OUT_L6_KW[["To Layer 6: Analysis Service<br/>(Keyword Analytics Dataset)"]]:::boundaryOutL6
        OUT_L6_CTRY[["To Layer 6: Country Service<br/>(Country & Collaboration Dataset)"]]:::boundaryOutL6
        OUT_L6_EMBED[["To Layer 6: Embedding Service<br/>(Full Text for FAISS Vector Index)"]]:::boundaryOutL6
    end

    %% Internal Connections
    IN_L4_XML --> DEDUP
    IN_L4_AFF --> DEDUP
    
    DEDUP --> OUT_L4_RERANK
    IN_L4_RERANKED --> EXTRACT_CTRY
    
    EXTRACT_CTRY --> CSV_LOADER
    CSV_LOADER --> DATA_STORE

    %% External Outgoing Connections to Layer 6
    DATA_STORE --> OUT_L6_KW
    DATA_STORE --> OUT_L6_CTRY
    DATA_STORE --> OUT_L6_EMBED
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ECFDF5"/>
      <stop offset="100%" stop-color="#D1FAE5"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrowCyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0891B2"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#9333EA"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#ECFDF5"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 5: DATA CLEANING &amp; ENRICHMENT LAYER
  </text>
  <text x="1050" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#D1FAE5">
    Color Theme: Green | Scope: Deduplication, ISO-3 Extraction &amp; CSV Persistence
  </text>

  <!-- Left: Inputs & Reranking Exchange with Layer 4 -->
  <rect x="50" y="130" width="360" height="780" rx="14" fill="#F0FDFA" stroke="#0891B2" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="75" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#0E7490">
    INTERACTIONS &harr; WITH LAYER 4
  </text>

  <!-- Input 1 from L4: XML Parser -->
  <g filter="url(#shadow)">
    <rect x="70" y="200" width="320" height="85" rx="10" fill="#ECFEFF" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="230" y="235" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#155E75" text-anchor="middle">
      From Layer 4: XML Parser
    </text>
    <text x="230" y="258" font-family="monospace" font-size="11" fill="#0E7490" text-anchor="middle">
      (Extracted Raw Paper Records)
    </text>
  </g>

  <!-- Input 2 from L4: Affiliation Enricher -->
  <g filter="url(#shadow)">
    <rect x="70" y="325" width="320" height="85" rx="10" fill="#ECFEFF" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="230" y="360" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#155E75" text-anchor="middle">
      From Layer 4: Affiliation Enricher
    </text>
    <text x="230" y="383" font-family="monospace" font-size="11" fill="#0E7490" text-anchor="middle">
      (Fallback Enriched Metadata)
    </text>
  </g>

  <!-- Output to L4 Reranker -->
  <g filter="url(#shadow)">
    <rect x="70" y="520" width="320" height="85" rx="10" fill="#ECFEFF" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="230" y="555" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#155E75" text-anchor="middle">
      To Layer 4: MedCPT Reranker
    </text>
    <text x="230" y="578" font-family="monospace" font-size="11" fill="#0E7490" text-anchor="middle">
      (Deduplicated Records)
    </text>
  </g>

  <!-- Input from L4 Reranker -->
  <g filter="url(#shadow)">
    <rect x="70" y="660" width="320" height="85" rx="10" fill="#ECFEFF" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="230" y="695" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#155E75" text-anchor="middle">
      From Layer 4: MedCPT Reranker
    </text>
    <text x="230" y="718" font-family="monospace" font-size="11" fill="#0E7490" text-anchor="middle">
      (Semantically Ranked Papers)
    </text>
  </g>

  <!-- Center Container: Layer 5 Core -->
  <rect x="440" y="130" width="670" height="780" rx="14" fill="#ECFDF5" stroke="#059669" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="465" y="160" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#047857">
    5. DATA CLEANING &amp; ENRICHMENT (Internal Architecture)
  </text>

  <!-- Node 1: Deduplication Engine -->
  <g filter="url(#shadow)">
    <rect x="480" y="240" width="590" height="95" rx="12" fill="url(#greenGrad)" stroke="#059669" stroke-width="3"/>
    <text x="775" y="278" font-family="system-ui, sans-serif" font-size="17" font-weight="bold" fill="#064E3B" text-anchor="middle">
      Deduplication Engine
    </text>
    <text x="775" y="305" font-family="system-ui, sans-serif" font-size="13" fill="#047857" text-anchor="middle">
      (Deduplicate by PMID, DOI, and Title Key Matching)
    </text>
  </g>

  <!-- Arrows from Inputs into Dedup -->
  <path d="M 390 242 L 440 242 L 440 270 L 480 270" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <path d="M 390 367 L 440 367 L 440 300 L 480 300" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Arrow Dedup to Reranker -->
  <path d="M 775 335 L 775 480 L 230 480 L 230 520" fill="none" stroke="#0891B2" stroke-width="2.5" marker-end="url(#arrowCyan)"/>
  <text x="450" y="470" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#0891B2">
    Send to MedCPT Reranker
  </text>

  <!-- Arrow from Reranked to Country Extractor -->
  <path d="M 390 702 L 440 702 L 440 450 L 480 450" fill="none" stroke="#0891B2" stroke-width="2.5" marker-end="url(#arrowCyan)"/>

  <!-- Node 2: Country Extractor Utility -->
  <g filter="url(#shadow)">
    <rect x="480" y="410" width="590" height="95" rx="12" fill="url(#greenGrad)" stroke="#059669" stroke-width="2.5"/>
    <text x="775" y="448" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#064E3B" text-anchor="middle">
      Country Extractor Utility
    </text>
    <text x="775" y="475" font-family="monospace" font-size="12" fill="#047857" text-anchor="middle">
      (utils/country_extractor.py - Regex &amp; ISO 3166-1 Map)
    </text>
  </g>

  <!-- Node 3: CSV Loader & Writer -->
  <g filter="url(#shadow)">
    <rect x="480" y="560" width="590" height="95" rx="12" fill="url(#greenGrad)" stroke="#059669" stroke-width="2.5"/>
    <text x="775" y="598" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#064E3B" text-anchor="middle">
      CSV Loader &amp; Writer
    </text>
    <text x="775" y="625" font-family="monospace" font-size="12" fill="#047857" text-anchor="middle">
      (utils/csv_loader.py - UTF-8-BOM / Latin-1 Fallbacks)
    </text>
  </g>
  <line x1="775" y1="505" x2="775" y2="560" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Node 4: Storage Cylinder - Local CSV Data Storage -->
  <g filter="url(#shadow)">
    <!-- Cylinder Body -->
    <path d="M 580 750 C 580 730, 970 730, 970 750 L 970 820 C 970 840, 580 840, 580 820 Z"
          fill="#D1FAE5" stroke="#047857" stroke-width="3"/>
    <!-- Cylinder Top -->
    <ellipse cx="775" cy="750" rx="195" ry="18" fill="#A7F3D0" stroke="#047857" stroke-width="3"/>
    <text x="775" y="785" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#064E3B" text-anchor="middle">
      Local CSV Data Storage
    </text>
    <text x="775" y="810" font-family="monospace" font-size="13" font-weight="bold" fill="#047857" text-anchor="middle">
      data/*.csv
    </text>
  </g>
  <line x1="775" y1="655" x2="775" y2="732" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowGreen)"/>

  <!-- Right: Outputs to Layer 6 -->
  <rect x="1140" y="130" width="410" height="780" rx="14" fill="#FAF5FF" stroke="#9333EA" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="1165" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#7C3AED">
    OUTPUTS &rarr; TO LAYER 6 (ANALYSIS ENGINES)
  </text>

  <!-- Output 1: KW Analysis -->
  <g filter="url(#shadow)">
    <rect x="1160" y="260" width="370" height="90" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1345" y="297" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Analysis Service
    </text>
    <text x="1345" y="322" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      (Keyword Analytics Dataset)
    </text>
  </g>

  <!-- Output 2: Country Service -->
  <g filter="url(#shadow)">
    <rect x="1160" y="470" width="370" height="90" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1345" y="507" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Country Service
    </text>
    <text x="1345" y="532" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      (Country &amp; Collaboration Dataset)
    </text>
  </g>

  <!-- Output 3: Embedding Service -->
  <g filter="url(#shadow)">
    <rect x="1160" y="680" width="370" height="90" rx="10" fill="#FFFFFF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1345" y="717" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Embedding Service
    </text>
    <text x="1345" y="742" font-family="monospace" font-size="11" fill="#7C3AED" text-anchor="middle">
      (Full Text for FAISS Vector Index)
    </text>
  </g>

  <!-- Arrows from DATA_STORE to Outputs -->
  <path d="M 970 780 L 1100 780 L 1100 305 L 1160 305" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>
  <path d="M 970 790 L 1080 790 L 1080 515 L 1160 515" fill="none" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>
  <line x1="970" y1="800" x2="1160" y2="725" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>
</svg>
"""

def generate_layer_05():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#ECFDF5')
    ax.set_facecolor('#ECFDF5')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#A7F3D0", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#047857", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 5: DATA CLEANING & ENRICHMENT LAYER",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Green | M.Tech Architecture Specification",
            fontsize=11, color="#D1FAE5", va='center', ha='right')

    # Left Container: Interactions with Layer 4
    in_box = FancyBboxPatch((50, 60), 360, 750, boxstyle="round,pad=8,rounding_size=12",
                            facecolor="#F0FDFA", edgecolor="#0891B2", linewidth=1.5, linestyle="--")
    ax.add_patch(in_box)
    ax.text(75, 785, "INTERACTIONS ↔ WITH LAYER 4", fontsize=11, fontweight='bold', color="#0E7490")

    in1 = FancyBboxPatch((70, 670), 320, 75, boxstyle="round,pad=6,rounding_size=8",
                         facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2, linestyle="--")
    ax.add_patch(in1)
    ax.text(230, 712, "From Layer 4: XML Parser", fontsize=10, fontweight='bold', color="#155E75", ha='center')
    ax.text(230, 690, "(Extracted Raw Paper Records)", fontsize=9, fontfamily='monospace', color="#0E7490", ha='center')

    in2 = FancyBboxPatch((70, 545), 320, 75, boxstyle="round,pad=6,rounding_size=8",
                         facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2, linestyle="--")
    ax.add_patch(in2)
    ax.text(230, 587, "From Layer 4: Affiliation Enricher", fontsize=10, fontweight='bold', color="#155E75", ha='center')
    ax.text(230, 565, "(Fallback Enriched Metadata)", fontsize=9, fontfamily='monospace', color="#0E7490", ha='center')

    out_rerank = FancyBboxPatch((70, 350), 320, 75, boxstyle="round,pad=6,rounding_size=8",
                                facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2, linestyle="--")
    ax.add_patch(out_rerank)
    ax.text(230, 392, "To Layer 4: MedCPT Reranker", fontsize=10, fontweight='bold', color="#155E75", ha='center')
    ax.text(230, 370, "(Deduplicated Records)", fontsize=9, fontfamily='monospace', color="#0E7490", ha='center')

    in_rerank = FancyBboxPatch((70, 210), 320, 75, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#ECFEFF", edgecolor="#0891B2", linewidth=2, linestyle="--")
    ax.add_patch(in_rerank)
    ax.text(230, 252, "From Layer 4: MedCPT Reranker", fontsize=10, fontweight='bold', color="#155E75", ha='center')
    ax.text(230, 230, "(Semantically Ranked Papers)", fontsize=9, fontfamily='monospace', color="#0E7490", ha='center')

    # Center Container: Layer 5 Core
    c_box = FancyBboxPatch((440, 60), 670, 750, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#ECFDF5", edgecolor="#059669", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(465, 785, "5. DATA CLEANING & ENRICHMENT (Internal Architecture)",
            fontsize=12, fontweight='bold', color="#047857")

    # 1. Deduplication Engine
    dedup = FancyBboxPatch((480, 630), 590, 85, boxstyle="round,pad=8,rounding_size=10",
                           facecolor="#D1FAE5", edgecolor="#059669", linewidth=3)
    ax.add_patch(dedup)
    ax.text(775, 680, "Deduplication Engine", fontsize=15, fontweight='bold', color="#064E3B", ha='center')
    ax.text(775, 652, "(Deduplicate by PMID, DOI, and Title Key Matching)", fontsize=11, color="#047857", ha='center')

    ax.annotate('', xy=(480, 680), xytext=(390, 707),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))
    ax.annotate('', xy=(480, 665), xytext=(390, 582),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))

    # Send to Reranker
    ax.annotate('', xy=(390, 387), xytext=(775, 630),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2, mutation_scale=12))
    ax.text(520, 500, "Send to MedCPT Reranker", fontsize=9, fontweight='bold', color="#0891B2")

    # 2. Country Extractor Utility
    c_ext = FancyBboxPatch((480, 460), 590, 85, boxstyle="round,pad=8,rounding_size=10",
                           facecolor="#ECFDF5", edgecolor="#059669", linewidth=2.5)
    ax.add_patch(c_ext)
    ax.text(775, 510, "Country Extractor Utility", fontsize=14, fontweight='bold', color="#064E3B", ha='center')
    ax.text(775, 482, "(utils/country_extractor.py - Regex & ISO 3166-1 Map)", fontsize=10, fontfamily='monospace', color="#047857", ha='center')

    ax.annotate('', xy=(480, 502), xytext=(390, 247),
                arrowprops=dict(arrowstyle="->", color="#0891B2", lw=2, mutation_scale=12))

    # 3. CSV Loader & Writer
    c_load = FancyBboxPatch((480, 310), 590, 85, boxstyle="round,pad=8,rounding_size=10",
                            facecolor="#ECFDF5", edgecolor="#059669", linewidth=2.5)
    ax.add_patch(c_load)
    ax.text(775, 360, "CSV Loader & Writer", fontsize=14, fontweight='bold', color="#064E3B", ha='center')
    ax.text(775, 332, "(utils/csv_loader.py - UTF-8-BOM / Latin-1 Fallbacks)", fontsize=10, fontfamily='monospace', color="#047857", ha='center')

    ax.annotate('', xy=(775, 395), xytext=(775, 460),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2, mutation_scale=12))

    # 4. Storage Cylinder: Local CSV Data Storage
    cyl = FancyBboxPatch((580, 110), 390, 130, boxstyle="round,pad=10,rounding_size=20",
                         facecolor="#D1FAE5", edgecolor="#047857", linewidth=3)
    ax.add_patch(cyl)
    ax.text(775, 185, "Local CSV Data Storage", fontsize=15, fontweight='bold', color="#064E3B", ha='center')
    ax.text(775, 155, "data/*.csv", fontsize=13, fontfamily='monospace', fontweight='bold', color="#047857", ha='center')

    ax.annotate('', xy=(775, 240), xytext=(775, 310),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=2.5, mutation_scale=12))

    # Right Container: Outputs to Layer 6
    out_box = FancyBboxPatch((1140, 60), 410, 750, boxstyle="round,pad=8,rounding_size=12",
                             facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=1.5, linestyle="--")
    ax.add_patch(out_box)
    ax.text(1165, 785, "OUTPUTS → TO LAYER 6 (ANALYSIS)", fontsize=11, fontweight='bold', color="#7C3AED")

    out1 = FancyBboxPatch((1160, 600), 370, 80, boxstyle="round,pad=6,rounding_size=8",
                          facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(out1)
    ax.text(1345, 647, "To Layer 6: Analysis Service", fontsize=11, fontweight='bold', color="#581C87", ha='center')
    ax.text(1345, 622, "(Keyword Analytics Dataset)", fontsize=9, fontfamily='monospace', color="#7C3AED", ha='center')

    out2 = FancyBboxPatch((1160, 410), 370, 80, boxstyle="round,pad=6,rounding_size=8",
                          facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(out2)
    ax.text(1345, 457, "To Layer 6: Country Service", fontsize=11, fontweight='bold', color="#581C87", ha='center')
    ax.text(1345, 432, "(Country & Collab Dataset)", fontsize=9, fontfamily='monospace', color="#7C3AED", ha='center')

    out3 = FancyBboxPatch((1160, 220), 370, 80, boxstyle="round,pad=6,rounding_size=8",
                          facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(out3)
    ax.text(1345, 267, "To Layer 6: Embedding Service", fontsize=11, fontweight='bold', color="#581C87", ha='center')
    ax.text(1345, 242, "(Full Text for FAISS Index)", fontsize=9, fontfamily='monospace', color="#7C3AED", ha='center')

    # Arrows to L6 outputs
    ax.annotate('', xy=(1160, 640), xytext=(970, 190),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))
    ax.annotate('', xy=(1160, 450), xytext=(970, 175),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))
    ax.annotate('', xy=(1160, 260), xytext=(970, 160),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=2, mutation_scale=12))

    save_all_formats("layer_05_data_cleaning", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_05()
