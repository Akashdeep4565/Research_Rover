"""
scripts/render_layer_06.py
Layer 6: Analysis & Computation Layer (Purple)
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
    %% LAYER 6: ANALYSIS & COMPUTATION ENGINES (PURPLE)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef purpleNode fill:#FAF5FF,stroke:#9333EA,stroke-width:2.5px,color:#581C87,font-size:14px;
    classDef phaseNode fill:#F3E8FF,stroke:#7E22CE,stroke-width:2.5px,color:#4C1D95,font-weight:bold,font-size:14px;
    classDef storageNode fill:#EDE9FE,stroke:#6B21A8,stroke-width:3px,color:#3B0764,font-weight:bold,font-size:15px;
    classDef apiNode fill:#E9D5FF,stroke:#581C87,stroke-width:2.5px,color:#3B0764,font-weight:bold,font-size:14px;
    classDef boundaryInL3 fill:#FFF7ED,stroke:#EA580C,stroke-width:2px,stroke-dasharray: 5 5,color:#9A3412,font-size:13px;
    classDef boundaryInL5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,stroke-dasharray: 5 5,color:#064E3B,font-size:13px;
    classDef boundaryOutL7 fill:#FFF1F2,stroke:#E11D48,stroke-width:2px,stroke-dasharray: 5 5,color:#9F1239,font-size:13px;

    subgraph IN_DATA["INPUTS FROM PREVIOUS LAYERS"]
        IN_L3_REQ[["From Layer 3: Validated Analysis Triggers<br/>(Keyword / Country / Embed / Chat)"]]:::boundaryInL3
        IN_L5_CSV[("From Layer 5: Local CSV Storage<br/>(data/*.csv)")]:::boundaryInL5
    end

    subgraph L6_CORE["LAYER 6: ANALYSIS & COMPUTATION ENGINES"]
        subgraph PIPELINE_KW["Keyword Analysis Pipeline"]
            SRV_KW["Analysis Service<br/>(services/analysis_service.py)"]:::purpleNode
            KW_FREQ["Phase 1: Keyword Frequency & Percentage"]:::phaseNode
            KW_GRAPH["Phase 2: Co-Occurrence Graph & Matrix"]:::phaseNode
            KW_CENTRALITY["Phase 3: NetworkX Centralities<br/>(Degree, Closeness, Betweenness, Eigenvector, Clustering)"]:::phaseNode
            KW_PRESENCE["Phase 4: Binary Keyword Presence Matrix"]:::phaseNode
            KW_CACHE[("Cached Summary Artifacts<br/>data/*_summary.json")]:::storageNode
        end

        subgraph PIPELINE_CTRY["Country & Collaboration Pipeline"]
            SRV_CTRY["Country Service<br/>(services/country_service.py)"]:::purpleNode
            CTRY_STATS["Country Publication Frequency & Coverage %"]:::phaseNode
            CTRY_GRAPH["International Co-Authorship Graph<br/>(Nodes & Weighted Collaboration Links)"]:::phaseNode
        end

        subgraph PIPELINE_RAG["Vector Embeddings & RAG Chat Pipeline"]
            SRV_EMBED["Embedding & Vector Service<br/>(services/embedding_service.py)"]:::purpleNode
            FAISS_STORE[("FAISS Vector Index<br/>data/*.index & *.pkl")]:::storageNode
            SRV_CHAT["RAG Chat Service<br/>(services/chat_service.py)"]:::purpleNode
            LLM_API["LLM Provider API<br/>(OpenAI / DeepSeek / Groq)"]:::apiNode
        end
    end

    subgraph OUT_L7["OUTPUTS TO LAYER 7 (VISUALIZATION)"]
        OUT_L7_KW_CACHE[["To Layer 7: Error Boundaries<br/>(Cached Summary JSON)"]]:::boundaryOutL7
        OUT_L7_CTRY_STATS[["To Layer 7: Error Boundaries<br/>(Country Publication Stats)"]]:::boundaryOutL7
        OUT_L7_CTRY_GRAPH[["To Layer 7: Error Boundaries<br/>(Co-Authorship Graph)"]]:::boundaryOutL7
        OUT_L7_RAG_STREAM[["To Layer 7: Interactive RAG Stream<br/>(AI Responses & Citations)"]]:::boundaryOutL7
    end

    %% Wiring Inputs
    IN_L3_REQ --> SRV_KW & SRV_CTRY & SRV_EMBED & SRV_CHAT
    IN_L5_CSV --> SRV_KW & SRV_CTRY & SRV_EMBED

    %% Keyword Pipeline Flow
    SRV_KW --> KW_FREQ --> KW_GRAPH --> KW_CENTRALITY --> KW_PRESENCE --> KW_CACHE --> OUT_L7_KW_CACHE

    %% Country Pipeline Flow
    SRV_CTRY --> CTRY_STATS --> OUT_L7_CTRY_STATS
    SRV_CTRY --> CTRY_GRAPH --> OUT_L7_CTRY_GRAPH

    %% RAG Pipeline Flow
    SRV_EMBED --> FAISS_STORE
    FAISS_STORE --> SRV_CHAT
    SRV_CHAT <-->|Query & Context Stream| LLM_API
    SRV_CHAT --> OUT_L7_RAG_STREAM
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FAF5FF"/>
      <stop offset="100%" stop-color="#F3E8FF"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7E22CE"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#9333EA"/>
    </marker>
    <marker id="arrowPink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#E11D48"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#FAF5FF"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 6: ANALYSIS &amp; COMPUTATION ENGINES
  </text>
  <text x="1060" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#F3E8FF">
    Color Theme: Purple | Scope: NetworkX Centralities, Country Graphs &amp; FAISS RAG
  </text>

  <!-- Top Inputs: Boundary from L3 & L5 -->
  <g filter="url(#shadow)">
    <rect x="50" y="130" width="700" height="70" rx="10" fill="#FFF7ED" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="400" y="160" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      From Layer 3: Validated Analysis Triggers
    </text>
    <text x="400" y="182" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (Keyword Generation, Country Aggregation, Embedding Vectorization, Chat Queries)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="800" y="130" width="750" height="70" rx="10" fill="#ECFDF5" stroke="#059669" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1175" y="160" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#065F46" text-anchor="middle">
      From Layer 5: Local CSV Data Storage
    </text>
    <text x="1175" y="182" font-family="monospace" font-size="11" fill="#047857" text-anchor="middle">
      data/*.csv (Cleaned &amp; Normalized Publications Dataset)
    </text>
  </g>

  <!-- Core Layer 6 Subgraph -->
  <rect x="50" y="220" width="1120" height="700" rx="14" fill="#FAF5FF" stroke="#9333EA" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="80" y="250" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#7E22CE">
    6. ANALYSIS &amp; COMPUTATION ENGINES (Internal Architecture)
  </text>

  <!-- PIPELINE 1: KEYWORDS (Left side of Layer 6) -->
  <rect x="70" y="270" width="480" height="630" rx="12" fill="#FFFFFF" stroke="#9333EA" stroke-width="2"/>
  <text x="90" y="295" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8">
    PIPELINE A: KEYWORD ANALYTICS (analysis_service.py)
  </text>

  <!-- Service Node -->
  <g filter="url(#shadow)">
    <rect x="90" y="310" width="440" height="55" rx="8" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2"/>
    <text x="310" y="342" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#581C87" text-anchor="middle">
      Analysis Service (services/analysis_service.py)
    </text>
  </g>

  <!-- Phase 1 -->
  <g filter="url(#shadow)">
    <rect x="90" y="385" width="440" height="50" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="310" y="415" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      Phase 1: Keyword Frequency &amp; Percentage
    </text>
  </g>
  <line x1="310" y1="365" x2="310" y2="385" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Phase 2 -->
  <g filter="url(#shadow)">
    <rect x="90" y="455" width="440" height="50" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="310" y="485" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      Phase 2: Co-Occurrence Graph &amp; Matrix
    </text>
  </g>
  <line x1="310" y1="435" x2="310" y2="455" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Phase 3 -->
  <g filter="url(#shadow)">
    <rect x="90" y="525" width="440" height="60" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="310" y="550" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      Phase 3: NetworkX Centralities
    </text>
    <text x="310" y="570" font-family="system-ui, sans-serif" font-size="10" fill="#6B21A8" text-anchor="middle">
      (Degree, Closeness, Betweenness, Eigenvector, Clustering)
    </text>
  </g>
  <line x1="310" y1="505" x2="310" y2="525" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Phase 4 -->
  <g filter="url(#shadow)">
    <rect x="90" y="605" width="440" height="50" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="310" y="635" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      Phase 4: Binary Keyword Presence Matrix
    </text>
  </g>
  <line x1="310" y1="585" x2="310" y2="605" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Cylinder: Cached Summary Artifacts -->
  <g filter="url(#shadow)">
    <path d="M 120 705 C 120 690, 500 690, 500 705 L 500 755 C 500 770, 120 770, 120 755 Z"
          fill="#EDE9FE" stroke="#6B21A8" stroke-width="2.5"/>
    <ellipse cx="310" cy="705" rx="190" ry="14" fill="#DDD6FE" stroke="#6B21A8" stroke-width="2.5"/>
    <text x="310" y="735" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#3B0764" text-anchor="middle">
      Cached Summary Artifacts
    </text>
    <text x="310" y="755" font-family="monospace" font-size="11" fill="#581C87" text-anchor="middle">
      data/*_summary.json
    </text>
  </g>
  <line x1="310" y1="655" x2="310" y2="695" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- PIPELINE 2: COUNTRY (Center right top) -->
  <rect x="580" y="270" width="560" height="270" rx="12" fill="#FFFFFF" stroke="#9333EA" stroke-width="2"/>
  <text x="600" y="295" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8">
    PIPELINE B: COUNTRY &amp; COLLABORATION (country_service.py)
  </text>

  <!-- Service Node -->
  <g filter="url(#shadow)">
    <rect x="600" y="310" width="520" height="55" rx="8" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2"/>
    <text x="860" y="342" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#581C87" text-anchor="middle">
      Country Service (services/country_service.py)
    </text>
  </g>

  <!-- Country Stats -->
  <g filter="url(#shadow)">
    <rect x="600" y="385" width="520" height="60" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="860" y="415" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      Country Publication Frequency &amp; Coverage %
    </text>
    <text x="860" y="435" font-family="system-ui, sans-serif" font-size="10" fill="#6B21A8" text-anchor="middle">
      (Aggregates frequency distribution and global research coverage)
    </text>
  </g>
  <line x1="860" y1="365" x2="860" y2="385" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Country Graph -->
  <g filter="url(#shadow)">
    <rect x="600" y="465" width="520" height="60" rx="8" fill="#F3E8FF" stroke="#7E22CE" stroke-width="1.5"/>
    <text x="860" y="495" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      International Co-Authorship Graph
    </text>
    <text x="860" y="515" font-family="system-ui, sans-serif" font-size="10" fill="#6B21A8" text-anchor="middle">
      (Nodes &amp; Weighted Collaboration Links)
    </text>
  </g>
  <path d="M 600 340 L 570 340 L 570 495 L 600 495" fill="none" stroke="#9333EA" stroke-width="1.5" marker-end="url(#arrowPurple)"/>

  <!-- PIPELINE 3: RAG & LLM (Center right bottom) -->
  <rect x="580" y="560" width="560" height="340" rx="12" fill="#FFFFFF" stroke="#9333EA" stroke-width="2"/>
  <text x="600" y="585" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8">
    PIPELINE C: VECTOR EMBEDDINGS &amp; RAG CHAT
  </text>

  <!-- Embedding Service -->
  <g filter="url(#shadow)">
    <rect x="600" y="600" width="250" height="55" rx="8" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2"/>
    <text x="725" y="625" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#581C87" text-anchor="middle">
      Embedding Service
    </text>
    <text x="725" y="643" font-family="monospace" font-size="10" fill="#7C3AED" text-anchor="middle">
      (embedding_service.py)
    </text>
  </g>

  <!-- FAISS Index Cylinder -->
  <g filter="url(#shadow)">
    <path d="M 610 685 C 610 675, 840 675, 840 685 L 840 730 C 840 740, 610 740, 610 730 Z"
          fill="#EDE9FE" stroke="#6B21A8" stroke-width="2"/>
    <ellipse cx="725" cy="685" rx="115" ry="10" fill="#DDD6FE" stroke="#6B21A8" stroke-width="2"/>
    <text x="725" y="708" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#3B0764" text-anchor="middle">
      FAISS Vector Index
    </text>
    <text x="725" y="725" font-family="monospace" font-size="9" fill="#581C87" text-anchor="middle">
      data/*.index &amp; *.pkl
    </text>
  </g>
  <line x1="725" y1="655" x2="725" y2="675" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- Chat Service -->
  <g filter="url(#shadow)">
    <rect x="880" y="600" width="240" height="135" rx="10" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2"/>
    <text x="1000" y="635" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      RAG Chat Service
    </text>
    <text x="1000" y="655" font-family="monospace" font-size="10" fill="#7C3AED" text-anchor="middle">
      (chat_service.py)
    </text>
    <text x="1000" y="690" font-family="system-ui, sans-serif" font-size="10" fill="#6B21A8" text-anchor="middle">
      Decomposes query,
    </text>
    <text x="1000" y="710" font-family="system-ui, sans-serif" font-size="10" fill="#6B21A8" text-anchor="middle">
      retrieves vectors &amp; formats prompt
    </text>
  </g>
  <line x1="840" y1="705" x2="880" y2="705" stroke="#9333EA" stroke-width="2" marker-end="url(#arrowPurple)"/>

  <!-- External LLM Provider Box -->
  <g filter="url(#shadow)">
    <rect x="600" y="775" width="520" height="110" rx="10" fill="#E9D5FF" stroke="#581C87" stroke-width="2.5"/>
    <text x="860" y="810" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#3B0764" text-anchor="middle">
      LLM Provider API
    </text>
    <text x="860" y="835" font-family="monospace" font-size="12" fill="#581C87" text-anchor="middle">
      (OpenAI / DeepSeek / Groq)
    </text>
    <text x="860" y="860" font-family="system-ui, sans-serif" font-size="11" fill="#4C1D95" text-anchor="middle">
      Generates scientific synthesis with citations
    </text>
  </g>
  <line x1="1000" y1="735" x2="1000" y2="775" stroke="#581C87" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
  <line x1="970" y1="775" x2="970" y2="735" stroke="#581C87" stroke-width="2.5" marker-end="url(#arrowPurple)"/>

  <!-- Right: Outputs to Layer 7 -->
  <rect x="1190" y="220" width="360" height="700" rx="14" fill="#FFF1F2" stroke="#E11D48" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="1210" y="250" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#BE123C">
    OUTPUTS &rarr; TO LAYER 7 (VISUALIZATION)
  </text>

  <!-- Output 1: KW Summary -->
  <g filter="url(#shadow)">
    <rect x="1210" y="320" width="320" height="85" rx="10" fill="#FFFFFF" stroke="#E11D48" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1370" y="355" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#9F1239" text-anchor="middle">
      To Layer 7: Error Boundaries
    </text>
    <text x="1370" y="378" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      data/*_summary.json (KW Artifacts)
    </text>
  </g>
  <path d="M 500 735 L 550 735 L 550 890 L 1160 890 L 1160 362 L 1210 362" fill="none" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- Output 2: Country Stats -->
  <g filter="url(#shadow)">
    <rect x="1210" y="445" width="320" height="85" rx="10" fill="#FFFFFF" stroke="#E11D48" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1370" y="480" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#9F1239" text-anchor="middle">
      To Layer 7: Error Boundaries
    </text>
    <text x="1370" y="503" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (Country Coverage % &amp; Tables)
    </text>
  </g>
  <line x1="1120" y1="415" x2="1210" y2="475" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- Output 3: Country Graph -->
  <g filter="url(#shadow)">
    <rect x="1210" y="570" width="320" height="85" rx="10" fill="#FFFFFF" stroke="#E11D48" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1370" y="605" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#9F1239" text-anchor="middle">
      To Layer 7: Error Boundaries
    </text>
    <text x="1370" y="628" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (2D / 3D Force Graph Topology)
    </text>
  </g>
  <line x1="1120" y1="495" x2="1210" y2="612" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>

  <!-- Output 4: RAG Stream -->
  <g filter="url(#shadow)">
    <rect x="1210" y="695" width="320" height="85" rx="10" fill="#FFFFFF" stroke="#E11D48" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1370" y="730" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#9F1239" text-anchor="middle">
      To Layer 7: Interactive RAG Stream
    </text>
    <text x="1370" y="753" font-family="monospace" font-size="11" fill="#BE123C" text-anchor="middle">
      (Conversational Stream &amp; Citations)
    </text>
  </g>
  <path d="M 1120 667 L 1160 667 L 1160 737 L 1210 737" fill="none" stroke="#E11D48" stroke-width="2" marker-end="url(#arrowPink)"/>
</svg>
"""

