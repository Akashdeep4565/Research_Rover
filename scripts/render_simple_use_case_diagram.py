"""
Generate Simple UML Use Case Diagram for Research Rover.
Reference: Traditional University Management System Use Case Diagram (EdrawMax style).

Style & Architecture:
- One stick-figure actor on the LEFT: "Researcher / Student"
- One large rectangular system boundary in the CENTRE: "Research Rover"
- Simple oval-shaped use cases INSIDE the rectangle (no colored cards, no clusters)
- Clean straight/curved association lines connecting the actor to user use cases
- White background, blue outlines, professional styling
- Pure student-friendly language (no technical jargon, no API names, no <<include>> / <<extend>>)
- Generates: .puml, .svg, .png (300 DPI), .pdf
"""

import os
import shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

# ==============================================================================
# 1. PLANTUML SPECIFICATION (TRADITIONAL SIMPLE LAYOUT)
# ==============================================================================
def get_plantuml_code():
    return """@startuml Research_Rover_Simple_User_Use_Case_Diagram
' ==============================================================================
' Project: Research Rover
' Diagram: Simple User Use Case Diagram
' Reference Style: University Management System Use Case Diagram
' ==============================================================================

skinparam backgroundColor #FFFFFF
skinparam handwritten false
skinparam monochrome false
skinparam shadowing false
skinparam defaultFontName "Segoe UI", Arial, Helvetica, sans-serif
skinparam defaultFontSize 13
skinparam defaultFontColor #0F172A

skinparam actor {
    BackgroundColor #EFF6FF
    BorderColor #1D4ED8
    BorderThickness 2
    FontColor #0F172A
    FontSize 14
    FontStyle bold
}

skinparam rectangle {
    BackgroundColor #FFFFFF
    BorderColor #2563EB
    BorderThickness 2.5
    FontColor #1D4ED8
    FontSize 16
    FontStyle bold
}

skinparam usecase {
    BackgroundColor #F8FAFC
    BorderColor #2563EB
    BorderThickness 1.8
    FontColor #0F172A
    FontSize 12.5
    FontStyle bold
    ArrowColor #3B82F6
    ArrowThickness 1.5
}

left to right direction

actor "Researcher / Student" as User

rectangle "Research Rover" {
    usecase "Search Research Papers" as UC_Search
    usecase "Explore Research Papers" as UC_ExplorePapers
    usecase "View Paper Details" as UC_PaperDetails
    usecase "Download Research Papers" as UC_DownloadPaper
    
    usecase "Upload Dataset" as UC_UploadData
    usecase "View My Datasets" as UC_ViewData
    usecase "Select Dataset" as UC_SelectData
    usecase "Download Dataset" as UC_DownloadData
    
    usecase "Explore Keywords" as UC_Keywords
    usecase "View Popular Keywords" as UC_PopularKW
    usecase "Explore Keyword Connections" as UC_KWConnections
    usecase "View Keyword Networks" as UC_KWNetworks
    
    usecase "Explore Countries" as UC_Countries
    usecase "View Country Rankings" as UC_CountryRank
    usecase "Explore World Map" as UC_WorldMap
    usecase "View International Collaborations" as UC_Collaborations
    
    usecase "Ask Questions" as UC_AskAI
    usecase "Get AI Answers" as UC_AIAnswers
    usecase "Explore Research Information" as UC_ResearchInfo
    
    usecase "Download Charts" as UC_DownloadCharts
    usecase "Export Reports" as UC_ExportReports
}

User -- UC_Search
User -- UC_ExplorePapers
User -- UC_PaperDetails
User -- UC_DownloadPaper

User -- UC_UploadData
User -- UC_ViewData
User -- UC_SelectData
User -- UC_DownloadData

User -- UC_Keywords
User -- UC_PopularKW
User -- UC_KWConnections
User -- UC_KWNetworks

User -- UC_Countries
User -- UC_CountryRank
User -- UC_WorldMap
User -- UC_Collaborations

User -- UC_AskAI
User -- UC_AIAnswers
User -- UC_ResearchInfo

User -- UC_DownloadCharts
User -- UC_ExportReports

@enduml
"""

