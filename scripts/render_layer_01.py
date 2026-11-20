"""
scripts/render_layer_01.py
Layer 1: User & Frontend Interaction Layer (Purple)
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
    %% LAYER 1: USER & FRONTEND INTERACTION LAYER (PURPLE)
    %% Standalone Enlarged Flowchart with Boundary Connectors
    %% =========================================================================

    classDef purpleNode fill:#FAF5FF,stroke:#9333EA,stroke-width:2.5px,color:#581C87,font-size:14px;
    classDef startNode fill:#F3E8FF,stroke:#7C3AED,stroke-width:3px,color:#4C1D95,font-weight:bold,font-size:15px;
    classDef decisionNode fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2.5px,color:#5B21B6,font-weight:bold,font-size:14px;
    classDef boundaryOut fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,stroke-dasharray: 5 5,color:#1E3A8A,font-size:13px;
    classDef boundaryIn fill:#FDF2F8,stroke:#DB2777,stroke-width:2px,stroke-dasharray: 5 5,color:#831843,font-size:13px;

    IN_L7_FEEDBACK[["[External Feedback from Layer 7]<br/>Delivered Insights & Exported CSV/JSON/PNG"]]:::boundaryIn

    subgraph L1_CORE["LAYER 1: USER & FRONTEND INTERACTION LAYER"]
        U_START(["User Accesses Research Rover"]):::startNode
        U_INPUT["Enter Query / Filters<br/>(Query string, max results, date range)"]:::purpleNode
        U_NAV{"Select Page View"}:::decisionNode
        PAGE_SEARCH["Search Page<br/>(SearchPage.tsx, SearchContext.tsx)"]:::purpleNode
        PAGE_ANALYTICS["Analytics Page<br/>(AnalyticsPage.tsx, AnalyticsContext.tsx)"]:::purpleNode
        PAGE_CHAT["Chat Page<br/>(ChatPage.tsx, ChatContext.tsx)"]:::purpleNode
    end

    OUT_API_SEARCH[["[Output to Layer 2: API Client]<br/>POST /api/v1/search/query"]]:::boundaryOut
    OUT_API_ANALYTICS[["[Output to Layer 2: API Client]<br/>GET/POST /api/v1/analysis/* & files/*"]]:::boundaryOut
    OUT_API_CHAT[["[Output to Layer 2: API Client]<br/>POST /api/v1/chat/query & embeddings/*"]]:::boundaryOut

    %% Internal Connections
    U_START --> U_INPUT
    U_INPUT --> U_NAV

    U_NAV -->|Search Query| PAGE_SEARCH
    U_NAV -->|Analyze CSV| PAGE_ANALYTICS
    U_NAV -->|Chat Query| PAGE_CHAT

    %% External Outgoing Connections
    PAGE_SEARCH --> OUT_API_SEARCH
    PAGE_ANALYTICS --> OUT_API_ANALYTICS
    PAGE_CHAT --> OUT_API_CHAT

    %% External Incoming Feedback
    IN_L7_FEEDBACK -.->|User Explores Results| U_NAV
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
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#9333EA"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#7C3AED"/>
    </marker>
    <marker id="arrowDash" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#BE185D"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1600" height="950" fill="#FAF5FF"/>
  <rect x="20" y="20" width="1560" height="910" rx="16" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="50" y="40" width="1500" height="70" rx="12" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <text x="80" y="82" font-family="system-ui, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">
    LAYER 1: USER &amp; FRONTEND INTERACTION LAYER
  </text>
  <text x="1100" y="82" font-family="system-ui, sans-serif" font-size="14" fill="#E9D5FF">
    Color Theme: Purple | Scope: User Journey &amp; Decision Navigation
  </text>

  <!-- Section Container -->
  <rect x="50" y="130" width="1500" height="570" rx="14" fill="#FAF5FF" stroke="#9333EA" stroke-width="2.5" stroke-dasharray="6 4"/>
  <text x="80" y="160" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#7C3AED">
    1. USER &amp; FRONTEND LAYER (Internal Architecture)
  </text>

  <!-- Boundary In: Layer 7 Feedback -->
  <g filter="url(#shadow)">
    <rect x="70" y="365" width="220" height="80" rx="8" fill="#FDF2F8" stroke="#DB2777" stroke-width="2" stroke-dasharray="4 4"/>
    <text x="180" y="395" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#9D174D" text-anchor="middle">
      [External Input from Layer 7]
    </text>
    <text x="180" y="415" font-family="system-ui, sans-serif" font-size="11" fill="#BE185D" text-anchor="middle">
      Delivered Insights &amp;
    </text>
    <text x="180" y="430" font-family="system-ui, sans-serif" font-size="11" fill="#BE185D" text-anchor="middle">
      Exported CSV/JSON/PNG
    </text>
  </g>

  <!-- Start Node -->
  <g filter="url(#shadow)">
    <rect x="620" y="175" width="360" height="55" rx="27.5" fill="#F3E8FF" stroke="#7C3AED" stroke-width="3"/>
    <text x="800" y="210" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#4C1D95" text-anchor="middle">
      User Accesses Research Rover
    </text>
  </g>

  <!-- Arrow: Start -> Input -->
  <line x1="800" y1="230" x2="800" y2="265" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Input Node -->
  <g filter="url(#shadow)">
    <rect x="580" y="265" width="440" height="70" rx="10" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2.5"/>
    <text x="800" y="295" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#581C87" text-anchor="middle">
      Enter Query / Filters
    </text>
    <text x="800" y="318" font-family="system-ui, sans-serif" font-size="12" fill="#7E22CE" text-anchor="middle">
      (Query string, max results, date range)
    </text>
  </g>

  <!-- Arrow: Input -> Nav -->
  <line x1="800" y1="335" x2="800" y2="370" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Decision Diamond: Select Page View -->
  <g filter="url(#shadow)">
    <polygon points="800,370 940,420 800,470 660,420" fill="#EDE9FE" stroke="#8B5CF6" stroke-width="2.5"/>
    <text x="800" y="425" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#5B21B6" text-anchor="middle">
      Select Page View
    </text>
  </g>

  <!-- Dashed Feedback Arrow -->
  <line x1="290" y1="410" x2="655" y2="410" stroke="#DB2777" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#arrowDash)"/>
  <text x="470" y="400" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#BE185D" text-anchor="middle">
    User Review &amp; Exploration
  </text>

  <!-- Branch Arrows from Diamond -->
  <!-- Left to Search -->
  <path d="M 660 420 L 290 420 L 290 525" fill="none" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="440" y="440" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#6B21A8">
    [Branch 1: Search Query]
  </text>

  <!-- Center to Analytics -->
  <line x1="800" y1="470" x2="800" y2="525" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="815" y="500" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#6B21A8">
    [Branch 2: Analyze CSV]
  </text>

  <!-- Right to Chat -->
  <path d="M 940 420 L 1310 420 L 1310 525" fill="none" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="1050" y="440" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#6B21A8">
    [Branch 3: Chat Query]
  </text>

  <!-- Page 1: Search Page -->
  <g filter="url(#shadow)">
    <rect x="90" y="530" width="400" height="95" rx="10" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2.5"/>
    <text x="290" y="565" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#581C87" text-anchor="middle">
      Search Page
    </text>
    <text x="290" y="590" font-family="system-ui, sans-serif" font-size="13" font-family="monospace" fill="#7E22CE" text-anchor="middle">
      (SearchPage.tsx, SearchContext.tsx)
    </text>
  </g>

  <!-- Page 2: Analytics Page -->
  <g filter="url(#shadow)">
    <rect x="600" y="530" width="400" height="95" rx="10" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2.5"/>
    <text x="800" y="565" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#581C87" text-anchor="middle">
      Analytics Page
    </text>
    <text x="800" y="590" font-family="system-ui, sans-serif" font-size="13" font-family="monospace" fill="#7E22CE" text-anchor="middle">
      (AnalyticsPage.tsx, AnalyticsContext.tsx)
    </text>
  </g>

  <!-- Page 3: Chat Page -->
  <g filter="url(#shadow)">
    <rect x="1110" y="530" width="400" height="95" rx="10" fill="url(#purpleGrad)" stroke="#9333EA" stroke-width="2.5"/>
    <text x="1310" y="565" font-family="system-ui, sans-serif" font-size="16" font-weight="bold" fill="#581C87" text-anchor="middle">
      Chat Page
    </text>
    <text x="1310" y="590" font-family="system-ui, sans-serif" font-size="13" font-family="monospace" fill="#7E22CE" text-anchor="middle">
      (ChatPage.tsx, ChatContext.tsx)
    </text>
  </g>

  <!-- Outgoing Boundary Connectors Container -->
  <rect x="50" y="730" width="1500" height="170" rx="12" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="80" y="755" font-family="system-ui, sans-serif" font-size="14" font-weight="bold" fill="#475569">
    BOUNDARY OUTPUTS &rarr; TO LAYER 2 (FRONTEND API CLIENT LAYER)
  </text>

  <!-- Arrows from Pages to Output Connectors -->
  <line x1="290" y1="625" x2="290" y2="775" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="800" y1="625" x2="800" y2="775" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="1310" y1="625" x2="1310" y2="775" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Output 1: Search -->
  <g filter="url(#shadow)">
    <rect x="90" y="780" width="400" height="85" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="5 4"/>
    <text x="290" y="812" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      [Output to Layer 2: API Client]
    </text>
    <text x="290" y="835" font-family="monospace" font-size="12" fill="#1D4ED8" text-anchor="middle">
      POST /api/v1/search/query
    </text>
  </g>

  <!-- Output 2: Analytics -->
  <g filter="url(#shadow)">
    <rect x="600" y="780" width="400" height="85" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="5 4"/>
    <text x="800" y="812" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      [Output to Layer 2: API Client]
    </text>
    <text x="800" y="835" font-family="monospace" font-size="12" fill="#1D4ED8" text-anchor="middle">
      GET/POST /api/v1/analysis/* &amp; files/*
    </text>
  </g>

  <!-- Output 3: Chat -->
  <g filter="url(#shadow)">
    <rect x="1110" y="780" width="400" height="85" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2" stroke-dasharray="5 4"/>
    <text x="1310" y="812" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#1E40AF" text-anchor="middle">
      [Output to Layer 2: API Client]
    </text>
    <text x="1310" y="835" font-family="monospace" font-size="12" fill="#1D4ED8" text-anchor="middle">
      POST /api/v1/chat/query &amp; embeddings/*
    </text>
  </g>
</svg>
"""

