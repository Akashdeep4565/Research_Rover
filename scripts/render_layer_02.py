"""
scripts/render_layer_02.py
Layer 2: Frontend API Client Layer (Blue)
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
    %% LAYER 2: FRONTEND API CLIENT LAYER (BLUE)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef blueNode fill:#EFF6FF,stroke:#2563EB,stroke-width:2.5px,color:#1E3A8A,font-size:14px;
    classDef clientNode fill:#DBEAFE,stroke:#1D4ED8,stroke-width:3px,color:#1E40AF,font-weight:bold,font-size:15px;
    classDef boundaryIn fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,stroke-dasharray: 5 5,color:#581C87,font-size:13px;
    classDef boundaryOut fill:#FFF7ED,stroke:#EA580C,stroke-width:2px,stroke-dasharray: 5 5,color:#9A3412,font-size:13px;
    classDef boundaryErr fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,stroke-dasharray: 5 5,color:#991B1B,font-size:13px;

    subgraph IN_L1["INPUTS FROM LAYER 1 (USER INTERACTION)"]
        IN_L1_SEARCH[["From Layer 1: Search Page<br/>(Search Query & Parameters)"]]:::boundaryIn
        IN_L1_ANALYTICS[["From Layer 1: Analytics Page<br/>(Dataset Selection & Filters)"]]:::boundaryIn
        IN_L1_CHAT[["From Layer 1: Chat Page<br/>(User Prompt & Session Context)"]]:::boundaryIn
    end

    subgraph L2_CORE["LAYER 2: FRONTEND API CLIENT LAYER"]
        API_CLIENT["Axios API Client<br/>(services/api.ts - Base URL: /api/v1)"]:::clientNode
        
        REQ_SEARCH["POST /api/v1/search/query"]:::blueNode
        REQ_FILES["GET /api/v1/files/list<br/>POST /api/v1/files/upload"]:::blueNode
        REQ_KW["POST /api/v1/analysis/generate<br/>GET /api/v1/analysis/{file}/matrix"]:::blueNode
        REQ_COUNTRY["GET /api/v1/analysis/{file}/countries<br/>GET /api/v1/analysis/{file}/country-collaboration"]:::blueNode
        REQ_CHAT["POST /api/v1/chat/query<br/>POST /api/v1/embeddings/generate"]:::blueNode
    end

    IN_L3_ERR[["From Layer 3: Error Validation<br/>(HTTP 400 / 404 / 500 Payload)"]]:::boundaryErr

    subgraph OUT_L3["OUTPUTS TO LAYER 3 (BACKEND CONTROLLERS)"]
        OUT_L3_SEARCH[["To Layer 3: Search Controller<br/>(api/routes/search.py)"]]:::boundaryOut
        OUT_L3_FILES[["To Layer 3: Files Controller<br/>(api/routes/files.py)"]]:::boundaryOut
        OUT_L3_KW[["To Layer 3: Analysis Controller (KW)<br/>(api/routes/analysis.py)"]]:::boundaryOut
        OUT_L3_COUNTRY[["To Layer 3: Analysis Controller (Country)<br/>(api/routes/analysis.py)"]]:::boundaryOut
        OUT_L3_CHAT[["To Layer 3: Chat Controller<br/>(api/routes/chat.py & embeddings.py)"]]:::boundaryOut
    end

    %% Internal Connections
    IN_L1_SEARCH --> API_CLIENT
    IN_L1_ANALYTICS --> API_CLIENT
    IN_L1_CHAT --> API_CLIENT

    API_CLIENT -->|Search| REQ_SEARCH
    API_CLIENT -->|File Ops| REQ_FILES
    API_CLIENT -->|Keyword Analysis| REQ_KW
    API_CLIENT -->|Country Analysis| REQ_COUNTRY
    API_CLIENT -->|Chat / Embed| REQ_CHAT

    REQ_SEARCH --> OUT_L3_SEARCH
    REQ_FILES --> OUT_L3_FILES
    REQ_KW --> OUT_L3_KW
    REQ_COUNTRY --> OUT_L3_COUNTRY
    REQ_CHAT --> OUT_L3_CHAT

    IN_L3_ERR -.->|Error Callback & Toast| API_CLIENT
"""

SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 950" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#EFF6FF"/>
      <stop offset="100%" stop-color="#DBEAFE"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1D4ED8"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563EB"/>
    </marker>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#EA580C"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#DC2626"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#EFF6FF"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 2: FRONTEND API CLIENT LAYER
  </text>
  <text x="1080" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#BFDBFE">
    Color Theme: Blue | Scope: Axios REST Client &amp; Endpoint Dispatch
  </text>

  <!-- Left: Boundary Inputs from Layer 1 -->
  <rect x="50" y="130" width="340" height="630" rx="14" fill="#F8FAFC" stroke="#9333EA" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="75" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#7C3AED">
    INPUTS &larr; FROM LAYER 1
  </text>

  <g filter="url(#shadow)">
    <rect x="70" y="190" width="300" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="225" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8" text-anchor="middle">
      From Layer 1: Search Page
    </text>
    <text x="220" y="248" font-family="system-ui, sans-serif" font-size="11" fill="#7E22CE" text-anchor="middle">
      (Query String &amp; Filters)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="70" y="315" width="300" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="350" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8" text-anchor="middle">
      From Layer 1: Analytics Page
    </text>
    <text x="220" y="373" font-family="system-ui, sans-serif" font-size="11" fill="#7E22CE" text-anchor="middle">
      (CSV Dataset File Selection)
    </text>
  </g>

  <g filter="url(#shadow)">
    <rect x="70" y="440" width="300" height="85" rx="10" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="475" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#6B21A8" text-anchor="middle">
      From Layer 1: Chat Page
    </text>
    <text x="220" y="498" font-family="system-ui, sans-serif" font-size="11" fill="#7E22CE" text-anchor="middle">
      (RAG Query &amp; Session History)
    </text>
  </g>

  <!-- Error Return from Layer 3 -->
  <g filter="url(#shadow)">
    <rect x="70" y="620" width="300" height="110" rx="10" fill="#FEF2F2" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="220" y="655" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991B1B" text-anchor="middle">
      [From Layer 3: Error Validation]
    </text>
    <text x="220" y="678" font-family="system-ui, sans-serif" font-size="11" fill="#B91C1C" text-anchor="middle">
      Return HTTP 400 / 404 / 500
    </text>
    <text x="220" y="698" font-family="system-ui, sans-serif" font-size="11" fill="#B91C1C" text-anchor="middle">
      Error Payload &amp; Notifications
    </text>
  </g>

  <!-- Middle: Center Subgraph - Layer 2 Core -->
  <rect x="420" y="130" width="670" height="780" rx="14" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="445" y="160" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#1D4ED8">
    2. FRONTEND API CLIENT LAYER (Internal Architecture)
  </text>

  <!-- Main Axios Client Box -->
  <g filter="url(#shadow)">
    <rect x="460" y="185" width="590" height="85" rx="12" fill="url(#blueGrad)" stroke="#1D4ED8" stroke-width="3"/>
    <text x="755" y="222" font-family="system-ui, sans-serif" font-size="18" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      Axios API Client
    </text>
    <text x="755" y="248" font-family="monospace" font-size="13" fill="#1E3A8A" text-anchor="middle">
      (services/api.ts - Base URL: /api/v1)
    </text>
  </g>

  <!-- Arrows from Inputs to Axios Client -->
  <path d="M 370 232 L 415 232 L 415 220 L 460 220" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 370 357 L 415 357 L 415 230 L 460 230" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 370 482 L 415 482 L 415 240 L 460 240" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 370 675 L 435 675 L 435 250 L 460 250" fill="none" stroke="#DC2626" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrowRed)"/>

  <!-- 5 Request Boxes inside Layer 2 -->
  <!-- 1. Search Request -->
  <g filter="url(#shadow)">
    <rect x="490" y="310" width="530" height="75" rx="10" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <text x="755" y="342" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1E3A8A" text-anchor="middle">
      Search Request Dispatch
    </text>
    <text x="755" y="365" font-family="monospace" font-size="13" font-weight="bold" fill="#2563EB" text-anchor="middle">
      POST /api/v1/search/query
    </text>
  </g>

  <!-- 2. Files Request -->
  <g filter="url(#shadow)">
    <rect x="490" y="420" width="530" height="85" rx="10" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <text x="755" y="452" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1E3A8A" text-anchor="middle">
      File Management Requests
    </text>
    <text x="755" y="475" font-family="monospace" font-size="12" fill="#2563EB" text-anchor="middle">
      GET /api/v1/files/list | POST /api/v1/files/upload
    </text>
  </g>

  <!-- 3. KW Request -->
  <g filter="url(#shadow)">
    <rect x="490" y="540" width="530" height="85" rx="10" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <text x="755" y="572" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1E3A8A" text-anchor="middle">
      Keyword Analytics Requests
    </text>
    <text x="755" y="595" font-family="monospace" font-size="12" fill="#2563EB" text-anchor="middle">
      POST /api/v1/analysis/generate | GET /api/v1/analysis/{file}/matrix
    </text>
  </g>

  <!-- 4. Country Request -->
  <g filter="url(#shadow)">
    <rect x="490" y="660" width="530" height="85" rx="10" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <text x="755" y="692" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1E3A8A" text-anchor="middle">
      Country Collaboration Requests
    </text>
    <text x="755" y="715" font-family="monospace" font-size="12" fill="#2563EB" text-anchor="middle">
      GET /api/v1/analysis/{file}/countries | .../country-collaboration
    </text>
  </g>

  <!-- 5. Chat Request -->
  <g filter="url(#shadow)">
    <rect x="490" y="780" width="530" height="85" rx="10" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
    <text x="755" y="812" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#1E3A8A" text-anchor="middle">
      Chat &amp; Embedding Requests
    </text>
    <text x="755" y="835" font-family="monospace" font-size="12" fill="#2563EB" text-anchor="middle">
      POST /api/v1/chat/query | POST /api/v1/embeddings/generate
    </text>
  </g>

  <!-- Internal Dispatch Arrows from Axios to Request Nodes -->
  <path d="M 755 270 L 755 310" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <path d="M 520 270 L 520 420" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 500 270 L 500 540" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 480 270 L 480 660" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>
  <path d="M 465 270 L 465 780" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>

  <!-- Right: Boundary Outputs to Layer 3 -->
  <rect x="1120" y="130" width="430" height="780" rx="14" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="1145" y="160" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#C2410C">
    OUTPUTS &rarr; TO LAYER 3 (BACKEND CONTROLLERS)
  </text>

  <!-- Output 1: Search -->
  <g filter="url(#shadow)">
    <rect x="1140" y="310" width="390" height="75" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1335" y="342" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      To Layer 3: Search Controller
    </text>
    <text x="1335" y="365" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (api/routes/search.py)
    </text>
  </g>
  <line x1="1020" y1="347" x2="1140" y2="347" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

  <!-- Output 2: Files -->
  <g filter="url(#shadow)">
    <rect x="1140" y="425" width="390" height="75" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1335" y="457" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      To Layer 3: Files Controller
    </text>
    <text x="1335" y="480" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (api/routes/files.py)
    </text>
  </g>
  <line x1="1020" y1="462" x2="1140" y2="462" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

  <!-- Output 3: KW -->
  <g filter="url(#shadow)">
    <rect x="1140" y="545" width="390" height="75" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1335" y="577" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      To Layer 3: Analysis Controller (KW)
    </text>
    <text x="1335" y="600" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (api/routes/analysis.py)
    </text>
  </g>
  <line x1="1020" y1="582" x2="1140" y2="582" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

  <!-- Output 4: Country -->
  <g filter="url(#shadow)">
    <rect x="1140" y="665" width="390" height="75" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1335" y="697" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      To Layer 3: Analysis Controller (Country)
    </text>
    <text x="1335" y="720" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (api/routes/analysis.py)
    </text>
  </g>
  <line x1="1020" y1="702" x2="1140" y2="702" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

  <!-- Output 5: Chat -->
  <g filter="url(#shadow)">
    <rect x="1140" y="785" width="390" height="75" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="1335" y="817" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#9A3412" text-anchor="middle">
      To Layer 3: Chat Controller
    </text>
    <text x="1335" y="840" font-family="monospace" font-size="11" fill="#C2410C" text-anchor="middle">
      (api/routes/chat.py &amp; embeddings.py)
    </text>
  </g>
  <line x1="1020" y1="822" x2="1140" y2="822" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>