# ==============================================================================
# 2. STANDALONE SVG SPECIFICATION
# ==============================================================================
def get_svg_code():
    usecases = [
        # Column 1
        (620, 210, "Search Research Papers"),
        (620, 340, "Explore Research Papers"),
        (620, 470, "View Paper Details"),
        (620, 600, "Download Research Papers"),
        (620, 730, "Upload Dataset"),
        (620, 860, "View My Datasets"),
        (620, 990, "Select Dataset"),
        # Column 2
        (1100, 210, "Download Dataset"),
        (1100, 340, "Explore Keywords"),
        (1100, 470, "View Popular Keywords"),
        (1100, 600, "Explore Keyword Connections"),
        (1100, 730, "View Keyword Networks"),
        (1100, 860, "Explore Countries"),
        (1100, 990, "View Country Rankings"),
        # Column 3
        (1580, 210, "Explore World Map"),
        (1580, 340, "View International Collaborations"),
        (1580, 470, "Ask Questions"),
        (1580, 600, "Get AI Answers"),
        (1580, 730, "Explore Research Information"),
        (1580, 860, "Download Charts"),
        (1580, 990, "Export Reports"),
    ]

    svg_lines = []
    actor_x, actor_y = 220, 600

    # Draw connection lines
    for (cx, cy, title) in usecases:
        # Connect to left edge of oval
        target_x = cx - 135
        target_y = cy
        svg_lines.append(f'<line x1="{actor_x}" y1="{actor_y}" x2="{target_x}" y2="{target_y}" stroke="#3b82f6" stroke-width="1.6" opacity="0.85"/>')

    # Draw ovals
    oval_elements = []
    for (cx, cy, title) in usecases:
        oval_elements.append(f'''
    <g transform="translate({cx},{cy})">
      <ellipse cx="0" cy="0" rx="135" ry="32" fill="#f8fafc" stroke="#2563eb" stroke-width="2.0"/>
      <text x="0" y="5" text-anchor="middle" font-size="13.5" font-weight="600" fill="#0f172a">{title}</text>
    </g>''')

    lines_str = "\n  ".join(svg_lines)
    ovals_str = "\n".join(oval_elements)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1150" width="1920" height="1150" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Title Banner -->
  <rect x="50" y="25" width="1820" height="55" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
  <text x="75" y="58" font-size="18" font-weight="bold" fill="#0f172a">Research Rover: Simple User Use Case Diagram</text>
  <text x="1840" y="58" text-anchor="end" font-size="13" font-weight="500" fill="#64748b">Student &amp; Researcher Functional Model</text>

  <!-- Association Lines (Underneath Boundary) -->
  {lines_str}

  <!-- System Boundary Box -->
  <rect x="360" y="110" width="1510" height="980" rx="16" fill="#ffffff" fill-opacity="0.95" stroke="#2563eb" stroke-width="2.5" filter="url(#shadow)"/>
  
  <!-- Boundary Header Tag -->
  <rect x="390" y="130" width="220" height="38" rx="8" fill="#2563eb"/>
  <text x="500" y="155" text-anchor="middle" font-size="16" font-weight="bold" fill="#ffffff">Research Rover</text>
  <text x="630" y="155" font-size="13" font-weight="500" fill="#64748b">(System Boundary)</text>

  <!-- Left: Actor Stick Figure -->
  <g id="actor_user" transform="translate(140, 500)">
    <!-- Head -->
    <circle cx="80" cy="40" r="26" fill="#eff6ff" stroke="#1d4ed8" stroke-width="2.8"/>
    <!-- Body -->
    <line x1="80" y1="66" x2="80" y2="140" stroke="#1d4ed8" stroke-width="4.0" stroke-linecap="round"/>
    <!-- Arms -->
    <line x1="25" y1="95" x2="135" y2="95" stroke="#1d4ed8" stroke-width="4.0" stroke-linecap="round"/>
    <!-- Legs -->
    <line x1="80" y1="140" x2="35" y2="210" stroke="#1d4ed8" stroke-width="4.0" stroke-linecap="round"/>
    <line x1="80" y1="140" x2="125" y2="210" stroke="#1d4ed8" stroke-width="4.0" stroke-linecap="round"/>
    <!-- Label -->
    <text x="80" y="240" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">Researcher / Student</text>
    <text x="80" y="260" text-anchor="middle" font-size="12" font-weight="500" fill="#64748b">(Primary Actor)</text>
  </g>

  <!-- Redraw association lines on top for crispness -->
  {lines_str}

  <!-- Use Case Ovals -->
  {ovals_str}