def generate_layer_01():
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
                         facecolor="#7C3AED", edgecolor="none")
    ax.add_patch(hdr)
    ax.text(80, 870, "LAYER 1: USER & FRONTEND INTERACTION LAYER",
            fontsize=18, fontweight='bold', color="#FFFFFF", va='center')
    ax.text(1450, 870, "Theme: Purple | M.Tech Architecture Specification",
            fontsize=11, color="#E9D5FF", va='center', ha='right')

    # Subgraph Border
    sub = FancyBboxPatch((50, 260), 1500, 560, boxstyle="round,pad=10,rounding_size=15",
                         facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5, linestyle="--")
    ax.add_patch(sub)
    ax.text(80, 800, "1. USER & FRONTEND LAYER (Internal Architecture)",
            fontsize=14, fontweight='bold', color="#7C3AED", va='center')

    # Start Node
    st = FancyBboxPatch((620, 720), 360, 50, boxstyle="round,pad=10,rounding_size=25",
                        facecolor="#F3E8FF", edgecolor="#7C3AED", linewidth=3)
    ax.add_patch(st)
    ax.text(800, 745, "User Accesses Research Rover", fontsize=14, fontweight='bold', color="#4C1D95",
            va='center', ha='center')

    # Input Node
    inp = FancyBboxPatch((580, 600), 440, 65, boxstyle="round,pad=10,rounding_size=12",
                         facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5)
    ax.add_patch(inp)
    ax.text(800, 642, "Enter Query / Filters", fontsize=13, fontweight='bold', color="#581C87",
            va='center', ha='center')
    ax.text(800, 620, "(Query string, max results, date range)", fontsize=10, color="#7E22CE",
            va='center', ha='center')

    # Arrow: Start -> Input
    ax.annotate('', xy=(800, 670), xytext=(800, 720),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2.5, mutation_scale=15))

    # Decision Diamond: Select Page View
    diamond = Polygon([(800, 560), (940, 505), (800, 450), (660, 505)],
                      facecolor="#EDE9FE", edgecolor="#8B5CF6", linewidth=2.5)
    ax.add_patch(diamond)
    ax.text(800, 505, "Select Page View", fontsize=13, fontweight='bold', color="#5B21B6",
            va='center', ha='center')

    # Arrow: Input -> Diamond
    ax.annotate('', xy=(800, 560), xytext=(800, 600),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2.5, mutation_scale=15))

    # Pages
    p_search = FancyBboxPatch((90, 310), 400, 85, boxstyle="round,pad=10,rounding_size=12",
                              facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5)
    ax.add_patch(p_search)
    ax.text(290, 362, "Search Page", fontsize=14, fontweight='bold', color="#581C87", va='center', ha='center')
    ax.text(290, 338, "(SearchPage.tsx, SearchContext.tsx)", fontsize=10, fontfamily='monospace', color="#7E22CE", va='center', ha='center')

    p_analytics = FancyBboxPatch((600, 310), 400, 85, boxstyle="round,pad=10,rounding_size=12",
                                facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5)
    ax.add_patch(p_analytics)
    ax.text(800, 362, "Analytics Page", fontsize=14, fontweight='bold', color="#581C87", va='center', ha='center')
    ax.text(800, 338, "(AnalyticsPage.tsx, AnalyticsContext.tsx)", fontsize=10, fontfamily='monospace', color="#7E22CE", va='center', ha='center')

    p_chat = FancyBboxPatch((1110, 310), 400, 85, boxstyle="round,pad=10,rounding_size=12",
                            facecolor="#FAF5FF", edgecolor="#9333EA", linewidth=2.5)
    ax.add_patch(p_chat)
    ax.text(1310, 362, "Chat Page", fontsize=14, fontweight='bold', color="#581C87", va='center', ha='center')
    ax.text(1310, 338, "(ChatPage.tsx, ChatContext.tsx)", fontsize=10, fontfamily='monospace', color="#7E22CE", va='center', ha='center')

    # Connecting Branches
    # Search
    ax.plot([660, 290, 290], [505, 505, 400], color="#7C3AED", lw=2.5)
    ax.annotate('', xy=(290, 400), xytext=(290, 410),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2.5, mutation_scale=15))
    ax.text(450, 515, "Search Query", fontsize=10, fontweight='bold', color="#6B21A8", ha='center')

    # Analytics
    ax.annotate('', xy=(800, 400), xytext=(800, 450),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2.5, mutation_scale=15))
    ax.text(810, 425, "Analyze CSV", fontsize=10, fontweight='bold', color="#6B21A8", ha='left')

    # Chat
    ax.plot([940, 1310, 1310], [505, 505, 400], color="#7C3AED", lw=2.5)
    ax.annotate('', xy=(1310, 400), xytext=(1310, 410),
                arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=2.5, mutation_scale=15))
    ax.text(1130, 515, "Chat Query", fontsize=10, fontweight='bold', color="#6B21A8", ha='center')

    # External Input from Layer 7 (Feedback)
    fb = FancyBboxPatch((70, 465), 230, 80, boxstyle="round,pad=8,rounding_size=10",
                        facecolor="#FDF2F8", edgecolor="#DB2777", linewidth=2, linestyle="--")
    ax.add_patch(fb)
    ax.text(185, 520, "[From Layer 7]", fontsize=10, fontweight='bold', color="#9D174D", ha='center')
    ax.text(185, 495, "Delivered Insights &\nExported Artifacts", fontsize=9, color="#BE185D", ha='center')
    ax.annotate('', xy=(655, 505), xytext=(305, 505),
                arrowprops=dict(arrowstyle="->", color="#DB2777", lw=2, linestyle="--", mutation_scale=12))

    # Boundary Outputs
    b_box = FancyBboxPatch((50, 60), 1500, 170, boxstyle="round,pad=10,rounding_size=12",
                           facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.5, linestyle=":")
    ax.add_patch(b_box)
    ax.text(80, 210, "BOUNDARY OUTPUTS → TO LAYER 2 (FRONTEND API CLIENT LAYER)",
            fontsize=12, fontweight='bold', color="#475569")

    # Output Connectors
    out1 = FancyBboxPatch((90, 85), 400, 75, boxstyle="round,pad=8,rounding_size=10",
                          facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2, linestyle="--")
    ax.add_patch(out1)
    ax.text(290, 132, "To Layer 2: Axios API Client", fontsize=11, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(290, 108, "POST /api/v1/search/query", fontsize=10, fontfamily='monospace', color="#1D4ED8", ha='center')
    ax.annotate('', xy=(290, 165), xytext=(290, 305),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2.5, mutation_scale=15))

    out2 = FancyBboxPatch((600, 85), 400, 75, boxstyle="round,pad=8,rounding_size=10",
                          facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2, linestyle="--")
    ax.add_patch(out2)
    ax.text(800, 132, "To Layer 2: Axios API Client", fontsize=11, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(800, 108, "GET/POST /api/v1/analysis/* & files/*", fontsize=10, fontfamily='monospace', color="#1D4ED8", ha='center')
    ax.annotate('', xy=(800, 165), xytext=(800, 305),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2.5, mutation_scale=15))

    out3 = FancyBboxPatch((1110, 85), 400, 75, boxstyle="round,pad=8,rounding_size=10",
                          facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2, linestyle="--")
    ax.add_patch(out3)
    ax.text(1310, 132, "To Layer 2: Axios API Client", fontsize=11, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(1310, 108, "POST /api/v1/chat/query & embeddings/*", fontsize=10, fontfamily='monospace', color="#1D4ED8", ha='center')
    ax.annotate('', xy=(1310, 165), xytext=(1310, 305),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2.5, mutation_scale=15))

    save_all_formats("layer_01_user_interaction", MMD_CONTENT, SVG_CONTENT, fig)

if __name__ == "__main__":
    generate_layer_01()