</svg>
"""

def generate_layer_02():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    fig.patch.set_facecolor('#EFF6FF')
    ax.set_facecolor('#EFF6FF')
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((30, 30), 1540, 890, boxstyle="round,pad=10,rounding_size=20",
                          facecolor="#FFFFFF", edgecolor="#BFDBFE", linewidth=2)
    ax.add_patch(card)

    # Header
    hdr = FancyBboxPatch((50, 840), 1500, 60, boxstyle="round,pad=5,rounding_size=12",
                         facecolor="#1D4ED8", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 2: FRONTEND API CLIENT LAYER",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Blue | M.Tech Architecture Specification",
            fontsize=11, color="#BFDBFE", va='center', ha='right')

    # Left Container: Inputs from L1
    in_box = FancyBboxPatch((50, 140), 340, 670, boxstyle="round,pad=8,rounding_size=12",
                            facecolor="#F8FAFC", edgecolor="#9333EA", linewidth=1.5, linestyle="--")
    ax.add_patch(in_box)
    ax.text(75, 785, "INPUTS ← FROM LAYER 1", fontsize=11, fontweight='bold', color="#7C3AED")

    in1 = FancyBboxPatch((70, 675), 300, 75, boxstyle="round,pad=6,rounding_size=8",
                         facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(in1)
    ax.text(220, 722, "From Layer 1: Search Page", fontsize=10, fontweight='bold', color="#6B21A8", ha='center')
    ax.text(220, 700, "(Search Query & Parameters)", fontsize=9, color="#7E22CE", ha='center')

    in2 = FancyBboxPatch((70, 565), 300, 75, boxstyle="round,pad=6,rounding_size=8",
                         facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(in2)
    ax.text(220, 612, "From Layer 1: Analytics Page", fontsize=10, fontweight='bold', color="#6B21A8", ha='center')
    ax.text(220, 590, "(Dataset File Selection)", fontsize=9, color="#7E22CE", ha='center')

    in3 = FancyBboxPatch((70, 455), 300, 75, boxstyle="round,pad=6,rounding_size=8",
                         facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2, linestyle="--")
    ax.add_patch(in3)
    ax.text(220, 502, "From Layer 1: Chat Page", fontsize=10, fontweight='bold', color="#6B21A8", ha='center')
    ax.text(220, 480, "(RAG Query & Context)", fontsize=9, color="#7E22CE", ha='center')

    # Error input
    in_err = FancyBboxPatch((70, 180), 300, 95, boxstyle="round,pad=6,rounding_size=8",
                            facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=2, linestyle="--")
    ax.add_patch(in_err)
    ax.text(220, 245, "[From Layer 3: Validation Error]", fontsize=10, fontweight='bold', color="#991B1B", ha='center')
    ax.text(220, 225, "Return HTTP 400 / 404 / 500", fontsize=9, color="#B91C1C", ha='center')
    ax.text(220, 205, "Error Payload & User Feedback", fontsize=9, color="#B91C1C", ha='center')

    # Center Container: Layer 2 Core
    c_box = FancyBboxPatch((420, 60), 670, 750, boxstyle="round,pad=8,rounding_size=12",
                           facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2.5, linestyle="--")
    ax.add_patch(c_box)
    ax.text(445, 785, "2. FRONTEND API CLIENT LAYER (Internal Architecture)",
            fontsize=13, fontweight='bold', color="#1D4ED8")

    # Axios client
    client = FancyBboxPatch((460, 680), 590, 75, boxstyle="round,pad=8,rounding_size=10",
                            facecolor="#DBEAFE", edgecolor="#1D4ED8", linewidth=3)
    ax.add_patch(client)
    ax.text(755, 725, "Axios API Client", fontsize=15, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(755, 700, "(services/api.ts - Base URL: /api/v1)", fontsize=11, fontfamily='monospace', color="#1E3A8A", ha='center')

    # Wiring from Inputs to Axios
    ax.annotate('', xy=(460, 725), xytext=(370, 712),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2, mutation_scale=12))
    ax.annotate('', xy=(460, 720), xytext=(370, 602),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2, mutation_scale=12))
    ax.annotate('', xy=(460, 715), xytext=(370, 492),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2, mutation_scale=12))
    ax.annotate('', xy=(460, 700), xytext=(370, 230),
                arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2, linestyle="--", mutation_scale=12))

    # Request Nodes
    reqs = [
        ("POST /api/v1/search/query", "Search Request Dispatch", 570),
        ("GET /api/v1/files/list | POST /api/v1/files/upload", "File Management Requests", 465),
        ("POST /api/v1/analysis/generate | GET .../matrix", "Keyword Analytics Requests", 360),
        ("GET /api/v1/analysis/{file}/countries | .../country-collab", "Country Collaboration Requests", 255),
        ("POST /api/v1/chat/query | POST /api/v1/embeddings/generate", "Chat & Embedding Requests", 150),
    ]

    for ep, title, y in reqs:
        r_box = FancyBboxPatch((490, y), 530, 65, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#FFFFFF", edgecolor="#2563EB", linewidth=2)
        ax.add_patch(r_box)
        ax.text(755, y + 42, title, fontsize=11, fontweight='bold', color="#1E3A8A", ha='center')
        ax.text(755, y + 18, ep, fontsize=10, fontfamily='monospace', color="#2563EB", ha='center')
        ax.annotate('', xy=(755, y + 65), xytext=(755, 680),
                    arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5, mutation_scale=10))

    # Right Container: Outputs to Layer 3
    out_box = FancyBboxPatch((1120, 60), 430, 750, boxstyle="round,pad=8,rounding_size=12",
                             facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=1.5, linestyle="--")
    ax.add_patch(out_box)
    ax.text(1145, 785, "OUTPUTS → TO LAYER 3 (CONTROLLERS)", fontsize=11, fontweight='bold', color="#C2410C")

    outs = [
        ("To Layer 3: Search Controller", "(api/routes/search.py)", 570),
        ("To Layer 3: Files Controller", "(api/routes/files.py)", 465),
        ("To Layer 3: Analysis Controller (KW)", "(api/routes/analysis.py)", 360),
        ("To Layer 3: Analysis Controller (Country)", "(api/routes/analysis.py)", 255),
        ("To Layer 3: Chat Controller", "(api/routes/chat.py & embeddings.py)", 150),
    ]

    for title, file_desc, y in outs:
        o_box = FancyBboxPatch((1140, y), 390, 65, boxstyle="round,pad=6,rounding_size=8",
                               facecolor="#FFFFFF", edgecolor="#EA580C", linewidth=2, linestyle="--")
        ax.add_patch(o_box)
        ax.text(1335, y + 42, title, fontsize=11, fontweight='bold', color="#9A3412", ha='center')
        ax.text(1335, y + 18, file_desc, fontsize=10, fontfamily='monospace', color="#C2410C", ha='center')
        ax.annotate('', xy=(1140, y + 32), xytext=(1020, y + 32),
                    arrowprops=dict(arrowstyle="->", color="#EA580C", lw=2, mutation_scale=12))

    save_all_formats("layer_02_frontend_api", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_02()
