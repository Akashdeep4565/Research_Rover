"""
scripts/render_layer_03.py
Layer 3: Backend Routing & Controller Layer (Orange)
Exact architecture extracted from reference.
"""

import os
from pathlib import Path
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Users/AkashDeep/AppData/Local/Temp")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon

from layer_helpers import save_all_formats

MMD_CONTENT = """flowchart TD
    %% =========================================================================
    %% LAYER 3: BACKEND ROUTING & CONTROLLER LAYER (ORANGE)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef orangeNode fill:#FFF7ED,stroke:#EA580C,stroke-width:2.5px,color:#9A3412,font-size:14px;
    classDef decisionNode fill:#FFEDD5,stroke:#C2410C,stroke-width:3px,color:#7C2D12,font-weight:bold,font-size:14px;
    classDef errorNode fill:#FEF2F2,stroke:#DC2626,stroke-width:2.5px,color:#991B1B,font-weight:bold,font-size:14px;
    classDef boundaryIn fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,stroke-dasharray: 5 5,color:#1E3A8A,font-size:13px;
    classDef boundaryOutL4 fill:#ECFEFF,stroke:#0891B2,stroke-width:2px,stroke-dasharray: 5 5,color:#155E75,font-size:13px;
    classDef boundaryOutL6 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,stroke-dasharray: 5 5,color:#581C87,font-size:13px;
    classDef boundaryOutErr fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,stroke-dasharray: 5 5,color:#991B1B,font-size:13px;

    subgraph IN_L2["INPUTS FROM LAYER 2 (API CLIENT)"]
        IN_L2_SEARCH[["From Layer 2: POST /api/v1/search/query"]]:::boundaryIn
        IN_L2_FILES[["From Layer 2: GET/POST /api/v1/files/*"]]:::boundaryIn
        IN_L2_ANALYSIS[["From Layer 2: GET/POST /api/v1/analysis/*"]]:::boundaryIn
        IN_L2_CHAT[["From Layer 2: POST /api/v1/chat/* & embeddings/*"]]:::boundaryIn
    end

    subgraph L3_CORE["LAYER 3: BACKEND ROUTING & CONTROLLER LAYER"]
        ROUTE_SEARCH["Search Controller<br/>(api/routes/search.py)"]:::orangeNode
        ROUTE_FILES["Files Controller<br/>(api/routes/files.py)"]:::orangeNode
        ROUTE_ANALYSIS["Analysis Controller<br/>(api/routes/analysis.py)"]:::orangeNode
        ROUTE_CHAT["Chat & Embedding Controller<br/>(api/routes/chat.py & embeddings.py)"]:::orangeNode
        
        VALIDATE{"Request Validation<br/>(models/schemas.py Pydantic)"}:::decisionNode
        ERR_VALIDATION["Return HTTP 400 / 404 / 500<br/>Error Payload"]:::errorNode
    end

    OUT_L2_ERR[["To Layer 2: Axios Client (Error Payload)"]]:::boundaryOutErr

    subgraph OUT_L4_L6["OUTPUTS TO SERVICES (LAYERS 4 & 6)"]
        OUT_L4_SEARCH[["To Layer 4: Search Service Orchestrator<br/>(services/search_service.py)"]]:::boundaryOutL4
        OUT_L6_KW[["To Layer 6: Analysis Service<br/>(services/analysis_service.py)"]]:::boundaryOutL6
        OUT_L6_CTRY[["To Layer 6: Country Service<br/>(services/country_service.py)"]]:::boundaryOutL6
        OUT_L6_EMBED[["To Layer 6: Embedding & Vector Service<br/>(services/embedding_service.py)"]]:::boundaryOutL6
        OUT_L6_CHAT[["To Layer 6: RAG Chat Service<br/>(services/chat_service.py)"]]:::boundaryOutL6
    end

    %% Internal Connections
    IN_L2_SEARCH --> ROUTE_SEARCH
    IN_L2_FILES --> ROUTE_FILES
    IN_L2_ANALYSIS --> ROUTE_ANALYSIS
    IN_L2_CHAT --> ROUTE_CHAT

    ROUTE_SEARCH --> VALIDATE
    ROUTE_FILES --> VALIDATE
    ROUTE_ANALYSIS --> VALIDATE
    ROUTE_CHAT --> VALIDATE

    VALIDATE -->|Invalid Request| ERR_VALIDATION --> OUT_L2_ERR
    
    VALIDATE -->|Valid: Search| OUT_L4_SEARCH
    VALIDATE -->|Valid: Keyword Analysis| OUT_L6_KW
    VALIDATE -->|Valid: Country Analysis| OUT_L6_CTRY
    VALIDATE -->|Valid: Embeddings| OUT_L6_EMBED
    VALIDATE -->|Valid: Chat Query| OUT_L6_CHAT
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF7ED"/>
      <stop offset="100%" stop-color="#FFEDD5"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C2410C"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#EA580C"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#DC2626"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16A34A"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#FFF7ED"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#FED7AA" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 3: BACKEND ROUTING &amp; CONTROLLER LAYER
  </text>
  <text x="1050" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#FFEDD5">
    Color Theme: Orange | Scope: FastAPI Endpoints &amp; Schema Validation
  </text>

  <!-- Left: Inputs from Layer 2 -->
  <rect x="50" y="130" width="310" height="780" rx="14" fill="#F8FAFC" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="75" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1D4ED8">
    INPUTS &larr; FROM LAYER 2
  </text>

  <g filter="url(#shadow)">
    <rect x="65" y="200" width="280" height="75" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="205" y="232" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      From Layer 2: Search Request
    </text>
    <text x="205" y="255" font-family="monospace" font-size="11" fill="#2563EB" text-anchor="middle">
      POST /api/v1/search/query
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="65" y="340" width="280" height="75" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="205" y="372" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      From Layer 2: File Operations
    </text>
    <text x="205" y="395" font-family="monospace" font-size="11" fill="#2563EB" text-anchor="middle">
      GET/POST /api/v1/files/*
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="65" y="480" width="280" height="75" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="205" y="512" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      From Layer 2: Analysis Queries
    </text>
    <text x="205" y="535" font-family="monospace" font-size="11" fill="#2563EB" text-anchor="middle">
      GET/POST /api/v1/analysis/*
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="65" y="620" width="280" height="75" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="205" y="652" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      From Layer 2: Chat &amp; Embeddings
    </text>
    <text x="205" y="675" font-family="monospace" font-size="11" fill="#2563EB" text-anchor="middle">
      POST /api/v1/chat/* &amp; embed/*
    </text>
  </g>

  <!-- Center: Layer 3 Core Container -->
  <rect x="380" y="130" width="700" height="780" rx="14" fill="#FFF7ED" stroke="#EA580C" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="405" y="160" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#C2410C">
    3. BACKEND ROUTING &amp; CONTROLLER LAYER (Internal Architecture)
  </text>

  <!-- 4 Controllers -->
  <g filter="url(#shadow)">
    <rect x="400" y="195" width="290" height="85" rx="10" fill="url(#orangeGrad)" stroke="#EA580C" stroke-width="2.5"/>
    <text x="545" y="232" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#7C2D12" text-anchor="middle">
      Search Controller
    </text>
    <text x="545" y="258" font-family="monospace" font-size="12" fill="#9A3412" text-anchor="middle">
      (api/routes/search.py)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="400" y="335" width="290" height="85" rx="10" fill="url(#orangeGrad)" stroke="#EA580C" stroke-width="2.5"/>
    <text x="545" y="372" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#7C2D12" text-anchor="middle">
      Files Controller
    </text>
    <text x="545" y="398" font-family="monospace" font-size="12" fill="#9A3412" text-anchor="middle">
      (api/routes/files.py)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="400" y="475" width="290" height="85" rx="10" fill="url(#orangeGrad)" stroke="#EA580C" stroke-width="2.5"/>
    <text x="545" y="512" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#7C2D12" text-anchor="middle">
      Analysis Controller
    </text>
    <text x="545" y="538" font-family="monospace" font-size="12" fill="#9A3412" text-anchor="middle">
      (api/routes/analysis.py)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="400" y="615" width="290" height="85" rx="10" fill="url(#orangeGrad)" stroke="#EA580C" stroke-width="2.5"/>
    <text x="545" y="652" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#7C2D12" text-anchor="middle">
      Chat &amp; Embedding Controller
    </text>
    <text x="545" y="678" font-family="monospace" font-size="12" fill="#9A3412" text-anchor="middle">
      (api/routes/chat.py &amp; embeddings.py)
    </text>
  </g>

  <!-- Arrows from Inputs to Controllers -->
  <line x1="345" y1="237" x2="400" y2="237" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <line x1="345" y1="377" x2="400" y2="377" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <line x1="345" y1="517" x2="400" y2="517" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <line x1="345" y1="657" x2="400" y2="657" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>

  <!-- Decision Diamond: Request Validation -->
  <g filter="url(#shadow)">
    <polygon points="850,370 990,450 850,530 710,450" fill="#FFEDD5" stroke="#C2410C" stroke-width="3"/>
    <text x="850" y="442" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#7C2D12" text-anchor="middle">
      Request Validation
    </text>
    <text x="850" y="465" font-family="monospace" font-size="11" fill="#9A3412" text-anchor="middle">
      (models/schemas.py Pydantic)
    </text>
  </g>

  <!-- Arrows from 4 Controllers to Validation Diamond -->
  <path d="M 690 237 L 760 237 L 850 370" fill="none" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <path d="M 690 377 L 730 377 L 760 410" fill="none" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <path d="M 690 517 L 730 517 L 760 490" fill="none" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>
  <path d="M 690 657 L 760 657 L 850 530" fill="none" stroke="#EA580C" stroke-width="2" marker-end="url(#arrowOrange)"/>

  <!-- Validation Decision Branches -->
  <!-- Invalid Branch (Down to Error Node) -->
  <line x1="850" y1="530" x2="850" y2="620" stroke="#DC2626" stroke-width="2.5" marker-end="url(#arrowRed)"/>
  <text x="860" y="580" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#DC2626">
    [Invalid]
  </text>

  <!-- Error Node -->
  <g filter="url(#shadow)">
    <rect x="715" y="625" width="270" height="85" rx="10" fill="#FEF2F2" stroke="#DC2626" stroke-width="2.5"/>
    <text x="850" y="660" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#991B1B" text-anchor="middle">
      Return HTTP 400 / 404 / 500
    </text>
    <text x="850" y="685" font-family="system-ui, sans-serif" font-size="12" fill="#B91C1C" text-anchor="middle">
      Standardized Error Payload
    </text>
  </g>

  <!-- Error to Layer 2 Boundary -->
  <path d="M 715 670 L 400 740 L 205 740 L 205 770" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrowRed)"/>
  
  <g filter="url(#shadow)">
    <rect x="65" y="775" width="280" height="75" rx="10" fill="#FEF2F2" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="205" y="807" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991B1B" text-anchor="middle">
      To Layer 2: Axios API Client
    </text>
    <text x="205" y="830" font-family="system-ui, sans-serif" font-size="11" fill="#B91C1C" text-anchor="middle">
      (Dispatch Error &amp; Toast)
    </text>
  </g>

  <!-- Valid Branches to Right: Outputs to Layer 4 & Layer 6 -->
  <rect x="1100" y="130" width="450" height="780" rx="14" fill="#F8FAFC" stroke="#0891B2" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="1125" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#0E7490">
    VALIDATED OUTPUTS &rarr; TO SERVICES (LAYERS 4 &amp; 6)
  </text>

  <!-- Valid Arrow Label -->
  <text x="1010" y="440" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#16A34A">
    [Valid Request]
  </text>

  <!-- Output 1: Search to Layer 4 -->
  <g filter="url(#shadow)">
    <rect x="1120" y="195" width="410" height="85" rx="10" fill="#ECFEFF" stroke="#0891B2" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1325" y="230" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#155E75" text-anchor="middle">
      To Layer 4: Search Service Orchestrator
    </text>
    <text x="1325" y="255" font-family="monospace" font-size="12" fill="#0E7490" text-anchor="middle">
      (services/search_service.py)
    </text>
  </g>
  <path d="M 990 450 L 1050 450 L 1050 237 L 1120 237" fill="none" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Output 2: KW to Layer 6 -->
  <g filter="url(#shadow)">
    <rect x="1120" y="325" width="410" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1325" y="360" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Analysis Service (Keywords)
    </text>
    <text x="1325" y="385" font-family="monospace" font-size="12" fill="#7C3AED" text-anchor="middle">
      (services/analysis_service.py)
    </text>
  </g>
  <path d="M 990 450 L 1070 450 L 1070 367 L 1120 367" fill="none" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Output 3: Country to Layer 6 -->
  <g filter="url(#shadow)">
    <rect x="1120" y="455" width="410" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1325" y="490" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Country Service (Geo/Collab)
    </text>
    <text x="1325" y="515" font-family="monospace" font-size="12" fill="#7C3AED" text-anchor="middle">
      (services/country_service.py)
    </text>
  </g>
  <line x1="990" y1="450" x2="1120" y2="497" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Output 4: Embeddings to Layer 6 -->
  <g filter="url(#shadow)">
    <rect x="1120" y="585" width="410" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1325" y="620" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: Embedding &amp; Vector Service
    </text>
    <text x="1325" y="645" font-family="monospace" font-size="12" fill="#7C3AED" text-anchor="middle">
      (services/embedding_service.py)
    </text>
  </g>
  <path d="M 990 450 L 1070 450 L 1070 627 L 1120 627" fill="none" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Output 5: Chat to Layer 6 -->
  <g filter="url(#shadow)">
    <rect x="1120" y="715" width="410" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1325" y="750" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#581C87" text-anchor="middle">
      To Layer 6: RAG Chat Service
    </text>
    <text x="1325" y="775" font-family="monospace" font-size="12" fill="#7C3AED" text-anchor="middle">
      (services/chat_service.py)
    </text>
  </g>
  <path d="M 990 450 L 1050 450 L 1050 757 L 1120 757" fill="none" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>
</svg>
"""

