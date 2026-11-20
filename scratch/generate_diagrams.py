"""
Research Rover Presentation Diagrams Generator
Generates pristine, publication-grade SVGs and renders them to 1920x1080 PNGs
using resvg-py.
"""

import os
import resvg_py
from PIL import Image

BASE_DIR = os.path.abspath("Research_Rover_Presentation_Assets")
SVG_DIR = os.path.join(BASE_DIR, "01_Diagrams_SVG")
PNG_DIR = os.path.join(BASE_DIR, "02_Diagrams_PNG")
PREVIEW_DIR = os.path.join(BASE_DIR, "03_Preview")

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)


def save_and_render(name: str, svg_content: str):
    svg_path = os.path.join(SVG_DIR, f"{name}.svg")
    png_path = os.path.join(PNG_DIR, f"{name}.png")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

    # Render PNG via resvg-py at native resolution (1920x1080)
    png_bytes = resvg_py.svg_to_bytes(svg_content.strip())
    with open(png_path, "wb") as f:
        f.write(png_bytes)

    size_kb = len(png_bytes) / 1024
    print(f"Generated {name}: SVG -> {svg_path}, PNG -> {png_path} ({size_kb:.1f} KB)")


# ---------------------------------------------------------------------------
# DIAGRAM 01: PROBLEM STATEMENT
# Target Slide: Slide 2 — Research Publication Challenges
# ---------------------------------------------------------------------------
def generate_diagram_01():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    <style>
      .title-tag { font-family: Arial, 'Segoe UI', sans-serif; font-size: 14px; font-weight: 700; fill: #138C8C; letter-spacing: 2px; text-transform: uppercase; }
      .main-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 34px; font-weight: 800; fill: #142B65; }
      .sub-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 16px; fill: #475569; }
      .sec-hdr { font-family: Arial, 'Segoe UI', sans-serif; font-size: 18px; font-weight: 700; fill: #142B65; letter-spacing: 1px; }
      .card-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 16px; font-weight: 700; fill: #142B65; }
      .card-desc { font-family: Arial, 'Segoe UI', sans-serif; font-size: 13.5px; fill: #334155; line-height: 1.4; }
      .sol-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 24px; font-weight: 800; fill: #FFFFFF; }
      .sol-subtitle { font-family: Arial, 'Segoe UI', sans-serif; font-size: 14px; fill: #99F6E4; letter-spacing: 0.5px; }
      .sol-cap-title { font-family: Arial, 'Segoe UI', sans-serif; font-size: 15px; font-weight: 700; fill: #142B65; }
      .sol-cap-desc { font-family: Arial, 'Segoe UI', sans-serif; font-size: 12.5px; fill: #475569; }
      .badge-txt { font-family: Arial, 'Segoe UI', sans-serif; font-size: 13px; font-weight: 700; fill: #FFFFFF; }
      .footer-txt { font-family: Arial, 'Segoe UI', sans-serif; font-size: 13px; fill: #64748B; }
    </style>
    <filter id="card-shadow" x="-3%" y="-3%" width="106%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.05" />
    </filter>
    <filter id="hero-shadow" x="-4%" y="-3%" width="108%" height="108%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#142B65" flood-opacity="0.16" />
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#138C8C" />
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1920" height="1080" fill="#FFFFFF" />
  
  <!-- Subtle Header Border Line -->
  <line x1="80" y1="140" x2="1840" y2="140" stroke="#E2E8F0" stroke-width="1.5" />

  <!-- Slide Header -->
  <g transform="translate(80, 55)">
    <text x="0" y="20" class="title-tag">Target: Slide 2 · Research Publication Challenges</text>
    <text x="0" y="58" class="main-title">Problem Statement &amp; Motivation</text>
    <text x="0" y="82" class="sub-title">Addressing critical bottlenecks in biomedical research discovery, metadata curation, and bibliometric intelligence</text>
  </g>

  <!-- LEFT PANEL: The 4 Key Challenges (2x2 Grid) -->
  <g transform="translate(80, 165)">
    <!-- Section Label -->
    <rect x="0" y="0" width="840" height="42" rx="8" fill="#F1F5F9" />
    <circle cx="24" cy="21" r="7" fill="#EF4444" />
    <text x="42" y="26" class="sec-hdr">CURRENT RESEARCH CHALLENGES</text>

    <!-- Challenge 1: Information Overload -->
    <g transform="translate(0, 58)">
      <rect width="405" height="340" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#card-shadow)" />
      <!-- Card top banner accent -->
      <path d="M 0 14 Q 0 0 14 0 L 391 0 Q 405 0 405 14 L 405 6 Q 405 0 391 0 L 14 0 Q 0 0 0 6 Z" fill="#142B65" />
      <circle cx="50" cy="55" r="26" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <!-- Icon: Stacked papers overload -->
      <path d="M 40 46 L 60 46 L 60 64 L 40 64 Z" fill="none" stroke="#142B65" stroke-width="2" stroke-linecap="round" />
      <path d="M 45 42 L 65 42 L 65 58" fill="none" stroke="#138C8C" stroke-width="2" stroke-linecap="round" />
      <path d="M 45 52 L 55 52 M 45 57 L 53 57" stroke="#142B65" stroke-width="1.5" stroke-linecap="round" />
      <text x="92" y="52" class="card-title">1. INFORMATION OVERLOAD</text>
      <text x="92" y="70" font-family="Arial" font-size="12px" font-weight="bold" fill="#EF4444">High Publication Volume</text>
      
      <foreignObject x="30" y="105" width="345" height="150">
        <p xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14.5px; color: #334155; line-height: 1.5; margin: 0;">
          Difficulty managing large volumes of research publications. Exponential growth in scientific literature overwhelms manual review, creating severe cognitive overload and discovery bottlenecks.
        </p>
      </foreignObject>
      <rect x="30" y="275" width="345" height="36" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="45" y="298" font-family="Arial" font-size="12px" fill="#64748B" font-weight="600">Impact: Relevant findings missed; manual search fails</text>
    </g>

    <!-- Challenge 2: Fragmented Data Sources -->
    <g transform="translate(435, 58)">
      <rect width="405" height="340" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#card-shadow)" />
      <circle cx="50" cy="55" r="26" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <!-- Icon: Disconnected nodes -->
      <circle cx="43" cy="50" r="4" fill="#142B65" />
      <circle cx="58" cy="46" r="4" fill="#138C8C" />
      <circle cx="52" cy="64" r="4" fill="#D99A32" />
      <line x1="43" y1="50" x2="58" y2="46" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,2" />
      <line x1="43" y1="50" x2="52" y2="64" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="3,2" />
      <text x="92" y="52" class="card-title">2. FRAGMENTED SOURCES</text>
      <text x="92" y="70" font-family="Arial" font-size="12px" font-weight="bold" fill="#EF4444">Disconnected Repositories</text>
      
      <foreignObject x="30" y="105" width="345" height="150">
        <p xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14.5px; color: #334155; line-height: 1.5; margin: 0;">
          Disconnected repositories and publication metadata. Bibliographic data resides in isolated silos (PubMed, OpenAlex, institutional archives) with incompatible schemas and varying standards.
        </p>
      </foreignObject>
      <rect x="30" y="275" width="345" height="36" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="45" y="298" font-family="Arial" font-size="12px" fill="#64748B" font-weight="600">Impact: Siloed metadata; incomplete research context</text>
    </g>

    <!-- Challenge 3: Manual Metadata Processing -->
    <g transform="translate(0, 420)">
      <rect width="405" height="340" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#card-shadow)" />
      <circle cx="50" cy="55" r="26" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <!-- Icon: Manual gear / funnel -->
      <path d="M 42 45 L 58 45 L 53 55 L 53 65 L 47 65 L 47 55 Z" fill="none" stroke="#142B65" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="50" cy="52" r="3" fill="#138C8C" />
      <text x="92" y="52" class="card-title">3. MANUAL PROCESSING</text>
      <text x="92" y="70" font-family="Arial" font-size="12px" font-weight="bold" fill="#EF4444">Time-Consuming Cleaning</text>
      
      <foreignObject x="30" y="105" width="345" height="150">
        <p xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14.5px; color: #334155; line-height: 1.5; margin: 0;">
          Time-consuming metadata extraction and cleaning. Raw exports require extensive manual wrangling to normalize inconsistent author names, affiliations, publication dates, and keyword strings.
        </p>
      </foreignObject>
      <rect x="30" y="275" width="345" height="36" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="45" y="298" font-family="Arial" font-size="12px" fill="#64748B" font-weight="600">Impact: High error rate; hundreds of hours lost</text>
    </g>

    <!-- Challenge 4: Limited Analytical Visibility -->
    <g transform="translate(435, 420)">
      <rect width="405" height="340" rx="14" fill="#F4F6F8" stroke="#CBD5E1" stroke-width="1.5" filter="url(#card-shadow)" />
      <circle cx="50" cy="55" r="26" fill="#EAF3F8" stroke="#142B65" stroke-width="2" />
      <!-- Icon: Bar chart with cross/restricted eye -->
      <rect x="40" y="56" width="5" height="10" fill="#142B65" />
      <rect x="48" y="50" width="5" height="16" fill="#142B65" />
      <rect x="56" y="44" width="5" height="22" fill="#138C8C" />
      <line x1="38" y1="67" x2="64" y2="43" stroke="#EF4444" stroke-width="2" stroke-linecap="round" />
      <text x="92" y="52" class="card-title">4. LIMITED VISIBILITY</text>
      <text x="92" y="70" font-family="Arial" font-size="12px" font-weight="bold" fill="#EF4444">Lack of Integrated Insights</text>
      
      <foreignObject x="30" y="105" width="345" height="150">
        <p xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14.5px; color: #334155; line-height: 1.5; margin: 0;">
          Lack of integrated bibliometric insights. Without automated co-occurrence networks, institutional geoparsing, and trend analysis, researchers struggle to spot emerging patterns and collaboration ties.
        </p>
      </foreignObject>
      <rect x="30" y="275" width="345" height="36" rx="8" fill="#FFFFFF" stroke="#E2E8F0" />
      <text x="45" y="298" font-family="Arial" font-size="12px" fill="#64748B" font-weight="600">Impact: Blind spots in research landscape &amp; trends</text>
    </g>
  </g>

  <!-- CENTER BRIDGE: Central Motivation -->
  <g transform="translate(945, 480)">
    <!-- Connecting flow arrows -->
    <path d="M 0 50 L 50 50" stroke="#138C8C" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow)" />
    
    <g transform="translate(55, 0)">
      <rect width="180" height="100" rx="14" fill="#142B65" filter="url(#card-shadow)" />
      <text x="90" y="32" font-family="Arial" font-size="11px" font-weight="700" fill="#138C8C" text-anchor="middle" letter-spacing="1.5px">CENTRAL MOTIVATION</text>
      <text x="90" y="58" font-family="Arial" font-size="14.5px" font-weight="800" fill="#FFFFFF" text-anchor="middle">Need for an</text>
      <text x="90" y="78" font-family="Arial" font-size="14.5px" font-weight="800" fill="#99F6E4" text-anchor="middle">Integrated Workflow</text>
    </g>

    <path d="M 240 50 L 290 50" stroke="#138C8C" stroke-width="3" marker-end="url(#arrow)" />
  </g>

  <!-- RIGHT PANEL: Research Rover Solution Block -->
  <g transform="translate(1260, 165)">
    <!-- Section Label -->
    <rect x="0" y="0" width="580" height="42" rx="8" fill="#EAF3F8" />
    <circle cx="24" cy="21" r="7" fill="#138C8C" />
    <text x="42" y="26" class="sec-hdr" fill="#142B65">INTEGRATED SOLUTION PLATFORM</text>

    <!-- Main Solution Card -->
    <g transform="translate(0, 58)">
      <rect width="580" height="702" rx="16" fill="#142B65" filter="url(#hero-shadow)" />
      
      <!-- Card Header Inside -->
      <g transform="translate(35, 35)">
        <rect width="130" height="26" rx="6" fill="#138C8C" />
        <text x="65" y="17" class="badge-txt" text-anchor="middle">RESEARCH ROVER</text>
        <text x="0" y="60" class="sol-title">Unified Discovery Platform</text>
        <text x="0" y="82" class="sol-subtitle">Automating Paper Retrieval, Curation &amp; Bibliometric Analytics</text>
      </g>

      <line x1="35" y1="145" x2="545" y2="145" stroke="#1E3A8A" stroke-width="1.5" />

      <!-- Subhead for capabilities -->
      <text x="35" y="175" font-family="Arial" font-size="14px" font-weight="700" fill="#93C5FD" letter-spacing="1px">CORE OUTPUT CAPABILITIES</text>

      <!-- Capability 1 -->
      <g transform="translate(35, 195)">
        <rect width="510" height="105" rx="10" fill="#FFFFFF" />
        <rect x="0" y="0" width="8" height="105" rx="4" fill="#138C8C" />
        <circle cx="45" cy="52" r="20" fill="#EAF3F8" />
        <path d="M 40 47 A 5 5 0 1 1 50 47 A 5 5 0 1 1 40 47 M 49 51 L 55 57" fill="none" stroke="#138C8C" stroke-width="2" stroke-linecap="round" />
        <text x="80" y="42" class="sol-cap-title">Research Paper Retrieval</text>
        <text x="80" y="64" class="sol-cap-desc">Direct querying of PubMed / NCBI E-utilities and OpenAlex APIs.</text>
        <text x="80" y="82" class="sol-cap-desc" font-weight="600" fill="#138C8C">Multi-source unified discovery with instant CSV exports.</text>
      </g>

      <!-- Capability 2 -->
      <g transform="translate(35, 315)">
        <rect width="510" height="105" rx="10" fill="#FFFFFF" />
        <rect x="0" y="0" width="8" height="105" rx="4" fill="#138C8C" />
        <circle cx="45" cy="52" r="20" fill="#EAF3F8" />
        <rect x="37" y="43" width="16" height="18" rx="2" fill="none" stroke="#138C8C" stroke-width="2" />
        <line x1="41" y1="48" x2="49" y2="48" stroke="#138C8C" stroke-width="1.5" />
        <line x1="41" y1="53" x2="49" y2="53" stroke="#138C8C" stroke-width="1.5" />
        <text x="80" y="42" class="sol-cap-title">Metadata Processing</text>
        <text x="80" y="64" class="sol-cap-desc">Automated XML parsing, canonical schema mapping &amp; deduplication.</text>
        <text x="80" y="82" class="sol-cap-desc" font-weight="600" fill="#138C8C">Intelligent column detection across Scopus, WoS and custom CSVs.</text>
      </g>

      <!-- Capability 3 -->
      <g transform="translate(35, 435)">
        <rect width="510" height="105" rx="10" fill="#FFFFFF" />
        <rect x="0" y="0" width="8" height="105" rx="4" fill="#138C8C" />
        <circle cx="45" cy="52" r="20" fill="#EAF3F8" />
        <circle cx="40" cy="50" r="3.5" fill="#138C8C" />
        <circle cx="51" cy="44" r="3.5" fill="#142B65" />
        <circle cx="49" cy="58" r="3.5" fill="#138C8C" />
        <line x1="40" y1="50" x2="51" y2="44" stroke="#138C8C" stroke-width="1.5" />
        <line x1="40" y1="50" x2="49" y2="58" stroke="#138C8C" stroke-width="1.5" />
        <line x1="51" y1="44" x2="49" y2="58" stroke="#138C8C" stroke-width="1.5" />
        <text x="80" y="42" class="sol-cap-title">Bibliometric Analysis</text>
        <text x="80" y="64" class="sol-cap-desc">Keyword frequency tables, co-occurrence matrices &amp; centralities.</text>
        <text x="80" y="82" class="sol-cap-desc" font-weight="600" fill="#138C8C">Institutional collaboration networks and geographic publication density.</text>
      </g>

      <!-- Capability 4 -->
      <g transform="translate(35, 555)">
        <rect width="510" height="105" rx="10" fill="#FFFFFF" />
        <rect x="0" y="0" width="8" height="105" rx="4" fill="#138C8C" />
        <circle cx="45" cy="52" r="20" fill="#EAF3F8" />
        <circle cx="45" cy="52" r="10" fill="none" stroke="#138C8C" stroke-width="2" />
        <line x1="35" y1="52" x2="55" y2="52" stroke="#138C8C" stroke-width="1.5" />
        <path d="M 45 42 A 10 7 0 0 1 45 62 A 10 7 0 0 1 45 42" fill="none" stroke="#138C8C" stroke-width="1.5" />
        <text x="80" y="42" class="sol-cap-title">Research Visualization</text>
        <text x="80" y="64" class="sol-cap-desc">Interactive 2D World Maps, 3D Globe, dynamic force networks,</text>
        <text x="80" y="82" class="sol-cap-desc" font-weight="600" fill="#138C8C">and AI-assisted conversational question answering.</text>
      </g>
    </g>
  </g>

  <!-- Presentation Footer Metadata -->
  <g transform="translate(80, 1025)">
    <text x="0" y="16" class="footer-txt">Research Rover: An Intelligent Research Discovery and Bibliometric Analysis Platform · M.Tech Data Science</text>
    <text x="1760" y="16" class="footer-txt" text-anchor="end">Slide 2 Diagram</text>
  </g>
</svg>"""
    save_and_render("01_problem_statement", svg)


if __name__ == "__main__":
    generate_diagram_01()