def generate_layer_06():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#FAF5FF')
    ax.set_facecolor('#FAF5FF')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#E9D5FF", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#7E22CE", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 6: ANALYSIS & COMPUTATION ENGINES",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Purple | M.Tech Architecture Specification",
            fontsize=11, color="#F3E8FF", va='center', ha='right')

    # Top Inputs from L3 & L5
    in_l3 = FancyBboxPatch((50, 750), 700, 65, boxstyle="round,pad=6,rounding_size=8",
                           facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=2, linestyle="--")
    ax.add_patch(in_l3)
    ax.text(400, 792, "From Layer 3: Validated Analysis Triggers", fontsize=11, fontweight='bold', color="#9A3412", ha='center')
    ax.text(400, 770, "(Keyword Generation, Country Aggregation, Embeddings, Chat Queries)", fontsize=9, fontfamily='monospace', color="#C2410C", ha='center')

    in_l5 = FancyBboxPatch((800, 750), 750, 65, boxstyle="round,pad=6,rounding_size=8",
                           facecolor="#ECFDF5", edgecolor="#059669", linewidth=2, linestyle="--")
    ax.add_patch(in_l5)
    ax.text(1175, 792, "From Layer 5: Local CSV Data Storage", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(1175, 770, "data/*.csv (Cleaned & Normalized Publications Dataset)", fontsize=9, fontfamily='monospace', color="#047857", ha='center')

    # Core Container: Layer 6
    c_box = FancyBboxPatch((50, 40), 1120, 680, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(80, 690, "6. ANALYSIS & COMPUTATION ENGINES (Internal Architecture)",
            fontsize=12, fontweight='bold', color="#7E22CE")

    # Pipeline A: Keyword Analytics
    p_kw = FancyBboxPatch((70, 60), 480, 610, boxstyle="round,pad=6,rounding_size=10",
                          facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(p_kw)
    ax.text(90, 645, "PIPELINE A: KEYWORDS (analysis_service.py)", fontsize=10, fontweight='bold', color="#6B21A8")

    # KW Service
    srv_kw = FancyBboxPatch((90, 570), 440, 50, boxstyle="round,pad=6,rounding_size=8",
                            facecolor="#F3E8FF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(srv_kw)
    ax.text(310, 595, "Analysis Service (services/analysis_service.py)", fontsize=11, fontweight='bold', color="#581C87", ha='center')

    # KW Phases 1-4
    phases = [
        ("Phase 1: Keyword Frequency & Percentage", 500),
        ("Phase 2: Co-Occurrence Graph & Matrix", 430),
        ("Phase 3: NetworkX Centralities (5 metrics)", 360),
        ("Phase 4: Binary Keyword Presence Matrix", 290),
    ]

    for title, y in phases:
        box = FancyBboxPatch((90, y), 440, 45, boxstyle="round,pad=6,rounding_size=6",
                             facecolor="#FAF5FF", edgecolor="#7E22CE", linewidth=1.5)
        ax.add_patch(box)
        ax.text(310, y + 22, title, fontsize=10, fontweight='bold', color="#4C1D95", ha='center')

    # KW Cache Cylinder
    cyl = FancyBboxPatch((120, 110), 380, 130, boxstyle="round,pad=8,rounding_size=15",
                         facecolor="#EDE9FE", edgecolor="#6B21A8", linewidth=2.5)
    ax.add_patch(cyl)
    ax.text(310, 185, "Cached Summary Artifacts", fontsize=12, fontweight='bold', color="#3B0764", ha='center')
    ax.text(310, 155, "data/*_summary.json", fontsize=10, fontfamily='monospace', color="#581C87", ha='center')

    # Arrows between KW phases
    for y in [570, 500, 430, 360, 290]:
        ax.annotate('', xy=(310, y - 25), xytext=(310, y),
                    arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.5, mutation_scale=10))

    # Pipeline B: Country & Collab
    p_ctry = FancyBboxPatch((580, 410), 560, 260, boxstyle="round,pad=6,rounding_size=10",
                            facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(p_ctry)
    ax.text(600, 645, "PIPELINE B: COUNTRY & COLLABORATION (country_service.py)", fontsize=10, fontweight='bold', color="#6B21A8")

    srv_ctry = FancyBboxPatch((600, 570), 520, 50, boxstyle="round,pad=6,rounding_size=8",
                              facecolor="#F3E8FF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(srv_ctry)
    ax.text(860, 595, "Country Service (services/country_service.py)", fontsize=12, fontweight='bold', color="#581C87", ha='center')

    c_stats = FancyBboxPatch((600, 495), 520, 50, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#FAF5FF", edgecolor="#7E22CE", linewidth=1.5)
    ax.add_patch(c_stats)
    ax.text(860, 520, "Country Publication Frequency & Coverage %", fontsize=11, fontweight='bold', color="#4C1D95", ha='center')

    c_graph = FancyBboxPatch((600, 425), 520, 50, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#FAF5FF", edgecolor="#7E22CE", linewidth=1.5)
    ax.add_patch(c_graph)
    ax.text(860, 450, "International Co-Authorship Graph (Nodes & Links)", fontsize=11, fontweight='bold', color="#4C1D95", ha='center')

    ax.annotate('', xy=(860, 545), xytext=(860, 570),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(860, 475), xytext=(860, 495),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.5, mutation_scale=10))

    # Pipeline C: Vector & RAG Chat
    p_rag = FancyBboxPatch((580, 60), 560, 320, boxstyle="round,pad=6,rounding_size=10",
                           facecolor="#FFFFFF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(p_rag)
    ax.text(600, 355, "PIPELINE C: VECTOR EMBEDDINGS & RAG CHAT", fontsize=10, fontweight='bold', color="#6B21A8")

    srv_embed = FancyBboxPatch((600, 280), 240, 50, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#F3E8FF", edgecolor="#9333EA", linewidth=1.5)
    ax.add_patch(srv_embed)
    ax.text(720, 305, "Embedding Service", fontsize=10, fontweight='bold', color="#581C87", ha='center')

    faiss_cyl = FancyBboxPatch((600, 195), 240, 65, boxstyle="round,pad=6,rounding_size=10",
                               facecolor="#EDE9FE", edgecolor="#6B21A8", linewidth=2)
    ax.add_patch(faiss_cyl)
    ax.text(720, 235, "FAISS Vector Index", fontsize=10, fontweight='bold', color="#3B0764", ha='center')
    ax.text(720, 215, "data/*.index & *.pkl", fontsize=8, fontfamily='monospace', color="#581C87", ha='center')

    ax.annotate('', xy=(720, 260), xytext=(720, 280),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.5, mutation_scale=10))

    srv_chat = FancyBboxPatch((870, 205), 250, 125, boxstyle="round,pad=6,rounding_size=8",
                              facecolor="#F3E8FF", edgecolor="#9333EA", linewidth=2)
    ax.add_patch(srv_chat)
    ax.text(995, 290, "RAG Chat Service", fontsize=11, fontweight='bold', color="#581C87", ha='center')
    ax.text(995, 270, "(chat_service.py)", fontsize=9, fontfamily='monospace', color="#7C3AED", ha='center')
    ax.text(995, 240, "Query decomposition & RAG", fontsize=9, color="#6B21A8", ha='center')

    ax.annotate('', xy=(870, 230), xytext=(840, 230),
                arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.5, mutation_scale=10))

    llm_api = FancyBboxPatch((600, 80), 520, 85, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#E9D5FF", edgecolor="#581C87", linewidth=2.5)
    ax.add_patch(llm_api)
    ax.text(860, 135, "LLM Provider API (OpenAI / DeepSeek / Groq)", fontsize=11, fontweight='bold', color="#3B0764", ha='center')
    ax.text(860, 105, "Generates scientific synthesis with citations", fontsize=9, color="#4C1D95", ha='center')

    ax.annotate('', xy=(995, 165), xytext=(995, 205),
                arrowprops=dict(arrowstyle="<->", color="#581C87", lw=2, mutation_scale=12))

    # Right Container: Outputs to Layer 7
    out_box = FancyBboxPatch((1190, 40), 360, 680, boxstyle="round,pad=8,rounding_size=12",
                             facecolor="#FFF1F2", edgecolor="#E11D48", linewidth=1.5, linestyle="--")
    ax.add_patch(out_box)
    ax.text(1210, 690, "OUTPUTS → TO LAYER 7 (VISUALIZATION)", fontsize=10, fontweight='bold', color="#BE123C")

    outputs = [
        ("To Layer 7: Error Boundaries", "data/*_summary.json (KW Artifacts)", 560),
        ("To Layer 7: Error Boundaries", "(Country Coverage % & Tables)", 430),
        ("To Layer 7: Error Boundaries", "(2D / 3D Force Graph Topology)", 300),
        ("To Layer 7: Interactive RAG", "(Conversational Stream & Citations)", 170),
    ]

    for title, desc, y in outputs:
        o_box = FancyBboxPatch((1210, y), 320, 75, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#FFFFFF", edgecolor="#E11D48", linewidth=2, linestyle="--")
        ax.add_patch(o_box)
        ax.text(1370, y + 45, title, fontsize=10, fontweight='bold', color="#9F1239", ha='center')
        ax.text(1370, y + 20, desc, fontsize=8, fontfamily='monospace', color="#BE123C", ha='center')

    # Arrows to outputs
    ax.annotate('', xy=(1210, 597), xytext=(500, 175),
                arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(1210, 467), xytext=(1120, 520),
                arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(1210, 337), xytext=(1120, 450),
                arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(1210, 207), xytext=(1120, 240),
                arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5, mutation_scale=10))

    save_all_formats("layer_06_analysis_computation", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_06()