def generate_layer_03():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#FFF7ED')
    ax.set_facecolor('#FFF7ED')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#FED7AA", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#C2410C", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 3: BACKEND ROUTING & CONTROLLER LAYER",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Orange | M.Tech Architecture Specification",
            fontsize=11, color="#FFEDD5", va='center', ha='right')

    # Left Container: Inputs from L2
    in_box = FancyBboxPatch((50, 140), 310, 670, boxstyle="round,pad=8,rounding_size=12",
                            facecolor="#F8FAFC", edgecolor="#2563EB", linewidth=1.5, linestyle="--")
    ax.add_patch(in_box)
    ax.text(75, 785, "INPUTS ← FROM LAYER 2", fontsize=11, fontweight='bold', color="#1D4ED8")

    inputs = [
        ("From Layer 2: Search Request", "POST /api/v1/search/query", 670),
        ("From Layer 2: File Operations", "GET/POST /api/v1/files/*", 530),
        ("From Layer 2: Analysis Queries", "GET/POST /api/v1/analysis/*", 390),
        ("From Layer 2: Chat & Embeddings", "POST /api/v1/chat/* & embed/*", 250),
    ]

    for title, ep, y in inputs:
        box = FancyBboxPatch((65, y), 280, 75, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2, linestyle="--")
        ax.add_patch(box)
        ax.text(205, y + 42, title, fontsize=10, fontweight='bold', color="#1E40AF", ha='center')
        ax.text(205, y + 20, ep, fontsize=9, fontfamily='monospace', color="#2563EB", ha='center')

    # Center Container: Layer 3 Core
    c_box = FancyBboxPatch((380, 60), 700, 750, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(405, 785, "3. BACKEND ROUTING & CONTROLLER LAYER (Internal Architecture)",
            fontsize=12, fontweight='bold', color="#C2410C")

    # 4 Controllers
    controllers = [
        ("Search Controller", "(api/routes/search.py)", 670),
        ("Files Controller", "(api/routes/files.py)", 530),
        ("Analysis Controller", "(api/routes/analysis.py)", 390),
        ("Chat & Embedding Controller", "(api/routes/chat.py & embeddings.py)", 250),
    ]

    for title, fpath, y in controllers:
        c_item = FancyBboxPatch((400, y), 290, 75, boxstyle="round,pad=6,rounding_size=8",
                                facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=2.5)
        ax.add_patch(c_item)
        ax.text(545, y + 42, title, fontsize=11, fontweight='bold', color="#7C2D12", ha='center')
        ax.text(545, y + 20, fpath, fontsize=9, fontfamily='monospace', color="#9A3412", ha='center')

        # Arrow from input
        ax.annotate('', xy=(400, y + 37), xytext=(345, y + 37),
                    arrowprops=dict(arrowstyle="->", color="#EA580C", lw=2, mutation_scale=12))

    # Decision Diamond: Request Validation
    val_diamond = Polygon([(850, 580), (990, 500), (850, 420), (710, 500)],
                          facecolor="#FFEDD5", edgecolor="#C2410C", linewidth=3)
    ax.add_patch(val_diamond)
    ax.text(850, 510, "Request Validation", fontsize=12, fontweight='bold', color="#7C2D12", ha='center')
    ax.text(850, 485, "(schemas.py Pydantic)", fontsize=10, fontfamily='monospace', color="#9A3412", ha='center')

    # Arrows from controllers to diamond
    ax.annotate('', xy=(760, 520), xytext=(690, 707),
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(730, 505), xytext=(690, 567),
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(730, 495), xytext=(690, 427),
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=1.5, mutation_scale=10))
    ax.annotate('', xy=(760, 480), xytext=(690, 287),
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=1.5, mutation_scale=10))

    # Error Validation Box (Below diamond)
    err_box = FancyBboxPatch((720, 240), 260, 80, boxstyle="round,pad=6,rounding_size=8",
                             facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=2.5)
    ax.add_patch(err_box)
    ax.text(850, 285, "Return HTTP 400 / 404 / 500", fontsize=11, fontweight='bold', color="#991B1B", ha='center')
    ax.text(850, 260, "Standardized Error Payload", fontsize=9, color="#B91C1C", ha='center')

    # Arrow to Error
    ax.annotate('', xy=(850, 320), xytext=(850, 420),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, mutation_scale=12))
    ax.text(860, 370, "Invalid", fontsize=10, fontweight='bold', color="#DC2626")

    # Error output to L2
    err_out = FancyBboxPatch((65, 80), 280, 65, boxstyle="round,pad=6,rounding_size=8",
                            facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=2, linestyle="--")
    ax.add_patch(err_out)
    ax.text(205, 120, "To Layer 2: Axios API Client", fontsize=10, fontweight='bold', color="#991B1B", ha='center')
    ax.text(205, 98, "(Dispatch Error Callback)", fontsize=9, color="#B91C1C", ha='center')
    ax.annotate('', xy=(205, 145), xytext=(720, 270),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.5, linestyle="--", mutation_scale=10))

    # Right Container: Outputs to Services (L4 & L6)
    out_box = FancyBboxPatch((1100, 60), 450, 750, boxstyle="round,pad=8,rounding_size=12",
                             facecolor="#F8FAFC", edgecolor="#0891B2", linewidth=1.5, linestyle="--")
    ax.add_patch(out_box)
    ax.text(1125, 785, "VALIDATED OUTPUTS → TO SERVICES (LAYERS 4 & 6)",
            fontsize=11, fontweight='bold', color="#0E7490")

    outputs = [
        ("To Layer 4: Search Service", "(services/search_service.py)", 670, "#ECFEFF", "#0891B2", "#155E75"),
        ("To Layer 6: Analysis Service (KW)", "(services/analysis_service.py)", 540, "#FAF5FF", "#9333EA", "#581C87"),
        ("To Layer 6: Country Service", "(services/country_service.py)", 410, "#FAF5FF", "#9333EA", "#581C87"),
        ("To Layer 6: Embedding Service", "(services/embedding_service.py)", 280, "#FAF5FF", "#9333EA", "#581C87"),
        ("To Layer 6: RAG Chat Service", "(services/chat_service.py)", 150, "#FAF5FF", "#9333EA", "#581C87"),
    ]

    for title, fdesc, y, bg, border, tc in outputs:
        o_item = FancyBboxPatch((1120, y), 410, 75, boxstyle="round,pad=6,rounding_size=8",
                                facecolor=bg, edgecolor=border, linewidth=2, linestyle="--")
        ax.add_patch(o_item)
        ax.text(1325, y + 42, title, fontsize=11, fontweight='bold', color=tc, ha='center')
        ax.text(1325, y + 20, fdesc, fontsize=9, fontfamily='monospace', color=tc, ha='center')

        # Arrow from Validation Diamond
        ax.annotate('', xy=(1120, y + 37), xytext=(990, 500),
                    arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2, mutation_scale=12))

    ax.text(1020, 520, "[Valid]", fontsize=10, fontweight='bold', color="#16A34A")

    save_all_formats("layer_03_backend_controllers", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_03()