</svg>'''

# ==============================================================================
# 3. HIGH-RESOLUTION MATPLOTLIB RENDERER (PNG & PDF)
# ==============================================================================
def render_matplotlib(png_path, pdf_path):
    fig, ax = plt.subplots(figsize=(20, 12), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Top Title Banner
    title_box = FancyBboxPatch((0.5, 11.2), 19.0, 0.6, boxstyle="round,pad=0,rounding_size=0.1",
                               facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
    ax.add_patch(title_box)
    ax.text(0.8, 11.5, "Research Rover: Simple User Use Case Diagram", fontsize=13, fontweight='bold', color="#0F172A", va='center')
    ax.text(19.2, 11.5, "Student & Researcher Functional Model", fontsize=10, color="#64748B", ha='right', va='center')

    # System Boundary Rectangle
    boundary = FancyBboxPatch((3.8, 0.6), 15.7, 10.3, boxstyle="round,pad=0,rounding_size=0.2",
                              facecolor="#FFFFFF", edgecolor="#2563EB", linewidth=2.5, zorder=2)
    ax.add_patch(boundary)

    # Boundary Label Badge
    tag = FancyBboxPatch((4.2, 10.2), 3.2, 0.5, boxstyle="round,pad=0,rounding_size=0.1",
                         facecolor="#2563EB", edgecolor="none", zorder=3)
    ax.add_patch(tag)
    ax.text(5.8, 10.45, "Research Rover", fontsize=12, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=4)
    ax.text(7.6, 10.45, "(System Boundary)", fontsize=9.5, color="#64748B", va='center', zorder=4)

    # Actor Stick Figure on Left
    actor_x = 2.0
    actor_y = 6.0
    
    # Head
    head = Circle((actor_x, actor_y + 0.9), 0.32, facecolor="#EFF6FF", edgecolor="#1D4ED8", linewidth=2.5, zorder=5)
    ax.add_patch(head)
    # Body
    ax.plot([actor_x, actor_x], [actor_y + 0.58, actor_y - 0.25], color="#1D4ED8", linewidth=3.5, solid_capstyle='round', zorder=5)
    # Arms
    ax.plot([actor_x - 0.65, actor_x + 0.65], [actor_y + 0.25, actor_y + 0.25], color="#1D4ED8", linewidth=3.5, solid_capstyle='round', zorder=5)
    # Legs
    ax.plot([actor_x, actor_x - 0.5], [actor_y - 0.25, actor_y - 1.1], color="#1D4ED8", linewidth=3.5, solid_capstyle='round', zorder=5)
    ax.plot([actor_x, actor_x + 0.5], [actor_y - 0.25, actor_y - 1.1], color="#1D4ED8", linewidth=3.5, solid_capstyle='round', zorder=5)
    # Text
    ax.text(actor_x, actor_y - 1.45, "Researcher / Student", fontsize=11.5, fontweight='bold', color="#0F172A", ha='center', va='center', zorder=5)
    ax.text(actor_x, actor_y - 1.75, "(Primary User)", fontsize=9, color="#64748B", ha='center', va='center', zorder=5)

    # Use Cases (21 in 3 balanced columns of 7)
    usecases = [
        # Col 1 (x=6.4)
        (6.4, 9.4, "Search Research Papers"),
        (6.4, 8.1, "Explore Research Papers"),
        (6.4, 6.8, "View Paper Details"),
        (6.4, 5.5, "Download Research Papers"),
        (6.4, 4.2, "Upload Dataset"),
        (6.4, 2.9, "View My Datasets"),
        (6.4, 1.6, "Select Dataset"),

        # Col 2 (x=11.5)
        (11.5, 9.4, "Download Dataset"),
        (11.5, 8.1, "Explore Keywords"),
        (11.5, 6.8, "View Popular Keywords"),
        (11.5, 5.5, "Explore Keyword Connections"),
        (11.5, 4.2, "View Keyword Networks"),
        (11.5, 2.9, "Explore Countries"),
        (11.5, 1.6, "View Country Rankings"),

        # Col 3 (x=16.6)
        (16.6, 9.4, "Explore World Map"),
        (16.6, 8.1, "View International Collaborations"),
        (16.6, 6.8, "Ask Questions"),
        (16.6, 5.5, "Get AI Answers"),
        (16.6, 4.2, "Explore Research Information"),
        (16.6, 2.9, "Download Charts"),
        (16.6, 1.6, "Export Reports"),
    ]

    oval_width = 3.2
    oval_height = 0.82

    # Draw Association Lines
    origin_x = actor_x + 0.65
    origin_y = actor_y + 0.25
    for (cx, cy, title) in usecases:
        target_x = cx - oval_width / 2
        target_y = cy
        ax.plot([origin_x, target_x], [origin_y, target_y], color="#3B82F6", linewidth=1.4, alpha=0.8, zorder=3)

    # Draw Oval Shapes
    for (cx, cy, title) in usecases:
        box = FancyBboxPatch(
            (cx - oval_width/2, cy - oval_height/2), oval_width, oval_height,
            boxstyle=f"round,pad=0,rounding_size={oval_height/2}",
            facecolor="#F8FAFC",
            edgecolor="#2563EB",
            linewidth=1.8,
            zorder=4
        )
        ax.add_patch(box)
        
        # Split 3-word titles onto 2 lines if needed
        words = title.split()
        if len(words) >= 3 and len(title) > 20:
            mid = len(words) // 2 + 1
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            ax.text(cx, cy + 0.12, line1, ha='center', va='center', fontsize=9.2, fontweight='bold', color="#0F172A", zorder=6)
            ax.text(cx, cy - 0.14, line2, ha='center', va='center', fontsize=9.2, fontweight='bold', color="#0F172A", zorder=6)
        else:
            ax.text(cx, cy, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=6)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(pdf_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated PNG: {png_path}")
    print(f"Generated PDF: {pdf_path}")

def main():
    base_dir = Path("E:/Research_Rover")
    uml_dir = base_dir / "docs" / "uml"
    pub_dir = base_dir / "frontend" / "public" / "assets" / "uml"
    
    for d in [uml_dir, pub_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    stem = "Research_Rover_Simple_User_Use_Case_Diagram"
    
    # 1. PUML
    puml_code = get_plantuml_code()
    for d in [base_dir, uml_dir, pub_dir]:
        p = d / f"{stem}.puml"
        p.write_text(puml_code, encoding='utf-8')
        print(f"Wrote PUML: {p}")
        
    # 2. SVG
    svg_code = get_svg_code()
    for d in [base_dir, uml_dir, pub_dir]:
        s = d / f"{stem}.svg"
        s.write_text(svg_code, encoding='utf-8')
        print(f"Wrote SVG:  {s}")
        
    # 3. PNG & PDF via Matplotlib
    png_path = base_dir / f"{stem}.png"
    pdf_path = base_dir / f"{stem}.pdf"
    render_matplotlib(png_path, pdf_path)
    
    for d in [uml_dir, pub_dir]:
        shutil.copy2(png_path, d / f"{stem}.png")
        shutil.copy2(pdf_path, d / f"{stem}.pdf")
        
    print(f"\n[SUCCESS] Generated all 4 deliverables for {stem}!")

if __name__ == '__main__':
    main()
