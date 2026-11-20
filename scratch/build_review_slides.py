"""
Build script for the 3 Technical Presentation Slides for Research Rover M.Tech Project Review.
Generates:
  - Slide 1: Problem Formulation & Literature Review (SVG + PNG 1920x1080)
  - Slide 2: Methodology & Technical Implementation (SVG + PNG 1920x1080)
  - Slide 3: Preliminary Results & Analysis (SVG + PNG 1920x1080)
  - Multi-slide preview contact sheet (PNG)
  - Responsive HTML gallery
  - Complete README.md documentation
"""

import os
import re
import resvg_py
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath("Research_Rover_Review_Slides")
SLIDE_1_DIR = os.path.join(BASE_DIR, "02_Slide_1_Problem_Formulation")
SLIDE_2_DIR = os.path.join(BASE_DIR, "03_Slide_2_Methodology")
SLIDE_3_DIR = os.path.join(BASE_DIR, "04_Slide_3_Preliminary_Results")
PREVIEW_DIR = os.path.join(BASE_DIR, "05_Preview")

os.makedirs(SLIDE_1_DIR, exist_ok=True)
os.makedirs(SLIDE_2_DIR, exist_ok=True)
os.makedirs(SLIDE_3_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# COLOR PALETTE TOKENS
# ---------------------------------------------------------------------------
NAVY = "#142B65"
TEAL = "#138C8C"
LIGHT_BLUE = "#EAF3F8"
LIGHT_GREY = "#F4F6F8"
WHITE = "#FFFFFF"
GREEN = "#23865A"   # Implemented & verified
AMBER = "#D99A32"   # Under development
DARK_TEXT = "#0F172A"
MUTED_TEXT = "#475569"
BORDER_COLOR = "#CBD5E1"
CARD_BORDER = "#E2E8F0"
BLUE_ACCENT = "#1D4ED8"

# ---------------------------------------------------------------------------
# COMMON SVG HEADER & DEFS (NO FOREIGNOBJECT - 100% POWERPOINT COMPATIBLE)
# ---------------------------------------------------------------------------
COMMON_DEFS = f"""
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <filter id="card-hover" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.12"/>
    </filter>
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{NAVY}"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </linearGradient>
    <linearGradient id="teal-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{TEAL}"/>
      <stop offset="100%" stop-color="#0E7490"/>
    </linearGradient>
    <linearGradient id="blue-pill" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{LIGHT_BLUE}"/>
      <stop offset="100%" stop-color="#E0EDF5"/>
    </linearGradient>
  </defs>
"""

def make_header(category: str, title: str, subtitle: str, slide_num: int) -> str:
    return f"""
  <!-- Slide Header Banner -->
  <rect x="0" y="0" width="1920" height="110" fill="url(#header-grad)" />
  <rect x="0" y="106" width="1920" height="4" fill="{TEAL}" />

  <!-- Category & Slide Badge -->
  <g transform="translate(60, 24)">
    <rect x="0" y="0" width="460" height="26" rx="13" fill="{TEAL}" fill-opacity="0.25" stroke="{TEAL}" stroke-width="1.2" />
    <text x="230" y="18" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#E0F2FE" text-anchor="middle" letter-spacing="1">
      {category}
    </text>
  </g>

  <!-- Slide Counter Pill -->
  <g transform="translate(1720, 24)">
    <rect x="0" y="0" width="140" height="26" rx="13" fill="#FFFFFF" fill-opacity="0.15" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="1" />
    <text x="70" y="18" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">
      SLIDE {slide_num} OF 3
    </text>
  </g>

  <!-- Main Slide Title -->
  <text x="60" y="80" font-family="Arial, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF">
    {title}
  </text>
  <text x="60" y="100" font-family="Arial, sans-serif" font-size="14" font-weight="500" fill="#93C5FD">
    {subtitle}
  </text>
"""

# ===========================================================================
# SLIDE 1: PROBLEM FORMULATION & LITERATURE REVIEW
# ===========================================================================
def build_slide_01() -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {COMMON_DEFS}

  <!-- Slide Background -->
  <rect width="1920" height="1080" fill="{LIGHT_GREY}" />

  {make_header(
      "M.TECH DATA SCIENCE PROJECT REVIEW",
      "Problem Formulation &amp; Literature Review",
      "Addressing Information Overload, Fragmented Metadata Schemas, and the Discovery-to-Analytics Chasm",
      1
  )}

  <!-- ================= LEFT COLUMN: PROBLEM FORMULATION (x: 60, width: 850) ================= -->
  <g transform="translate(60, 130)">
    <!-- Section Header Badge -->
    <rect x="0" y="0" width="850" height="38" rx="8" fill="{NAVY}" />
    <text x="24" y="25" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART A — SCIENTIFIC RESEARCH CHALLENGES (PROBLEM FORMULATION)
    </text>
    <text x="830" y="25" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#93C5FD" text-anchor="end">
      4 CORE BOTTLENECKS
    </text>

    <!-- CHALLENGE 1: Information Overload (y: 50) -->
    <g transform="translate(0, 50)">
      <rect x="0" y="0" width="850" height="175" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="8" height="175" rx="4" fill="#DC2626" />
      
      <!-- Icon Container -->
      <rect x="24" y="20" width="46" height="46" rx="8" fill="#FEE2E2" />
      <!-- Book/Stack Icon -->
      <path d="M37 32 H57 V54 H37 Z M41 36 V50 M47 36 V50 M53 36 V50" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round"/>
      
      <text x="84" y="38" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="{NAVY}">
        1. Scientific Information Overload &amp; Discovery Fatigue
      </text>
      <text x="84" y="58" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#DC2626" letter-spacing="0.5">
        EXPONENTIAL LITERATURE EXPANSION · HIGH COGNITIVE RETRIEVAL FRICTION
      </text>

      <!-- Bullet Points -->
      <circle cx="92" cy="85" r="3.5" fill="#DC2626" />
      <text x="106" y="90" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Exponential Publication Volume:</tspan> Over 36 million citations in biomedical and data science repositories with over 1.5M added annually.
      </text>

      <circle cx="92" cy="113" r="3.5" fill="#DC2626" />
      <text x="106" y="118" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">High Query Friction:</tspan> Keyword queries frequently miss seminal papers due to lexical mismatches, unexpanded acronyms, and synonyms.
      </text>

      <circle cx="92" cy="141" r="3.5" fill="#DC2626" />
      <text x="106" y="146" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Impact on Researchers:</tspan> Critical prior work is frequently overlooked, leading to redundant research effort and inefficient synthesis.
      </text>
    </g>

    <!-- CHALLENGE 2: Fragmented Research Sources (y: 240) -->
    <g transform="translate(0, 240)">
      <rect x="0" y="0" width="850" height="175" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="8" height="175" rx="4" fill="{AMBER}" />
      
      <!-- Icon Container -->
      <rect x="24" y="20" width="46" height="46" rx="8" fill="#FEF3C7" />
      <!-- Disconnected Database Nodes Icon -->
      <circle cx="39" cy="38" r="5" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <circle cx="55" cy="38" r="5" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <circle cx="47" cy="52" r="5" fill="none" stroke="{AMBER}" stroke-width="2"/>
      <path d="M43 40 L51 40 M41 43 L45 49 M53 43 L49 49" stroke="{AMBER}" stroke-width="1.5"/>

      <text x="84" y="38" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="{NAVY}">
        2. Fragmented Research Sources &amp; Disparate Metadata
      </text>
      <text x="84" y="58" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="{AMBER}" letter-spacing="0.5">
        HETEROGENEOUS SCHEMAS · REPOSITORY ISOLATION (PUBMED, SCOPUS, WOS, OPENALEX)
      </text>

      <!-- Bullet Points -->
      <circle cx="92" cy="85" r="3.5" fill="{AMBER}" />
      <text x="106" y="90" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Database Heterogeneity:</tspan> Metadata is siloed across PubMed (XML), Scopus (CSV), Web of Science (TXT/CSV), and OpenAlex (JSON/CSV).
      </text>

      <circle cx="92" cy="113" r="3.5" fill="{AMBER}" />
      <text x="106" y="118" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Incompatible Column Schemas:</tspan> Identical concepts named differently (e.g., &quot;DOI&quot; vs &quot;Doi&quot; vs &quot;doi&quot;; &quot;Source&quot; vs &quot;Journal/Book&quot;).
      </text>

      <circle cx="92" cy="141" r="3.5" fill="{AMBER}" />
      <text x="106" y="146" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Schema Lock-In:</tspan> Existing tools typically force researchers into a single proprietary ecosystem or fail entirely on external CSVs.
      </text>
    </g>

    <!-- CHALLENGE 3: Manual Metadata Processing (y: 430) -->
    <g transform="translate(0, 430)">
      <rect x="0" y="0" width="850" height="175" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="8" height="175" rx="4" fill="#8B5CF6" />
      
      <!-- Icon Container -->
      <rect x="24" y="20" width="46" height="46" rx="8" fill="#EDE9FE" />
      <!-- Filter/Hygiene Icon -->
      <path d="M37 32 H57 L49 43 V53 L45 51 V43 Z" fill="none" stroke="#8B5CF6" stroke-width="2" stroke-linecap="round"/>

      <text x="84" y="38" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="{NAVY}">
        3. Manual Metadata Processing &amp; Data Hygiene Deficits
      </text>
      <text x="84" y="58" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#8B5CF6" letter-spacing="0.5">
        TEDIOUS EXTRACTION · DUPLICATE CONTAMINATION · AFFILIATION COMPLEXITY
      </text>

      <!-- Bullet Points -->
      <circle cx="92" cy="85" r="3.5" fill="#8B5CF6" />
      <text x="106" y="90" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Labor-Intensive Extraction:</tspan> Manual identification of author affiliations, institution departments, and geographic coordinates.
      </text>

      <circle cx="92" cy="113" r="3.5" fill="#8B5CF6" />
      <text x="106" y="118" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Duplicate Contamination:</tspan> Identical papers re-indexed under varying titles or case variations severely distort statistical counts.
      </text>

      <circle cx="92" cy="141" r="3.5" fill="#8B5CF6" />
      <text x="106" y="146" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Absence of Quality Metrics:</tspan> Researchers lack automated methods to assess whether an ingested dataset is fit for downstream analysis.
      </text>
    </g>

    <!-- CHALLENGE 4: Limited Analytical Visibility (y: 620) -->
    <g transform="translate(0, 620)">
      <rect x="0" y="0" width="850" height="175" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="8" height="175" rx="4" fill="{TEAL}" />
      
      <!-- Icon Container -->
      <rect x="24" y="20" width="46" height="46" rx="8" fill="#CCFBF1" />
      <!-- Network Chart Icon -->
      <circle cx="47" cy="35" r="4" fill="none" stroke="{TEAL}" stroke-width="2"/>
      <circle cx="37" cy="51" r="4" fill="none" stroke="{TEAL}" stroke-width="2"/>
      <circle cx="57" cy="51" r="4" fill="none" stroke="{TEAL}" stroke-width="2"/>
      <path d="M45 38 L39 48 M49 38 L55 48 M41 51 L53 51" stroke="{TEAL}" stroke-width="1.5"/>

      <text x="84" y="38" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="{NAVY}">
        4. Limited Analytical Visibility &amp; Disconnected Exploration
      </text>
      <text x="84" y="58" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="{TEAL}" letter-spacing="0.5">
        ISOLATED SEARCH ENGINES · SEPARATE BIBLIOMETRICS TOOLS · ZERO INTERACTIVE AI
      </text>

      <!-- Bullet Points -->
      <circle cx="92" cy="85" r="3.5" fill="{TEAL}" />
      <text x="106" y="90" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Lack of Macro-Level Insights:</tspan> Standard search engines display flat list outputs; impossible to see keyword co-occurrence clusters.
      </text>

      <circle cx="92" cy="113" r="3.5" fill="{TEAL}" />
      <text x="106" y="118" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">Opaque Global Collaborations:</tspan> Geographic and institutional co-authorship networks remain hidden without specialized software.
      </text>

      <circle cx="92" cy="141" r="3.5" fill="{TEAL}" />
      <text x="106" y="146" font-family="Arial, sans-serif" font-size="13" font-weight="400" fill="{DARK_TEXT}">
        <tspan font-weight="700">No Semantic Interactivity:</tspan> Traditional bibliometric tools provide static plots but cannot answer natural-language research questions.
      </text>
    </g>
  </g>

  <!-- ================= RIGHT COLUMN: RESEARCH GAP & LITERATURE REVIEW (x: 940, width: 920) ================= -->
  <g transform="translate(940, 130)">
    
    <!-- PART B: THE RESEARCH GAP & INTEGRATION OBJECTIVE (y: 0 to 280) -->
    <rect x="0" y="0" width="920" height="38" rx="8" fill="{NAVY}" />
    <text x="24" y="25" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART B — RESEARCH GAP &amp; PROPOSED SYSTEM INTEGRATION
    </text>

    <!-- Comparison Container -->
    <g transform="translate(0, 50)">
      <rect x="0" y="0" width="920" height="230" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      
      <!-- Existing Disconnected Workflow (Left Sub-box) -->
      <g transform="translate(20, 18)">
        <rect x="0" y="0" width="425" height="194" rx="8" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1" />
        <rect x="0" y="0" width="425" height="30" rx="8" fill="#FFE4E6" />
        <text x="212" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#BE123C" text-anchor="middle">
          CONVENTIONAL DISCONNECTED WORKFLOW
        </text>

        <!-- Steps in conventional -->
        <g transform="translate(15, 42)">
          <rect x="0" y="0" width="395" height="28" rx="5" fill="{WHITE}" stroke="#FDA4AF" stroke-width="1"/>
          <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#9F1239">Step 1: Publication Retrieval</text>
          <text x="180" y="18" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">PubMed / Google Scholar (Flat list)</text>
        </g>
        <text x="212" y="82" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#BE123C" text-anchor="middle">↓ Manual CSV Export &amp; Custom Python Scripts</text>
        <g transform="translate(15, 92)">
          <rect x="0" y="0" width="395" height="28" rx="5" fill="{WHITE}" stroke="#FDA4AF" stroke-width="1"/>
          <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#9F1239">Step 2: Desktop Bibliometrics</text>
          <text x="180" y="18" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">VOSviewer / Bibliometrix (Offline tools)</text>
        </g>
        <text x="212" y="132" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#BE123C" text-anchor="middle">↓ Separate Disconnected Workflow</text>
        <g transform="translate(15, 142)">
          <rect x="0" y="0" width="395" height="28" rx="5" fill="{WHITE}" stroke="#FDA4AF" stroke-width="1"/>
          <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#9F1239">Step 3: Document Synthesis</text>
          <text x="180" y="18" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Generic LLMs (No citation provenance)</text>
        </g>
      </g>

      <!-- Research Rover Unified Workflow (Right Sub-box) -->
      <g transform="translate(475, 18)">
        <rect x="0" y="0" width="425" height="194" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1" />
        <rect x="0" y="0" width="425" height="30" rx="8" fill="#D1FAE5" />
        <text x="212" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#047857" text-anchor="middle">
          RESEARCH ROVER UNIFIED PLATFORM
        </text>

        <!-- 4 integrated capabilities -->
        <g transform="translate(15, 40)">
          <rect x="0" y="0" width="395" height="32" rx="6" fill="{WHITE}" stroke="#6EE7B7" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Unified Multi-Source Ingestion:</text>
          <text x="195" y="21" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Live PubMed API + Universal CSV Normalizer</text>
        </g>
        <g transform="translate(15, 76)">
          <rect x="0" y="0" width="395" height="32" rx="6" fill="{WHITE}" stroke="#6EE7B7" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Automated Quality &amp; Hygiene:</text>
          <text x="195" y="21" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Deduplication + Quality Score + Feature Readiness</text>
        </g>
        <g transform="translate(15, 112)">
          <rect x="0" y="0" width="395" height="32" rx="6" fill="{WHITE}" stroke="#6EE7B7" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Dual Analytical Engines:</text>
          <text x="195" y="21" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">NetworkX Graph Centrality + 2D/3D Country Maps</text>
        </g>
        <g transform="translate(15, 148)">
          <rect x="0" y="0" width="395" height="32" rx="6" fill="{WHITE}" stroke="#6EE7B7" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Grounded AI RAG Synthesis:</text>
          <text x="195" y="21" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">FAISS Dense Vectors + Cited Gemini Assistant</text>
        </g>
      </g>
    </g>

    <!-- PART C: LITERATURE REVIEW MATRIX (y: 300 to 795) -->
    <g transform="translate(0, 300)">
      <rect x="0" y="0" width="920" height="38" rx="8" fill="{NAVY}" />
      <text x="24" y="25" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
        PART C — LITERATURE REVIEW MATRIX (VERIFIED FOUNDATIONAL CITATIONS)
      </text>

      <!-- Table Wrapper -->
      <rect x="0" y="48" width="920" height="447" rx="10" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      
      <!-- Table Header -->
      <rect x="0" y="48" width="920" height="42" rx="10" fill="{LIGHT_BLUE}" />
      <line x1="0" y1="90" x2="920" y2="90" stroke="{BORDER_COLOR}" stroke-width="1.5" />
      
      <!-- Column Dividers -->
      <line x1="210" y1="48" x2="210" y2="495" stroke="{BORDER_COLOR}" stroke-width="1" stroke-dasharray="3,3" />
      <line x1="450" y1="48" x2="450" y2="495" stroke="{BORDER_COLOR}" stroke-width="1" stroke-dasharray="3,3" />
      <line x1="685" y1="48" x2="685" y2="495" stroke="{BORDER_COLOR}" stroke-width="1" stroke-dasharray="3,3" />

      <!-- Header Labels -->
      <text x="15" y="74" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">AUTHOR / YEAR / VENUE</text>
      <text x="225" y="74" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">MAIN CONTRIBUTION</text>
      <text x="465" y="74" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">LIMITATION / RESEARCH GAP</text>
      <text x="700" y="74" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">RELEVANCE TO ROVER</text>

      <!-- ROW 1: Van Eck & Waltman (2010) (y: 95) -->
      <g transform="translate(0, 95)">
        <text x="15" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="{NAVY}">Van Eck &amp; Waltman</text>
        <text x="15" y="40" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="{BLUE_ACCENT}">2010 · Scientometrics</text>
        <text x="15" y="58" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">&quot;Software survey: VOSviewer...&quot;</text>
        <rect x="15" y="70" width="135" height="18" rx="4" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
        <text x="82" y="83" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="{BLUE_ACCENT}" text-anchor="middle">Bibliometric Mapping</text>

        <!-- Main Contribution -->
        <text x="225" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">VOS Mapping &amp; Clustering:</text>
        <text x="225" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Introduced distance-based</text>
        <text x="225" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">co-occurrence clustering and</text>
        <text x="225" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">visualization methodology for</text>
        <text x="225" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">scientific keywords &amp; authors.</text>

        <!-- Limitation / Gap -->
        <text x="465" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#BE123C">Standalone Desktop Tool:</text>
        <text x="465" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Requires manual export files;</text>
        <text x="465" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">no live query retrieval API;</text>
        <text x="465" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">lacks interactive conversational</text>
        <text x="465" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">synthesis or AI Q&amp;A.</text>

        <!-- Relevance to Rover -->
        <text x="700" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">Co-occurrence &amp; Graphs:</text>
        <text x="700" y="38" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Forms the mathematical</text>
        <text x="700" y="54" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">foundation for Rover's keyword</text>
        <text x="700" y="70" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">matrix, NetworkX centrality,</text>
        <text x="700" y="86" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">and interactive SVG graphs.</text>
      </g>

      <line x1="0" y1="210" x2="920" y2="210" stroke="{BORDER_COLOR}" stroke-width="1" />

      <!-- ROW 2: Aria & Cuccurullo (2017) (y: 220) -->
      <g transform="translate(0, 220)">
        <text x="15" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="{NAVY}">Aria &amp; Cuccurullo</text>
        <text x="15" y="40" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="{BLUE_ACCENT}">2017 · J. Informetrics</text>
        <text x="15" y="58" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">&quot;bibliometrix: An R-package...&quot;</text>
        <rect x="15" y="70" width="135" height="18" rx="4" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
        <text x="82" y="83" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="{GREEN}" text-anchor="middle">Science Mapping (R)</text>

        <!-- Main Contribution -->
        <text x="225" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">Comprehensive Mapping:</text>
        <text x="225" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Programmatic R library for</text>
        <text x="225" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">bibliometric analysis, country</text>
        <text x="225" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">collaboration tracking, and</text>
        <text x="225" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">co-citation graph analytics.</text>

        <!-- Limitation / Gap -->
        <text x="465" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#BE123C">CLI &amp; Coding Barrier:</text>
        <text x="465" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Requires R runtime &amp; code</text>
        <text x="465" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">familiarity; separated from web</text>
        <text x="465" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">search UI; lacks semantic RAG</text>
        <text x="465" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">question-answering layer.</text>

        <!-- Relevance to Rover -->
        <text x="700" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">Country &amp; Macro Metrics:</text>
        <text x="700" y="38" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Directly guides Rover's</text>
        <text x="700" y="54" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">country affiliation extraction,</text>
        <text x="700" y="70" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">geographic maps, and web-</text>
        <text x="700" y="86" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">native bibliometric dashboards.</text>
      </g>

      <line x1="0" y1="330" x2="920" y2="330" stroke="{BORDER_COLOR}" stroke-width="1" />

      <!-- ROW 3: Lewis et al. (2020) (y: 340) -->
      <g transform="translate(0, 340)">
        <text x="15" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="{NAVY}">Lewis et al.</text>
        <text x="15" y="40" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="{BLUE_ACCENT}">2020 · NeurIPS</text>
        <text x="15" y="58" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">&quot;Retrieval-Augmented Gen...&quot;</text>
        <rect x="15" y="70" width="135" height="18" rx="4" fill="#FDF4FF" stroke="#F0ABFC" stroke-width="1"/>
        <text x="82" y="83" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#A21CAF" text-anchor="middle">RAG Paradigm</text>

        <!-- Main Contribution -->
        <text x="225" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">Dense Retrieval + LLM:</text>
        <text x="225" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Pioneered RAG framework</text>
        <text x="225" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">combining non-parametric vector</text>
        <text x="225" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">memory (dense search) with</text>
        <text x="225" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">parametric LLM generators.</text>

        <!-- Limitation / Gap -->
        <text x="465" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#BE123C">Generic Text Benchmark:</text>
        <text x="465" y="38" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">Evaluated on open QA; lacks</text>
        <text x="465" y="54" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">bibliometric graph integration,</text>
        <text x="465" y="70" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">multischema normalization,</text>
        <text x="465" y="86" font-family="Arial, sans-serif" font-size="11" fill="{MUTED_TEXT}">and citation provenance cards.</text>

        <!-- Relevance to Rover -->
        <text x="700" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">Semantic Assistant:</text>
        <text x="700" y="38" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Architectural blueprint for</text>
        <text x="700" y="54" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Rover's FAISS vector store,</text>
        <text x="700" y="70" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">HDBSCAN chunking, and cited</text>
        <text x="700" y="86" font-family="Arial, sans-serif" font-size="11" fill="{DARK_TEXT}">Gemini conversational Q&amp;A.</text>
      </g>

      <!-- Matrix Verification Sub-note -->
      <g transform="translate(10, 462)">
        <rect x="0" y="0" width="900" height="24" rx="4" fill="#F8FAFC" />
        <text x="450" y="16" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="{MUTED_TEXT}" text-anchor="middle">
          [Verified Foundational Citations in Scientometrics, Science Mapping &amp; Dense Retrieval-Augmented Generation]
        </text>
      </g>
    </g>
  </g>

  <!-- ================= BOTTOM BANNER: ONE CONCISE RESEARCH OBJECTIVE STATEMENT (y: 975) ================= -->
  <g transform="translate(60, 975)">
    <rect x="0" y="0" width="1800" height="78" rx="10" fill="{NAVY}" stroke="{TEAL}" stroke-width="1.8" filter="url(#shadow)" />
    <rect x="0" y="0" width="12" height="78" rx="4" fill="{TEAL}" />
    
    <!-- Target Icon -->
    <circle cx="38" cy="39" r="16" fill="none" stroke="{TEAL}" stroke-width="2.5"/>
    <circle cx="38" cy="39" r="8" fill="{TEAL}"/>
    <circle cx="38" cy="39" r="3" fill="{WHITE}"/>

    <text x="68" y="30" font-family="Arial, sans-serif" font-size="13" font-weight="800" fill="{TEAL}" letter-spacing="1">
      OVERALL PROJECT RESEARCH OBJECTIVE
    </text>
    <text x="68" y="55" font-family="Arial, sans-serif" font-size="16" font-weight="600" fill="{WHITE}">
      &quot;To design, implement, and evaluate an integrated research discovery and bibliometric analysis platform that bridges the gap between publication retrieval, multi-source metadata normalization, network bibliometrics, and conversational AI-assisted synthesis.&quot;
    </text>
  </g>
</svg>"""
    return svg

# ===========================================================================
# SLIDE 2: METHODOLOGY & TECHNICAL IMPLEMENTATION
# ===========================================================================
def build_slide_02() -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {COMMON_DEFS}

  <!-- Slide Background -->
  <rect width="1920" height="1080" fill="{LIGHT_GREY}" />

  {make_header(
      "M.TECH DATA SCIENCE PROJECT REVIEW",
      "Methodology &amp; Technical Implementation",
      "End-to-End System Architecture, Dual-Path Ingestion Pipeline &amp; Verified Technology Stack",
      2
  )}

  <!-- ================= PART A: SIX-TIER CONNECTED SYSTEM ARCHITECTURE (y: 125, height: 430) ================= -->
  <g transform="translate(60, 125)">
    <!-- Header with status legend -->
    <rect x="0" y="0" width="1800" height="34" rx="6" fill="{NAVY}" />
    <text x="20" y="22" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART A — SIX-TIER CONNECTED SYSTEM ARCHITECTURE &amp; REPOSITORY COMPONENT MAPPING
    </text>
    
    <!-- Legend -->
    <g transform="translate(1420, 7)">
      <rect x="0" y="0" width="180" height="20" rx="4" fill="{GREEN}" />
      <text x="90" y="14" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">✓ IMPLEMENTED &amp; VERIFIED</text>
    </g>
    <g transform="translate(1615, 7)">
      <rect x="0" y="0" width="170" height="20" rx="4" fill="{AMBER}" />
      <text x="85" y="14" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">⏳ UNDER DEVELOPMENT</text>
    </g>

    <!-- 6 Connected Tier Cards across horizontal layout (each width: 285, gap: 18) -->
    <!-- TIER 1: User Interface (x: 0) -->
    <g transform="translate(0, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        1. USER INTERFACE TIER
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        React 18 · Vite · TypeScript · Tailwind
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ SearchPage &amp; Query Builder</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Keyword expansion, dates, stages 0–4</text>
      </g>
      <g transform="translate(12, 130)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Dataset Quality Modal</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Score 0–100, grade, feature checks</text>
      </g>
      <g transform="translate(12, 188)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ AnalyticsPage &amp; Word Cloud</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Keyword frequency &amp; presence matrix</text>
      </g>
      <g transform="translate(12, 246)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Country Visualizer (2D &amp; 3D)</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">TopoJSON World Map &amp; 3D globe</text>
      </g>
      <g transform="translate(12, 304)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ ChatPage (Cited Assistant)</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Conversational QA with [n] source cards</text>
      </g>
    </g>

    <!-- TIER 2: Backend Controllers (x: 303) -->
    <g transform="translate(303, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        2. BACKEND API CONTROLLERS
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        FastAPI · Pydantic · Uvicorn · AsyncIO
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ /api/v1/search</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Async search task, cancel &amp; progress</text>
      </g>
      <g transform="translate(12, 130)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ /api/v1/files</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Upload, download, CSV data &amp; quality</text>
      </g>
      <g transform="translate(12, 188)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ /api/v1/embeddings</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Vector indexing background dispatch</text>
      </g>
      <g transform="translate(12, 246)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ /api/v1/chat</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Synchronous RAG with Gemini LLM</text>
      </g>
      <g transform="translate(12, 304)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ /api/v1/analysis &amp; /system</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Summaries, matrices &amp; health checks</text>
      </g>
    </g>

    <!-- TIER 3: Data Collection (x: 606) -->
    <g transform="translate(606, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        3. DATA COLLECTION TIER
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        NCBI E-utilities · Crawl4ai · BS4
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="60" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Live PubMed E-utilities</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">esearch, efetch (batch 50 XML),</text>
        <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">esummary &amp; espell with backoff</text>
      </g>
      <g transform="translate(12, 140)">
        <rect x="0" y="0" width="261" height="60" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Universal CSV Ingestion</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">PubMed, Scopus, Web of Science,</text>
        <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">and OpenAlex tabular files</text>
      </g>
      <g transform="translate(12, 208)">
        <rect x="0" y="0" width="261" height="60" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Full-Text Web Scraper</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Domain-locked crawler with</text>
        <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">automated abstract fallback</text>
      </g>
      <g transform="translate(12, 280)">
        <rect x="0" y="0" width="261" height="65" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{AMBER}">⏳ CORE Academic API</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">SearchService._search_core</text>
        <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">currently stubbed ([]); live</text>
        <text x="10" y="60" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">retrieval uses PubMed.</text>
      </g>
    </g>

    <!-- TIER 4: Data Processing & Quality (x: 909) -->
    <g transform="translate(909, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        4. DATA PROCESSING &amp; QUALITY
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        Canonical Normalizer · Hygiene · Assessor
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ XML Parsing &amp; Extraction</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Title, abstract, author, DOI, PMID</text>
      </g>
      <g transform="translate(12, 130)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Canonical Normalizer</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Fuzzy mapping, preserves raw cols</text>
      </g>
      <g transform="translate(12, 188)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Deduplication &amp; Hygiene</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">DOI lowercase &amp; title hash pruning</text>
      </g>
      <g transform="translate(12, 246)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Affiliation Country Extractor</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Regex country &amp; ISO-3 mapping</text>
      </g>
      <g transform="translate(12, 304)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Quality Assessor</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Score (0–100), grades, readiness</text>
      </g>
    </g>

    <!-- TIER 5: Analytical & Intelligence (x: 1212) -->
    <g transform="translate(1212, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        5. ANALYTICAL &amp; AI ENGINE
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        NetworkX · FAISS · Transformers · Gemini
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Keyword &amp; Co-Occurrence</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Frequency &amp; presence matrix</text>
      </g>
      <g transform="translate(12, 130)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ NetworkX Centrality</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Degree, betweenness, closeness</text>
      </g>
      <g transform="translate(12, 188)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Country Link Analysis</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Bilateral co-authorship edge graph</text>
      </g>
      <g transform="translate(12, 246)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ HDBSCAN &amp; FAISS Vectors</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">all-mpnet-base-v2, IndexFlatL2</text>
      </g>
      <g transform="translate(12, 304)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ RAG Decomposition &amp; LLM</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Gemini 2.5 with [n] source citations</text>
      </g>
    </g>

    <!-- TIER 6: Visualization & Output (x: 1515) -->
    <g transform="translate(1515, 44)">
      <rect x="0" y="0" width="285" height="380" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="285" height="36" rx="8" fill="{NAVY}" />
      <text x="142" y="23" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">
        6. VISUALIZATION &amp; OUTPUT TIER
      </text>
      <text x="142" y="52" font-family="Arial, sans-serif" font-size="11" font-weight="600" fill="{BLUE_ACCENT}" text-anchor="middle">
        D3 · TopoJSON · SVG · CSV/JSON Export
      </text>
      <line x1="15" y1="62" x2="270" y2="62" stroke="{BORDER_COLOR}" stroke-width="1"/>

      <!-- Modules -->
      <g transform="translate(12, 72)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ SVG Force Network Graph</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Keyword co-occurrence pan &amp; zoom</text>
      </g>
      <g transform="translate(12, 130)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ 2D D3 Choropleth Map</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Country intensity &amp; hover metrics</text>
      </g>
      <g transform="translate(12, 188)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">✓ Clean Artifact Exports</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Clean CSV, sidecar JSON, mapping</text>
      </g>
      <g transform="translate(12, 246)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{AMBER}">⏳ Backend Analysis UI Wire</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Currently computes in-browser</text>
      </g>
      <g transform="translate(12, 304)">
        <rect x="0" y="0" width="261" height="50" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
        <text x="10" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{AMBER}">⏳ Real-Time Chat Stream</text>
        <text x="10" y="34" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Currently buffered response</text>
      </g>
    </g>

    <!-- Connector arrows across tiers -->
    <path d="M285 234 L303 234 M588 234 L606 234 M891 234 L909 234 M1194 234 L1212 234 M1497 234 L1515 234" 
          stroke="{TEAL}" stroke-width="2.5" fill="none" stroke-linecap="round" marker-end="url(#arrow)"/>
  </g>

  <!-- ================= PART B: METHODOLOGY WORKFLOW PIPELINE (y: 565, height: 265) ================= -->
  <g transform="translate(60, 565)">
    <!-- Section Header -->
    <rect x="0" y="0" width="1800" height="34" rx="6" fill="{NAVY}" />
    <text x="20" y="22" font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART B — END-TO-END METHODOLOGY &amp; DUAL-INGESTION WORKFLOW PIPELINE
    </text>

    <!-- Pipeline Container Box -->
    <rect x="0" y="42" width="1800" height="235" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />

    <!-- 1. Dual Ingestion Inputs (x: 15) -->
    <g transform="translate(20, 58)">
      <rect x="0" y="0" width="190" height="88" rx="6" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1.2"/>
      <text x="12" y="22" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">PATH A: Live Query</text>
      <text x="12" y="42" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Comma-separated query</text>
      <text x="12" y="58" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Date range filters</text>
      <text x="12" y="74" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• PubMed E-utilities search</text>

      <rect x="0" y="104" width="190" height="88" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.2"/>
      <text x="12" y="126" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{GREEN}">PATH B: CSV Upload</text>
      <text x="12" y="146" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• PubMed / Scopus export</text>
      <text x="12" y="162" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Web of Science / OpenAlex</text>
      <text x="12" y="178" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Custom research CSVs</text>
    </g>

    <path d="M220 155 L245 155" stroke="{TEAL}" stroke-width="2.5" fill="none" />

    <!-- 2. Dispatch & Ingestion (x: 250) -->
    <g transform="translate(250, 75)">
      <rect x="0" y="0" width="170" height="150" rx="6" fill="{LIGHT_GREY}" stroke="{BORDER_COLOR}" stroke-width="1.2"/>
      <rect x="0" y="0" width="170" height="26" rx="6" fill="{NAVY}"/>
      <text x="85" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">FastAPI Dispatch</text>
      <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="{DARK_TEXT}">• Request validation</text>
      <text x="10" y="68" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• File extension check</text>
      <text x="10" y="88" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• 50MB size limit</text>
      <text x="10" y="108" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Rate limiter &amp; retry</text>
      <text x="10" y="128" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Async background task</text>
    </g>

    <path d="M425 155 L450 155" stroke="{TEAL}" stroke-width="2.5" fill="none" />

    <!-- 3. Metadata Extraction & XML (x: 455) -->
    <g transform="translate(455, 75)">
      <rect x="0" y="0" width="175" height="150" rx="6" fill="{LIGHT_GREY}" stroke="{BORDER_COLOR}" stroke-width="1.2"/>
      <rect x="0" y="0" width="175" height="26" rx="6" fill="{NAVY}"/>
      <text x="87" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Metadata Extraction</text>
      <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="{DARK_TEXT}">• XML Article parsing</text>
      <text x="10" y="68" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Title, abstract, DOI</text>
      <text x="10" y="88" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• PMID, PMCID, year</text>
      <text x="10" y="108" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Authors &amp; affiliations</text>
      <text x="10" y="128" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• MeSH terms &amp; keywords</text>
    </g>

    <path d="M635 155 L660 155" stroke="{TEAL}" stroke-width="2.5" fill="none" />

    <!-- 4. Normalization & Hygiene (x: 665) -->
    <g transform="translate(665, 75)">
      <rect x="0" y="0" width="185" height="150" rx="6" fill="{LIGHT_GREY}" stroke="{BORDER_COLOR}" stroke-width="1.2"/>
      <rect x="0" y="0" width="185" height="26" rx="6" fill="{NAVY}"/>
      <text x="92" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Normalization &amp; Quality</text>
      <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="{DARK_TEXT}">• Canonical schema map</text>
      <text x="10" y="68" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Fuzzy header match</text>
      <text x="10" y="88" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• DOI &amp; title deduplication</text>
      <text x="10" y="108" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Quality Assessor (0–100)</text>
      <text x="10" y="128" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Feature readiness check</text>
    </g>

    <path d="M855 155 L880 155" stroke="{TEAL}" stroke-width="2.5" fill="none" />

    <!-- 5. Canonical Storage (x: 885) -->
    <g transform="translate(885, 75)">
      <rect x="0" y="0" width="170" height="150" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.2"/>
      <rect x="0" y="0" width="170" height="26" rx="6" fill="{GREEN}"/>
      <text x="85" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Structured Storage</text>
      <text x="10" y="48" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{GREEN}">data/ Folder Artifacts:</text>
      <text x="10" y="68" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• Clean &lt;name&gt;.csv</text>
      <text x="10" y="88" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• canonical_metadata.json</text>
      <text x="10" y="108" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• full_text_mapping.json</text>
      <text x="10" y="128" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• FAISS .index &amp; chunks</text>
    </g>

    <!-- Split Arrow to Dual Tracks -->
    <path d="M1060 155 L1085 155 M1085 155 L1085 105 L1110 105 M1085 155 L1085 205 L1110 205" stroke="{TEAL}" stroke-width="2" fill="none" />

    <!-- 6. Dual Processing Tracks (x: 1115) -->
    <!-- Track 1: Bibliometric Analysis (y: 58) -->
    <g transform="translate(1115, 58)">
      <rect x="0" y="0" width="310" height="92" rx="6" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1.2"/>
      <text x="12" y="22" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">TRACK 1: Bibliometrics &amp; Collaboration</text>
      <text x="12" y="40" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Keyword frequency aggregation &amp; presence matrix</text>
      <text x="12" y="56" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• NetworkX centralities (degree, betweenness, clustering)</text>
      <text x="12" y="72" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Author affiliations &amp; bilateral country edge links</text>
    </g>

    <!-- Track 2: Semantic AI Intelligence (y: 158) -->
    <g transform="translate(1115, 158)">
      <rect x="0" y="0" width="310" height="92" rx="6" fill="#FDF4FF" stroke="#F0ABFC" stroke-width="1.2"/>
      <text x="12" y="22" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#A21CAF">TRACK 2: Dense Vectors &amp; RAG Intelligence</text>
      <text x="12" y="40" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Sentence-Transformers (all-mpnet-base-v2, 768-d)</text>
      <text x="12" y="56" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• HDBSCAN semantic chunks &amp; 800-token capping</text>
      <text x="12" y="72" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• FAISS IndexFlatL2 similarity + Gemini cited Q&amp;A</text>
    </g>

    <!-- Convergence Arrow to Results -->
    <path d="M1430 105 L1455 105 L1455 155 L1480 155 M1430 205 L1455 205 L1455 155" stroke="{TEAL}" stroke-width="2" fill="none" />

    <!-- 7. Visualization & Synthesis (x: 1485) -->
    <g transform="translate(1485, 75)">
      <rect x="0" y="0" width="290" height="150" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.5"/>
      <rect x="0" y="0" width="290" height="26" rx="6" fill="{GREEN}"/>
      <text x="145" y="18" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Interactive Discovery &amp; Insights</text>
      <text x="12" y="48" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{GREEN}">Rendered UI Dashboards:</text>
      <text x="12" y="68" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• Interactive SVG force graph (zoom/pan)</text>
      <text x="12" y="88" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• D3 2D World Map &amp; 3D Collaboration Globe</text>
      <text x="12" y="108" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• Keyword presence matrix &amp; frequency charts</text>
      <text x="12" y="128" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• Context-grounded RAG chat with source cards</text>
    </g>
  </g>

  <!-- ================= PART C: COMPACT TECHNICAL IMPLEMENTATION STRIP (y: 890, height: 165) ================= -->
  <g transform="translate(60, 890)">
    <!-- Header -->
    <rect x="0" y="0" width="1800" height="30" rx="6" fill="{NAVY}" />
    <text x="20" y="20" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART C — TECHNICAL IMPLEMENTATION &amp; VERIFIED PRODUCTION STACK
    </text>

    <!-- 8 Tech Stack Cards (width: 215, gap: 11) -->
    <!-- Tech 1: Python -->
    <g transform="translate(0, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Python 3.11+</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Backend &amp; Computation</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Core scientific runtime</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Multiprocessing &amp; threads</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Asyncio task concurrency</text>
    </g>

    <!-- Tech 2: FastAPI -->
    <g transform="translate(226, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">FastAPI</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">High-Speed REST API</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Pydantic schema validation</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• BackgroundTasks execution</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• OpenAPI / Swagger docs</text>
    </g>

    <!-- Tech 3: React + Vite -->
    <g transform="translate(452, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">React 18 + Vite</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Frontend Architecture</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• TypeScript component tree</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Shared context providers</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Tailwind CSS &amp; Shadcn</text>
    </g>

    <!-- Tech 4: Pandas -->
    <g transform="translate(678, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Pandas</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Tabular Data Hygiene</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Canonical normalization</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• DOI &amp; title deduplication</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• CSV generation &amp; mapping</text>
    </g>

    <!-- Tech 5: NetworkX -->
    <g transform="translate(904, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">NetworkX</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Graph Centrality Analysis</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Co-occurrence graph nodes</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Degree &amp; betweenness</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Closeness &amp; eigenvector</text>
    </g>

    <!-- Tech 6: Sentence-Transformers -->
    <g transform="translate(1130, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Sentence-Transformers</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Dense Vector Encoding</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• all-mpnet-base-v2 (768-d)</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• HDBSCAN semantic chunks</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• 800-token cap boundary</text>
    </g>

    <!-- Tech 7: FAISS -->
    <g transform="translate(1356, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">FAISS</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">Vector Similarity Search</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• IndexFlatL2 cosine search</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Sub-millisecond queries</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Persistent .index files</text>
    </g>

    <!-- Tech 8: Google Gemini & NCBI -->
    <g transform="translate(1582, 38)">
      <rect x="0" y="0" width="215" height="115" rx="6" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.2" filter="url(#shadow)"/>
      <rect x="0" y="0" width="215" height="24" rx="6" fill="{NAVY}"/>
      <text x="107" y="17" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Gemini &amp; NCBI</text>
      <text x="10" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">LLM &amp; Biomedical APIs</text>
      <text x="10" y="62" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• gemini-2.5-flash with [n]</text>
      <text x="10" y="78" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• Query decomposition</text>
      <text x="10" y="94" font-family="Arial, sans-serif" font-size="9.5" fill="{MUTED_TEXT}">• PubMed E-utilities &amp; MeSH</text>
    </g>
  </g>
</svg>"""
    return svg

# ===========================================================================
# SLIDE 3: PRELIMINARY RESULTS & ANALYSIS
# ===========================================================================
def build_slide_03() -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  {COMMON_DEFS}

  <!-- Slide Background -->
  <rect width="1920" height="1080" fill="{LIGHT_GREY}" />

  {make_header(
      "M.TECH DATA SCIENCE PROJECT REVIEW",
      "Preliminary Results &amp; Analysis",
      "Empirical System Outputs, Dataset Quality Validation &amp; Verified Bibliometric Metrics (Tested on Real Datasets)",
      3
  )}

  <!-- ================= RESULTS DASHBOARD (3 COLUMNS) ================= -->
  <!-- COLUMN 1: APPLICATION EVIDENCE & SEARCH VALIDATION (x: 60, width: 560) -->
  <g transform="translate(60, 125)">
    <!-- Section Header -->
    <rect x="0" y="0" width="560" height="34" rx="6" fill="{NAVY}" />
    <text x="20" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART A — APPLICATION EVIDENCE &amp; SEARCH VALIDATION
    </text>

    <!-- Evidence Card 1: PubMed Ingestion Execution (y: 44) -->
    <g transform="translate(0, 44)">
      <rect x="0" y="0" width="560" height="385" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="560" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        Search &amp; Metadata Extraction (Query: &quot;first aid&quot;)
      </text>
      <rect x="440" y="7" width="105" height="18" rx="4" fill="{GREEN}" />
      <text x="492" y="19" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">100 PAPERS EXTRACTED</text>

      <!-- Search Execution Metrics -->
      <g transform="translate(16, 42)">
        <text x="0" y="14" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">PubMed Live Search Execution Evidence:</text>
        <rect x="0" y="22" width="528" height="68" rx="6" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
        <text x="12" y="40" font-family="Arial, sans-serif" font-size="10" font-weight="600" fill="{DARK_TEXT}">• Query: &quot;first aid&quot; (Automated MeSH phrase expansion active)</text>
        <text x="12" y="56" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Progress Stages: 0 Init → 1 Querying → 2 Extracting → 3 CSV Save → 4 Done</text>
        <text x="12" y="72" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Output CSV: data/first_aid.csv (100 records, 100% schema alignment)</text>

        <!-- Metadata Field Yield -->
        <text x="0" y="108" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Verified Metadata Yield from XML Articles:</text>
        
        <!-- Field Yield Table -->
        <g transform="translate(0, 116)">
          <rect x="0" y="0" width="528" height="210" rx="6" fill="{WHITE}" stroke="{BORDER_COLOR}" stroke-width="1"/>
          
          <rect x="0" y="0" width="528" height="24" rx="6" fill="{LIGHT_BLUE}"/>
          <text x="10" y="16" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">EXTRACTED FIELD</text>
          <text x="210" y="16" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">POPULATED COUNT</text>
          <text x="360" y="16" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">COVERAGE %</text>
          <text x="470" y="16" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">STATUS</text>

          <!-- Rows -->
          <text x="10" y="42" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Paper Title</text>
          <text x="210" y="42" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">100 / 100 records</text>
          <text x="360" y="42" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">100.0%</text>
          <text x="470" y="42" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Perfect</text>

          <text x="10" y="66" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Publication Year</text>
          <text x="210" y="66" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">100 / 100 records</text>
          <text x="360" y="66" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">100.0%</text>
          <text x="470" y="66" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Perfect</text>

          <text x="10" y="90" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Journal / Source</text>
          <text x="210" y="90" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">100 / 100 records</text>
          <text x="360" y="90" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">100.0%</text>
          <text x="470" y="90" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Perfect</text>

          <text x="10" y="114" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Digital Object ID (DOI)</text>
          <text x="210" y="114" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">99 / 100 records</text>
          <text x="360" y="114" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">99.0%</text>
          <text x="470" y="114" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Excellent</text>

          <text x="10" y="138" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Author Names List</text>
          <text x="210" y="138" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">99 / 100 records</text>
          <text x="360" y="138" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">99.0%</text>
          <text x="470" y="138" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Excellent</text>

          <text x="10" y="162" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Author Affiliations</text>
          <text x="210" y="162" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">97 / 100 records</text>
          <text x="360" y="162" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">97.0%</text>
          <text x="470" y="162" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ High Yield</text>

          <text x="10" y="186" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Keywords / MeSH Terms</text>
          <text x="210" y="186" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">95 / 100 records</text>
          <text x="360" y="186" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">95.0%</text>
          <text x="470" y="186" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ High Yield</text>

          <text x="10" y="206" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">Abstract Body Text</text>
          <text x="210" y="206" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">90 / 100 records</text>
          <text x="360" y="206" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">90.0%</text>
          <text x="470" y="206" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ High Yield</text>
        </g>
      </g>
    </g>

    <!-- Evidence Card 2: Dataset Quality & Feature Readiness (y: 440) -->
    <g transform="translate(0, 440)">
      <rect x="0" y="0" width="560" height="465" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="560" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        Dataset Quality &amp; Feature Readiness Audit
      </text>

      <!-- Overall Score & Grade Badge -->
      <g transform="translate(16, 46)">
        <rect x="0" y="0" width="528" height="85" rx="6" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1.2"/>
        
        <!-- Score Box -->
        <rect x="15" y="12" width="130" height="60" rx="6" fill="{WHITE}" stroke="#86EFAC" stroke-width="1"/>
        <text x="80" y="34" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{MUTED_TEXT}" text-anchor="middle">OVERALL SCORE</text>
        <text x="80" y="62" font-family="Arial, sans-serif" font-size="24" font-weight="800" fill="{GREEN}" text-anchor="middle">96.9 / 100</text>

        <!-- Grade Box -->
        <rect x="155" y="12" width="130" height="60" rx="6" fill="{WHITE}" stroke="#86EFAC" stroke-width="1"/>
        <text x="220" y="34" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{MUTED_TEXT}" text-anchor="middle">QUALITY GRADE</text>
        <text x="220" y="62" font-family="Arial, sans-serif" font-size="20" font-weight="800" fill="{GREEN}" text-anchor="middle">Excellent</text>

        <!-- Records Hygiene Summary -->
        <text x="300" y="32" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">Dataset Hygiene Metrics:</text>
        <text x="300" y="50" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Total Records: 100 | Valid: 100</text>
        <text x="300" y="66" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">• Duplicate Contamination: 0 (0%)</text>
      </g>

      <!-- 7 Feature Readiness Grid -->
      <g transform="translate(16, 142)">
        <text x="0" y="12" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Evaluated 7-Feature Readiness Status:</text>
        
        <!-- Feature 1 -->
        <g transform="translate(0, 20)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">keyword_analysis</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 95.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 2 -->
        <g transform="translate(0, 60)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">cooccurrence_analysis</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 95.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 3 -->
        <g transform="translate(0, 100)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">country_analysis</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 97.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 4 -->
        <g transform="translate(0, 140)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">author_analysis</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 99.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 5 -->
        <g transform="translate(0, 180)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">semantic_search</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 89.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 6 -->
        <g transform="translate(0, 220)">
          <rect x="0" y="0" width="528" height="34" rx="4" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <text x="12" y="21" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">ai_chat_rag</text>
          <text x="260" y="21" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 89.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{GREEN}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">READY</text>
        </g>

        <!-- Feature 7: Trend analysis -->
        <g transform="translate(0, 260)">
          <rect x="0" y="0" width="528" height="48" rx="4" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
          <text x="12" y="20" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{DARK_TEXT}">trend_analysis</text>
          <text x="260" y="20" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">Coverage: 100.0%</text>
          <rect x="420" y="8" width="95" height="18" rx="3" fill="{AMBER}"/>
          <text x="467" y="20" font-family="Arial, sans-serif" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">PARTIAL</text>
          <text x="12" y="38" font-family="Arial, sans-serif" font-size="9" fill="#B45309">Warning: Single publication year cohort ([2026]); multi-year longitudinal trend disabled.</text>
        </g>
      </g>
    </g>
  </g>

  <!-- COLUMN 2: ANALYTICAL & BIBLIOMETRIC RESULTS (x: 645, width: 615) -->
  <g transform="translate(645, 125)">
    <!-- Section Header -->
    <rect x="0" y="0" width="615" height="34" rx="6" fill="{NAVY}" />
    <text x="20" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART B — BIBLIOMETRIC &amp; GEOGRAPHIC ANALYTICAL OUTPUTS
    </text>

    <!-- Card 3: Keyword Frequency & NetworkX Centrality (y: 44) -->
    <g transform="translate(0, 44)">
      <rect x="0" y="0" width="615" height="425" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="615" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        Keyword Frequency &amp; NetworkX Centrality Analysis
      </text>
      <rect x="495" y="7" width="105" height="18" rx="4" fill="{GREEN}" />
      <text x="547" y="19" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">406 KEYWORDS</text>

      <g transform="translate(16, 44)">
        <text x="0" y="12" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Top Keyword Frequency Distribution (first_aid.csv):</text>
        
        <!-- Frequency Table -->
        <g transform="translate(0, 20)">
          <rect x="0" y="0" width="583" height="135" rx="5" fill="{WHITE}" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <rect x="0" y="0" width="583" height="22" rx="5" fill="{LIGHT_BLUE}"/>
          <text x="10" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">RANKED KEYWORD TERM</text>
          <text x="240" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">FREQUENCY</text>
          <text x="350" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">PERCENTAGE</text>
          <text x="470" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">RELATIVE BAR</text>

          <!-- Rows -->
          <text x="10" y="38" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{DARK_TEXT}">1. first aid</text>
          <text x="240" y="38" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">9 papers</text>
          <text x="350" y="38" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">9.0%</text>
          <rect x="470" y="28" width="90" height="12" rx="2" fill="{TEAL}"/>

          <text x="10" y="60" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">2. mental health first aid</text>
          <text x="240" y="60" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">8 papers</text>
          <text x="350" y="60" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">8.0%</text>
          <rect x="470" y="50" width="80" height="12" rx="2" fill="{TEAL}"/>

          <text x="10" y="82" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">3. psychological first aid</text>
          <text x="240" y="82" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">8 papers</text>
          <text x="350" y="82" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">8.0%</text>
          <rect x="470" y="72" width="80" height="12" rx="2" fill="{TEAL}"/>

          <text x="10" y="104" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">4. mental health</text>
          <text x="240" y="104" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">6 papers</text>
          <text x="350" y="104" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">6.0%</text>
          <rect x="470" y="94" width="60" height="12" rx="2" fill="{TEAL}"/>

          <text x="10" y="126" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">5. knowledge</text>
          <text x="240" y="126" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">5 papers</text>
          <text x="350" y="126" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">5.0%</text>
          <rect x="470" y="116" width="50" height="12" rx="2" fill="{TEAL}"/>
        </g>

        <!-- NetworkX Centrality Evidence -->
        <text x="0" y="178" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Verified NetworkX Centrality Metrics (250 Co-occurrence Edges):</text>
        
        <g transform="translate(0, 186)">
          <rect x="0" y="0" width="583" height="175" rx="5" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
          
          <!-- Centrality Card 1: first aid -->
          <g transform="translate(12, 12)">
            <rect x="0" y="0" width="559" height="70" rx="5" fill="{WHITE}" stroke="#93C5FD" stroke-width="1"/>
            <text x="10" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">Centrality Lead: &quot;first aid&quot;</text>
            <text x="10" y="38" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">
              Degree: <tspan font-weight="700" fill="{GREEN}">0.4343</tspan> | 
              Betweenness: <tspan font-weight="700" fill="{GREEN}">0.5950</tspan> | 
              Closeness: <tspan font-weight="700" fill="{GREEN}">0.4380</tspan>
            </text>
            <text x="10" y="56" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">
              Eigenvector Centrality: <tspan font-weight="700">0.4137</tspan> | Clustering Coefficient: <tspan font-weight="700">0.1661</tspan>
            </text>
          </g>

          <!-- Centrality Card 2: mental health first aid -->
          <g transform="translate(12, 92)">
            <rect x="0" y="0" width="559" height="70" rx="5" fill="{WHITE}" stroke="#CBD5E1" stroke-width="1"/>
            <text x="10" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{NAVY}">Secondary Lead: &quot;mental health first aid&quot;</text>
            <text x="10" y="38" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">
              Degree: <tspan font-weight="700" fill="{GREEN}">0.2222</tspan> | 
              Betweenness: <tspan font-weight="700" fill="{GREEN}">0.1766</tspan> | 
              Closeness: <tspan font-weight="700" fill="{GREEN}">0.3370</tspan>
            </text>
            <text x="10" y="56" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">
              Clustering Coefficient: <tspan font-weight="700">0.2251</tspan> (High community triad connectivity)
            </text>
          </g>
        </g>
      </g>
    </g>

    <!-- Card 4: Country Analysis & International Collaboration (y: 480) -->
    <g transform="translate(0, 480)">
      <rect x="0" y="0" width="615" height="425" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="615" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        Author Affiliation &amp; International Country Collaboration
      </text>
      <rect x="495" y="7" width="105" height="18" rx="4" fill="{GREEN}" />
      <text x="547" y="19" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">40 COUNTRIES</text>

      <g transform="translate(16, 44)">
        <text x="0" y="12" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Country Affiliation Yield &amp; Geographic Distribution:</text>

        <!-- Top Countries Table -->
        <g transform="translate(0, 20)">
          <rect x="0" y="0" width="583" height="160" rx="5" fill="{WHITE}" stroke="{BORDER_COLOR}" stroke-width="1"/>
          <rect x="0" y="0" width="583" height="22" rx="5" fill="{LIGHT_BLUE}"/>
          <text x="10" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">RESOLVED COUNTRY</text>
          <text x="210" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">ISO-3</text>
          <text x="310" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">PAPERS</text>
          <text x="410" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">PERCENTAGE</text>
          <text x="500" y="15" font-family="Arial, sans-serif" font-size="10" font-weight="700" fill="{NAVY}">BAR</text>

          <!-- Rows -->
          <text x="10" y="40" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{DARK_TEXT}">1. China</text>
          <text x="210" y="40" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">CHN</text>
          <text x="310" y="40" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">24</text>
          <text x="410" y="40" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">24.0%</text>
          <rect x="500" y="30" width="70" height="11" rx="2" fill="{NAVY}"/>

          <text x="10" y="62" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">2. United States</text>
          <text x="210" y="62" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">USA</text>
          <text x="310" y="62" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">16</text>
          <text x="410" y="62" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">16.0%</text>
          <rect x="500" y="52" width="48" height="11" rx="2" fill="{NAVY}"/>

          <text x="10" y="84" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">3. United Kingdom</text>
          <text x="210" y="84" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">GBR</text>
          <text x="310" y="84" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">11</text>
          <text x="410" y="84" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">11.0%</text>
          <rect x="500" y="74" width="33" height="11" rx="2" fill="{NAVY}"/>

          <text x="10" y="106" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">4. Australia</text>
          <text x="210" y="106" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">AUS</text>
          <text x="310" y="106" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">8</text>
          <text x="410" y="106" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">8.0%</text>
          <rect x="500" y="96" width="24" height="11" rx="2" fill="{NAVY}"/>

          <text x="10" y="128" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">5. Turkey</text>
          <text x="210" y="128" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">TUR</text>
          <text x="310" y="128" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">7</text>
          <text x="410" y="128" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">7.0%</text>
          <rect x="500" y="118" width="21" height="11" rx="2" fill="{NAVY}"/>

          <text x="10" y="150" font-family="Arial, sans-serif" font-size="10.5" font-weight="600" fill="{DARK_TEXT}">6. Germany</text>
          <text x="210" y="150" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">DEU</text>
          <text x="310" y="150" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">6</text>
          <text x="410" y="150" font-family="Arial, sans-serif" font-size="10.5" fill="{MUTED_TEXT}">6.0%</text>
          <rect x="500" y="140" width="18" height="11" rx="2" fill="{NAVY}"/>
        </g>

        <!-- International Collaboration Network Evidence -->
        <text x="0" y="204" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Verified Bilateral Country Collaboration Edges (23 Multi-Country Papers):</text>
        
        <g transform="translate(0, 212)">
          <rect x="0" y="0" width="583" height="148" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
          
          <g transform="translate(15, 15)">
            <text x="0" y="15" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{GREEN}">Lead Co-Authorship Edges:</text>
            <text x="0" y="34" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">Canada ↔ United States:</tspan> Joint Weight: 5 papers</text>
            <text x="0" y="52" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">China ↔ Hong Kong:</tspan> Joint Weight: 4 papers</text>
            <text x="0" y="70" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">Australia ↔ United Kingdom:</tspan> Joint Weight: 4 papers</text>
            <text x="0" y="88" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">United Kingdom ↔ United States:</tspan> Joint Weight: 4 papers</text>
            <text x="0" y="106" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">Australia ↔ United States:</tspan> Joint Weight: 3 papers</text>
            <text x="0" y="124" font-family="Arial, sans-serif" font-size="10" fill="{DARK_TEXT}">• <tspan font-weight="700">Canada ↔ United Kingdom:</tspan> Joint Weight: 3 papers</text>
          </g>
        </g>
      </g>
    </g>
  </g>

  <!-- COLUMN 3: SEMANTIC RAG, EVALUATION STATUS & PROGRESS (x: 1285, width: 575) -->
  <g transform="translate(1285, 125)">
    <!-- Section Header -->
    <rect x="0" y="0" width="575" height="34" rx="6" fill="{NAVY}" />
    <text x="20" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
      PART C — RAG SEMANTICS, EVALUATION &amp; DEVELOPMENT STATUS
    </text>

    <!-- Card 5: Semantic Search & AI Chat Grounding (y: 44) -->
    <g transform="translate(0, 44)">
      <rect x="0" y="0" width="575" height="235" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="575" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        AI RAG Assistant &amp; Vector Retrieval Evidence
      </text>
      <rect x="475" y="7" width="85" height="18" rx="4" fill="{GREEN}" />
      <text x="517" y="19" font-family="Arial, sans-serif" font-size="9.5" font-weight="700" fill="#FFFFFF" text-anchor="middle">FAISS ACTIVE</text>

      <g transform="translate(16, 44)">
        <text x="0" y="12" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">Functional RAG Architecture Verification:</text>
        <rect x="0" y="22" width="543" height="155" rx="6" fill="#F8FAFC" stroke="{BORDER_COLOR}" stroke-width="1"/>
        
        <g transform="translate(12, 12)">
          <text x="0" y="15" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ HDBSCAN Semantic Chunking:</text>
          <text x="0" y="31" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Preserves natural paragraphs; caps oversized text at 800 tokens.</text>

          <text x="0" y="52" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ FAISS IndexFlatL2 Vector Index:</text>
          <text x="0" y="68" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Normalizes 768-d embeddings for fast cosine similarity search.</text>

          <text x="0" y="89" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Query Decomposition Engine:</text>
          <text x="0" y="105" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Gemini splits complex prompts into ≤5 distinct sub-questions.</text>

          <text x="0" y="126" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">✓ Provenance-Enforced Answers:</text>
          <text x="0" y="142" font-family="Arial, sans-serif" font-size="10" fill="{MUTED_TEXT}">Responses cite sources [n] linking directly to DOI/PDF cards.</text>
        </g>
      </g>
    </g>

    <!-- Card 6: Benchmark Status Warning Box (y: 290) -->
    <g transform="translate(0, 290)">
      <rect x="0" y="0" width="575" height="110" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="8" height="110" rx="4" fill="{AMBER}" />
      
      <g transform="translate(20, 16)">
        <text x="0" y="15" font-family="Arial, sans-serif" font-size="12" font-weight="800" fill="#92400E">
          EVALUATION STATUS &amp; RESEARCH RIGOR NOTICE
        </text>
        <text x="0" y="38" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{NAVY}">
          &quot;Preliminary functional validation – quantitative evaluation pending.&quot;
        </text>
        <text x="0" y="58" font-family="Arial, sans-serif" font-size="10" fill="#78350F">
          All figures shown represent authentic execution outputs from the live Research Rover
        </text>
        <text x="0" y="74" font-family="Arial, sans-serif" font-size="10" fill="#78350F">
          pipeline on real academic datasets. Formal benchmark evaluations (BLEU/ROUGE
        </text>
        <text x="0" y="90" font-family="Arial, sans-serif" font-size="10" fill="#78350F">
          retrieval faithfulness, Precision@k, Recall@k, and latency profiling) are currently ongoing.
        </text>
      </g>
    </g>

    <!-- Card 7: Implementation Progress & Roadmap Status (y: 410) -->
    <g transform="translate(0, 410)">
      <rect x="0" y="0" width="575" height="495" rx="8" fill="{WHITE}" stroke="{CARD_BORDER}" stroke-width="1.5" filter="url(#shadow)" />
      <rect x="0" y="0" width="575" height="32" rx="8" fill="{NAVY}" />
      <text x="16" y="21" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">
        Implementation Inventory &amp; Development Progress
      </text>

      <g transform="translate(16, 44)">
        <!-- 1. Implemented & Verified -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="543" height="135" rx="5" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
          <rect x="0" y="0" width="543" height="22" rx="5" fill="#DCFCE7"/>
          <text x="10" y="16" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{GREEN}">
            ✓ IMPLEMENTED &amp; VERIFIED (PRODUCTION-READY)
          </text>
          <g transform="translate(10, 32)">
            <text x="0" y="12" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• PubMed live retrieval &amp; MeSH automatic query expansion</text>
            <text x="0" y="28" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Universal CSV normalizer (PubMed, Scopus, WoS, OpenAlex)</text>
            <text x="0" y="44" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Dataset quality assessor (0–100 score, grade, feature checks)</text>
            <text x="0" y="60" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Regex affiliation country extractor &amp; 2D/3D map visualizations</text>
            <text x="0" y="76" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Keyword frequency, co-occurrence presence matrix &amp; NetworkX</text>
            <text x="0" y="92" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• HDBSCAN chunking, FAISS vector index &amp; Gemini RAG Q&amp;A</text>
          </g>
        </g>

        <!-- 2. Partially Implemented / Under Development -->
        <g transform="translate(0, 145)">
          <rect x="0" y="0" width="543" height="135" rx="5" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
          <rect x="0" y="0" width="543" height="22" rx="5" fill="#FDE68A"/>
          <text x="10" y="16" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="#B45309">
            ⏳ UNDER DEVELOPMENT (PARTIALLY IMPLEMENTED)
          </text>
          <g transform="translate(10, 32)">
            <text x="0" y="12" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Full UI wiring of backend NetworkX AnalysisService</text>
            <text x="0" y="28" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• CORE academic search API connector (currently stubbed)</text>
            <text x="0" y="44" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Automated full-text scraping coverage on paywalled portals</text>
            <text x="0" y="60" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Real-time token streaming for chat interface</text>
            <text x="0" y="76" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Great-circle collaboration arcs on 3D globe</text>
          </g>
        </g>

        <!-- 3. Planned Enhancements -->
        <g transform="translate(0, 290)">
          <rect x="0" y="0" width="543" height="145" rx="5" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1" stroke-dasharray="3,3"/>
          <rect x="0" y="0" width="543" height="22" rx="5" fill="#DBEAFE"/>
          <text x="10" y="16" font-family="Arial, sans-serif" font-size="10.5" font-weight="700" fill="{BLUE_ACCENT}">
            🚀 PLANNED ENHANCEMENTS (ROADMAP)
          </text>
          <g transform="translate(10, 32)">
            <text x="0" y="12" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Multi-source federated search (OpenAlex, CrossRef, Semantic Scholar)</text>
            <text x="0" y="28" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Citation network analysis (co-citation &amp; bibliographic coupling)</text>
            <text x="0" y="44" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• ML-based author name disambiguation &amp; institution clustering</text>
            <text x="0" y="60" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Formal empirical benchmarking suite (Precision@k, Recall@k, Latency)</text>
            <text x="0" y="76" font-family="Arial, sans-serif" font-size="9.5" fill="{DARK_TEXT}">• Multi-user authentication &amp; cloud database persistence</text>
          </g>
        </g>
      </g>
    </g>
  </g>
</svg>"""
    return svg

# ===========================================================================
# SAVE, RENDER & PREVIEW GENERATION
# ===========================================================================
def save_and_render_slide(slide_dir: str, name: str, svg_content: str):
    # Sanitize ampersands for pure SVG 1.1 XML compliance
    svg_content = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)", "&amp;", svg_content)
    
    svg_path = os.path.join(slide_dir, f"{name}.svg")
    png_path = os.path.join(slide_dir, f"{name}.png")

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

    png_bytes = resvg_py.svg_to_bytes(svg_content.strip())
    with open(png_path, "wb") as f:
        f.write(png_bytes)

    size_kb = len(png_bytes) / 1024
    print(f"Generated {name}: SVG -> {svg_path}, PNG -> {png_path} ({size_kb:.1f} KB)")


def generate_contact_sheet():
    print("Generating all-in-one preview contact sheet for all 3 slides...")
    # Composite: Vertical stack of 3 slides with title and border
    # Width: 1920, Height: 3 * (1080 * 0.45 + 50) + 120 = ~1600
    thumb_w = 1600
    thumb_h = int(thumb_w * 1080 / 1920)  # 900
    canvas_w = 1800
    canvas_h = 3 * (thumb_h + 80) + 140

    sheet = Image.new("RGB", (canvas_w, canvas_h), "#0F172A")
    draw = ImageDraw.Draw(sheet)

    # Title Banner
    draw.rectangle([0, 0, canvas_w, 110], fill="#142B65")
    draw.rectangle([0, 106, canvas_w, 110], fill="#138C8C")
    draw.text((canvas_w // 2, 35), "RESEARCH ROVER — M.TECH PROJECT REVIEW TECHNICAL SLIDES", fill="#FFFFFF", anchor="mm")
    draw.text((canvas_w // 2, 75), "Comprehensive 3-Slide Master Portfolio · 16:9 Widescreen (1920 x 1080) Presentation Visuals", fill="#93C5FD", anchor="mm")

    slide_pngs = [
        ("SLIDE 1: Problem Formulation & Literature Review", os.path.join(SLIDE_1_DIR, "slide_1_problem_formulation.png")),
        ("SLIDE 2: Methodology & Technical Implementation", os.path.join(SLIDE_2_DIR, "slide_2_methodology.png")),
        ("SLIDE 3: Preliminary Results & Analysis", os.path.join(SLIDE_3_DIR, "slide_3_preliminary_results.png"))
    ]

    curr_y = 140
    for label, path in slide_pngs:
        # Title Label
        draw.text((100, curr_y + 15), label.upper(), fill="#38BDF8")
        
        # Open and resize thumbnail
        img = Image.open(path)
        img_thumb = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)

        # Draw white frame around slide
        draw.rectangle([98, curr_y + 38, 100 + thumb_w + 2, curr_y + 40 + thumb_h + 2], fill="#1E293B", outline="#38BDF8", width=2)
        sheet.paste(img_thumb, (100, curr_y + 40))

        curr_y += thumb_h + 80

    out_path = os.path.join(PREVIEW_DIR, "all_three_slides_preview.png")
    sheet.save(out_path, "PNG", optimize=True)
    size_kb = os.path.getsize(out_path) / 1024
    print(f"Generated All-Three-Slides Contact Sheet -> {out_path} ({size_kb:.1f} KB)")


def generate_html_preview():
    print("Generating interactive HTML preview gallery...")
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research Rover — M.Tech Project Review Slides (3-Slide Master Collection)</title>
  <style>
    :root {{
      --navy: #142B65;
      --teal: #138C8C;
      --light-blue: #EAF3F8;
      --bg: #0F172A;
      --card-bg: #1E293B;
      --border: #334155;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
      --green: #23865A;
      --amber: #D99A32;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding-bottom: 80px;
    }}
    header {{
      background: linear-gradient(135deg, var(--navy), #1E3A8A);
      border-bottom: 4px solid var(--teal);
      padding: 36px 48px;
    }}
    .badge {{
      display: inline-block;
      background: rgba(19, 140, 140, 0.25);
      border: 1px solid var(--teal);
      color: #7DD3FC;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      padding: 4px 14px;
      border-radius: 999px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    h1 {{ font-size: 28px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px; }}
    .subtitle {{ font-size: 15px; color: #93C5FD; max-width: 900px; }}
    
    .nav-bar {{
      display: flex;
      gap: 16px;
      padding: 16px 48px;
      background: #111827;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .nav-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 18px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .nav-btn:hover {{ background: var(--teal); color: #FFF; border-color: var(--teal); }}
    
    main {{ max-width: 1400px; margin: 40px auto; padding: 0 32px; display: flex; flex-direction: column; gap: 48px; }}
    .slide-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .slide-header {{
      padding: 20px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.6);
    }}
    .slide-title-group h2 {{ font-size: 18px; font-weight: 700; color: #FFF; }}
    .slide-title-group p {{ font-size: 13px; color: var(--text-muted); }}
    .actions {{ display: flex; gap: 10px; }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-svg {{ background: #2563EB; color: #FFF; }}
    .btn-svg:hover {{ background: #1D4ED8; }}
    .btn-png {{ background: #0D9488; color: #FFF; }}
    .btn-png:hover {{ background: #0F766E; }}
    
    .slide-viewport {{
      padding: 24px;
      background: #0B0F17;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .slide-img {{
      width: 100%;
      height: auto;
      max-width: 1320px;
      border-radius: 6px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
      border: 1px solid rgba(255,255,255,0.1);
    }}
    .specs-grid {{
      padding: 16px 24px;
      background: #0F172A;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      font-size: 12px;
      border-top: 1px solid var(--border);
    }}
    .spec-item span {{ color: var(--text-muted); display: block; margin-bottom: 2px; }}
    .spec-item strong {{ color: #F1F5F9; }}
    footer {{ text-align: center; color: var(--text-muted); font-size: 13px; margin-top: 60px; }}
  </style>
</head>
<body>

<header>
  <div class="badge">M.Tech Data Science Project Review</div>
  <h1>RESEARCH ROVER — 3-Slide Technical Presentation Portfolio</h1>
  <p class="subtitle">An Intelligent Research Discovery and Bibliometric Analysis Platform. Complete, verified visual assets ready for direct insertion into Microsoft PowerPoint.</p>
</header>

<div class="nav-bar">
  <a href="#slide1" class="nav-btn">Slide 1: Problem &amp; Literature</a>
  <a href="#slide2" class="nav-btn">Slide 2: Methodology &amp; Architecture</a>
  <a href="#slide3" class="nav-btn">Slide 3: Results &amp; Analysis</a>
  <a href="all_three_slides_preview.png" target="_blank" class="nav-btn" style="background:#138C8C;">View Full Contact Sheet (PNG)</a>
</div>

<main>
  <!-- SLIDE 1 -->
  <article class="slide-card" id="slide1">
    <div class="slide-header">
      <div class="slide-title-group">
        <h2>SLIDE 1: Problem Formulation &amp; Literature Review</h2>
        <p>Information Overload, Fragmented Metadata Schemas &amp; Literature Review Matrix</p>
      </div>
      <div class="actions">
        <a href="../02_Slide_1_Problem_Formulation/slide_1_problem_formulation.svg" target="_blank" class="btn btn-svg">Open Vector SVG</a>
        <a href="../02_Slide_1_Problem_Formulation/slide_1_problem_formulation.png" download class="btn btn-png">Download 1080p PNG</a>
      </div>
    </div>
    <div class="slide-viewport">
      <img src="../02_Slide_1_Problem_Formulation/slide_1_problem_formulation.png" alt="Slide 1 Preview" class="slide-img">
    </div>
    <div class="specs-grid">
      <div class="spec-item"><span>Aspect Ratio</span><strong>16:9 Widescreen (1920 × 1080)</strong></div>
      <div class="spec-item"><span>Technology</span><strong>Pure SVG 1.1 (No ForeignObject)</strong></div>
      <div class="spec-item"><span>PowerPoint Support</span><strong>Direct Insert or &quot;Convert to Shape&quot;</strong></div>
      <div class="spec-item"><span>Foundational Citations</span><strong>Van Eck &amp; Waltman (2010), Aria (2017), Lewis (2020)</strong></div>
    </div>
  </article>

  <!-- SLIDE 2 -->
  <article class="slide-card" id="slide2">
    <div class="slide-header">
      <div class="slide-title-group">
        <h2>SLIDE 2: Methodology &amp; Technical Implementation</h2>
        <p>Six-Tier Architecture, Dual-Path Ingestion Pipeline &amp; Verified Technology Stack</p>
      </div>
      <div class="actions">
        <a href="../03_Slide_2_Methodology/slide_2_methodology.svg" target="_blank" class="btn btn-svg">Open Vector SVG</a>
        <a href="../03_Slide_2_Methodology/slide_2_methodology.png" download class="btn btn-png">Download 1080p PNG</a>
      </div>
    </div>
    <div class="slide-viewport">
      <img src="../03_Slide_2_Methodology/slide_2_methodology.png" alt="Slide 2 Preview" class="slide-img">
    </div>
    <div class="specs-grid">
      <div class="spec-item"><span>Aspect Ratio</span><strong>16:9 Widescreen (1920 × 1080)</strong></div>
      <div class="spec-item"><span>Architectural Tiers</span><strong>6 Connected Tiers (UI to Output)</strong></div>
      <div class="spec-item"><span>Status Indicators</span><strong>Green (Verified) vs Amber (Under Dev)</strong></div>
      <div class="spec-item"><span>Verified Stack</span><strong>FastAPI, React, Pandas, NetworkX, FAISS, Gemini</strong></div>
    </div>
  </article>

  <!-- SLIDE 3 -->
  <article class="slide-card" id="slide3">
    <div class="slide-header">
      <div class="slide-title-group">
        <h2>SLIDE 3: Preliminary Results &amp; Analysis</h2>
        <p>Empirical System Outputs, Dataset Quality Validation &amp; Verified Bibliometric Metrics</p>
      </div>
      <div class="actions">
        <a href="../04_Slide_3_Preliminary_Results/slide_3_preliminary_results.svg" target="_blank" class="btn btn-svg">Open Vector SVG</a>
        <a href="../04_Slide_3_Preliminary_Results/slide_3_preliminary_results.png" download class="btn btn-png">Download 1080p PNG</a>
      </div>
    </div>
    <div class="slide-viewport">
      <img src="../04_Slide_3_Preliminary_Results/slide_3_preliminary_results.png" alt="Slide 3 Preview" class="slide-img">
    </div>
    <div class="specs-grid">
      <div class="spec-item"><span>Validation Dataset</span><strong>first_aid.csv (100 Real Papers from PubMed)</strong></div>
      <div class="spec-item"><span>Dataset Quality</span><strong>Score: 96.9 / 100 (Grade: Excellent)</strong></div>
      <div class="spec-item"><span>Affiliation Yield</span><strong>96.0% Country Coverage · 40 Nations</strong></div>
      <div class="spec-item"><span>Network Metrics</span><strong>Lead Centrality: 0.4343 · 250 Co-occurrence Edges</strong></div>
    </div>
  </article>
</main>

<footer>
  <p>RESEARCH ROVER — M.Tech Data Science Review Presentation Assets · Generated on November 17, 2026</p>
</footer>

</body>
</html>"""
    html_path = os.path.join(PREVIEW_DIR, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML Preview Gallery -> {html_path}")


def generate_readme():
    print("Generating root README.md documentation...")
    readme_content = f"""# Research Rover — M.Tech Project Review Technical Slides

**Project Title:** RESEARCH ROVER: An Intelligent Research Discovery and Bibliometric Analysis Platform  
**Academic Degree:** M.Tech Data Science  
**Review Presentation Stage:** Mid-Semester Project Review  
**Date:** November 17, 2026  
**Directory:** `Research_Rover_Review_Slides/`

---

## 1. Directory Structure

```text
Research_Rover_Review_Slides/
│
├── 01_Source_Analysis/
│   ├── implementation_inventory.md     # Full architectural audit (Implemented, Partial, Planned)
│   ├── verified_components.md          # Detailed verification of production-ready modules
│   └── pending_components.md           # Roadmap and ongoing components analysis
│
├── 02_Slide_1_Problem_Formulation/
│   ├── slide_1_problem_formulation.svg  # Scalable vector diagram for PowerPoint
│   └── slide_1_problem_formulation.png  # Full HD 1080p raster render (1920 × 1080)
│
├── 03_Slide_2_Methodology/
│   ├── slide_2_methodology.svg          # Connected 6-tier architecture & dual-path pipeline
│   └── slide_2_methodology.png          # Full HD 1080p raster render (1920 × 1080)
│
├── 04_Slide_3_Preliminary_Results/
│   ├── slide_3_preliminary_results.svg  # Empirical results dashboard with real metrics
│   └── slide_3_preliminary_results.png  # Full HD 1080p raster render (1920 × 1080)
│
├── 05_Preview/
│   ├── all_three_slides_preview.png     # Composite contact sheet of all 3 slides
│   └── index.html                       # Standalone local interactive HTML preview gallery
│
└── README.md                            # Comprehensive portfolio documentation
```

---

## 2. Slide Master Inventory & Presentation Mapping

| Slide | Title & Theme | Key Contents | Vector SVG | Raster PNG (1080p) |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Problem Formulation & Literature Review** | • 4 Research Challenges (Information Overload, Fragmented Schemas, Manual Processing, Limited Visibility)<br>• Proposed Integration Paradigm vs. Conventional Disconnected Tools<br>• Literature Review Matrix (Van Eck 2010, Aria 2017, Lewis 2020)<br>• Concise Research Objective Statement | `02_Slide_1_Problem_Formulation/slide_1_problem_formulation.svg` | `02_Slide_1_Problem_Formulation/slide_1_problem_formulation.png` |
| **02** | **Methodology & Technical Implementation** | • Six-Tier Connected Architecture (UI, Backend, Ingestion, Normalization, Analytical AI, Visualization)<br>• Dual-Path Ingestion Pipeline (Live PubMed E-utilities + Universal Multi-Schema CSVs)<br>• Production Technology Stack Strip (FastAPI, React, Pandas, NetworkX, FAISS, Gemini) | `03_Slide_2_Methodology/slide_2_methodology.svg` | `03_Slide_2_Methodology/slide_2_methodology.png` |
| **03** | **Preliminary Results & Analysis** | • Search Validation (100 papers from query `"first aid"` with 100% Title/Year/Source, 99% DOI)<br>• Dataset Quality Score (**96.9/100**, Grade: **Excellent**, 0 duplicates)<br>• 7-Feature Readiness Status (6 Ready, 1 Partial)<br>• Verified NetworkX Centralities (`"first aid"` degree: 0.4343, betweenness: 0.5950)<br>• Geographic Affiliations (**96.0% country coverage**, 40 nations, 23 international papers)<br>• Preliminary Validation Status Label & Roadmap Progress Matrix | `04_Slide_3_Preliminary_Results/slide_3_preliminary_results.svg` | `04_Slide_3_Preliminary_Results/slide_3_preliminary_results.png` |

---

## 3. Design System & Compliance Guarantee

- **Aspect Ratio:** 16:9 Widescreen (`1920 × 1080` resolution).
- **Color Palette:**
  - Navy Blue: `#142B65` (Primary structural containers & headers)
  - Teal: `#138C8C` (Accent lines, connectors & highlights)
  - Light Blue: `#EAF3F8` (Table headers & secondary cards)
  - Light Grey: `#F4F6F8` (Canvas background)
  - White: `#FFFFFF` (Card surfaces)
  - Green: `#23865A` (Implemented & Verified status)
  - Amber: `#D99A32` (Under Development / Warning status)
- **PowerPoint Vector Compatibility:**
  - 100% Pure native SVG 1.1 elements (`<rect>`, `<path>`, `<circle>`, `<text>`, `<tspan>`).
  - Zero `<foreignObject>` or embedded raster tags, eliminating any font or clipping errors in Microsoft PowerPoint.
  - Fully convertible into native PowerPoint vector shapes via right-click **Convert to Shape** (`Ctrl+Shift+G`).

---

## 4. PowerPoint Insertion Instructions

### Method 1: Direct Vector SVG Insertion (Recommended)
1. Open PowerPoint and select the destination slide.
2. Click **Insert** &rarr; **Pictures** &rarr; **This Device...**
3. Navigate to `Research_Rover_Review_Slides/` and select the appropriate `.svg` file.
4. Scale as desired. Linework and typography remain mathematically sharp at any classroom projection zoom level.

### Converting SVG to Editable PowerPoint Shapes (Optional)
If you wish to edit text, recolor elements, or animate specific cards:
1. Select the inserted SVG image on the slide.
2. In the **Graphics Format** tab on the ribbon, click **Convert to Shape** (or right-click &rarr; **Convert to Shape**).
3. PowerPoint will ungroup the diagram into native Microsoft Office vector shapes and text boxes.

### Method 2: High-Resolution 1080p PNG Fallback
If using an older projector system or presentation viewer without SVG support:
1. Insert the corresponding `.png` from each slide directory.
2. The images are pre-scaled to `1920 × 1080`, fitting widescreen presentation slides without letterboxing.
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Generated Portfolio README.md -> {readme_path}")


def main():
    print("=== BUILDING RESEARCH ROVER 3 TECHNICAL REVIEW SLIDES ===")

    # 1. Slide 1: Problem Formulation & Literature Review
    svg_01 = build_slide_01()
    save_and_render_slide(SLIDE_1_DIR, "slide_1_problem_formulation", svg_01)

    # 2. Slide 2: Methodology & Technical Implementation
    svg_02 = build_slide_02()
    save_and_render_slide(SLIDE_2_DIR, "slide_2_methodology", svg_02)

    # 3. Slide 3: Preliminary Results & Analysis
    svg_03 = build_slide_03()
    save_and_render_slide(SLIDE_3_DIR, "slide_3_preliminary_results", svg_03)

    # 4. Preview Contact Sheet
    generate_contact_sheet()

    # 5. Interactive HTML Preview Gallery
    generate_html_preview()

    # 6. Documentation
    generate_readme()

    print("\nALL 3 PRESENTATION SLIDES & PREVIEWS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    main()
