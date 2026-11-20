"""
Render high-resolution, presentation-grade 300 DPI UML Use Case Diagram for Research Rover.
Uses Matplotlib to produce a crystal-clear, landscape PNG matching UML 2.5 standards.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from pathlib import Path

def draw_stick_figure(ax, x, y, scale=1.0, color="#1D4ED8"):
    # Head
    head_radius = 0.18 * scale
    head = Circle((x, y + 0.65 * scale), head_radius, facecolor="#EFF6FF", edgecolor=color, linewidth=2.0, zorder=5)
    ax.add_patch(head)
    
    # Body
    ax.plot([x, x], [y + 0.65 * scale - head_radius, y + 0.1 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    
    # Arms
    ax.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.35 * scale, y + 0.35 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    
    # Legs
    ax.plot([x, x - 0.28 * scale], [y + 0.1 * scale, y - 0.45 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)
    ax.plot([x, x + 0.28 * scale], [y + 0.1 * scale, y - 0.45 * scale], color=color, linewidth=2.5, solid_capstyle='round', zorder=5)

def draw_usecase_oval(ax, x, y, width, height, title, subtitle=None, fillcolor="#F8FAFC", edgecolor="#2563EB", textcolor="#0F172A", title_fontsize=9, sub_fontsize=7.5, is_base=False):
    lw = 2.0 if is_base else 1.3
    # Use rounded box with corner radius = height/2 to make a perfect capsule/oval shape
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle=f"round,pad=0,rounding_size={height/2}",
        facecolor=fillcolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=4
    )
    ax.add_patch(box)
    
    if subtitle:
        ax.text(x, y + height * 0.12, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=textcolor, zorder=6)
        ax.text(x, y - height * 0.22, subtitle, ha='center', va='center', fontsize=sub_fontsize, color="#64748B", zorder=6)
    else:
        ax.text(x, y, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=textcolor, zorder=6)

def draw_external_actor(ax, x, y, width, height, title, subtitle, tag_color="#0284C7"):
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0,rounding_size=0.15",
        facecolor="#F8FAFC",
        edgecolor=tag_color,
        linewidth=1.6,
        zorder=4
    )
    ax.add_patch(box)
    
    ax.text(x, y + height * 0.28, "<<external system>>", ha='center', va='center', fontsize=7.5, fontweight='bold', color=tag_color, zorder=6)
    ax.text(x, y + height * 0.02, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=6)
    ax.text(x, y - height * 0.26, subtitle, ha='center', va='center', fontsize=7.5, color="#64748B", zorder=6)

def generate_use_case_diagram_png(output_path):
    fig, ax = plt.subplots(figsize=(20, 13.5), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 13.5)
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    header = FancyBboxPatch((0.5, 12.3), 19.0, 0.9, boxstyle="round,pad=0,rounding_size=0.15",
                            facecolor="#0F172A", edgecolor="#1E293B", linewidth=1.5, zorder=3)
    ax.add_patch(header)
    ax.text(0.8, 12.85, "UML 2.5 USE CASE MODEL", fontsize=9.5, fontweight='bold', color="#38BDF8")
    ax.text(0.8, 12.52, "Research Rover: Comprehensive System Functional Capabilities", fontsize=15, fontweight='bold', color="#FFFFFF")
    ax.text(19.2, 12.65, "M.Tech Software Architecture Specification", ha='right', va='center', fontsize=9.5, color="#94A3B8")

    # =========================================================================
    # SYSTEM BOUNDARY: RESEARCH ROVER
    # =========================================================================
    boundary = FancyBboxPatch((3.0, 0.7), 13.8, 11.3, boxstyle="round,pad=0,rounding_size=0.25",
                              facecolor="#FAFAFA", edgecolor="#3B82F6", linewidth=2.5, linestyle="--", zorder=2)
    ax.add_patch(boundary)
    
    # Boundary Title Tag
    tag_box = FancyBboxPatch((3.3, 11.65), 4.2, 0.45, boxstyle="round,pad=0,rounding_size=0.1",
                             facecolor="#2563EB", edgecolor="none", zorder=3)
    ax.add_patch(tag_box)
    ax.text(5.4, 11.87, "SYSTEM BOUNDARY: RESEARCH ROVER", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#FFFFFF")

    # =========================================================================
    # PRIMARY ACTOR (LEFT)
    # =========================================================================
    actor_card = FancyBboxPatch((0.5, 5.0), 2.2, 3.2, boxstyle="round,pad=0,rounding_size=0.2",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.8, zorder=3)
    ax.add_patch(actor_card)
    draw_stick_figure(ax, 1.6, 6.7, scale=1.1, color="#1D4ED8")
    ax.text(1.6, 5.75, "<<human actor>>", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1E40AF")
    ax.text(1.6, 5.45, "Researcher / Student", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0F172A")
    ax.text(1.6, 5.2, "(Primary User)", ha='center', va='center', fontsize=8, color="#64748B")

    # =========================================================================
    # FUNCTIONAL GROUP RECTANGLES INSIDE BOUNDARY
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # A. RESEARCH PAPER SEARCH MODULE
    # -------------------------------------------------------------------------
    grp_search = FancyBboxPatch((3.3, 9.25), 13.2, 2.3, boxstyle="round,pad=0,rounding_size=0.18",
                                facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_search)
    ax.text(3.5, 11.3, "A. RESEARCH PAPER SEARCH MODULE", fontsize=9.5, fontweight='bold', color="#1E40AF")
    
    # Base Search Use Case
    draw_usecase_oval(ax, 4.8, 10.35, 2.4, 0.65, "Search Research Papers", "(Base Search Query)", fillcolor="#EFF6FF", edgecolor="#2563EB", is_base=True)
    
    # Specializations (Generalizations)
    draw_usecase_oval(ax, 7.8, 11.0, 2.1, 0.5, "Unified Search", "(PubMed + OpenAlex)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 7.8, 10.35, 2.1, 0.5, "PubMed Search", "(Biomedical MeSH Focus)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 7.8, 9.7, 2.1, 0.5, "OpenAlex Search", "(Multidisciplinary Works)", fillcolor="#F8FAFC", edgecolor="#3B82F6")
    
    # Includes / Extends in Search
    draw_usecase_oval(ax, 10.6, 10.85, 2.2, 0.52, "Optimize & Expand Query", "(MeSH & Domain Acronyms)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 10.6, 9.85, 2.2, 0.52, "Re-Rank by Relevance", "(MedCPT Cross-Encoder)", fillcolor="#FAF5FF", edgecolor="#9333EA")
    draw_usecase_oval(ax, 13.4, 10.85, 2.3, 0.55, "Browse Search Results", "(Paginated Paper Cards)", fillcolor="#F0FDF4", edgecolor="#16A34A", is_base=True)
    draw_usecase_oval(ax, 13.4, 9.85, 2.2, 0.52, "Download Available PDF", "(SSRF-Protected Stream)", fillcolor="#FFF1F2", edgecolor="#E11D48")
    draw_usecase_oval(ax, 15.65, 10.35, 1.8, 0.5, "Cancel In-Flight Search", "(Cooperative Abort)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Search
    # Generalization arrows (Unified/PubMed/OpenAlex -> Search)
    ax.annotate("", xy=(6.0, 10.5), xytext=(6.75, 10.9), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))
    ax.annotate("", xy=(6.0, 10.35), xytext=(6.75, 10.35), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))
    ax.annotate("", xy=(6.0, 10.2), xytext=(6.75, 9.8), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.3, mutation_scale=12))

    # Includes: Search -> QueryOpt, Search -> Browse
    ax.annotate("", xy=(9.5, 10.85), xytext=(6.0, 10.5), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(7.6, 10.68, "<<include>>", fontsize=7.5, color="#475569", fontweight='bold')

    ax.annotate("", xy=(12.25, 10.85), xytext=(6.0, 10.4), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(9.0, 10.45, "<<include>>", fontsize=7.5, color="#475569", fontweight='bold')

    # Extend: Re-rank -> Search
    ax.annotate("", xy=(6.0, 10.15), xytext=(9.5, 9.85), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.2, ls="--", mutation_scale=10))
    ax.text(7.6, 9.95, "<<extend>>", fontsize=7.5, color="#9333EA", fontweight='bold')

    # Extend: PDF -> Browse
    ax.annotate("", xy=(13.4, 10.57), xytext=(13.4, 10.11), arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.2, ls="--", mutation_scale=10))
    ax.text(13.48, 10.32, "<<extend>>", fontsize=7.5, color="#E11D48", fontweight='bold')

    # -------------------------------------------------------------------------
    # B. DATASET MANAGEMENT MODULE
    # -------------------------------------------------------------------------
    grp_dataset = FancyBboxPatch((3.3, 7.65), 13.2, 1.45, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_dataset)
    ax.text(3.5, 8.88, "B. DATASET MANAGEMENT MODULE", fontsize=9.5, fontweight='bold', color="#0369A1")

    draw_usecase_oval(ax, 5.0, 8.25, 2.5, 0.58, "Upload Custom Dataset", "(CSV Validation & Encoding)", fillcolor="#F0F9FF", edgecolor="#0284C7", is_base=True)
    draw_usecase_oval(ax, 8.3, 8.25, 2.5, 0.58, "List & Switch Datasets", "(Auto-Discovered from data/)", fillcolor="#F8FAFC", edgecolor="#0284C7")
    draw_usecase_oval(ax, 11.6, 8.25, 2.5, 0.58, "Export Clean Dataset CSV", "(Unpolluted Research Columns)", fillcolor="#F8FAFC", edgecolor="#0284C7")
    draw_usecase_oval(ax, 14.8, 8.25, 2.4, 0.58, "Delete Dataset & Index", "(File Storage Clean-up)", fillcolor="#FEF2F2", edgecolor="#DC2626")

    # -------------------------------------------------------------------------
    # C. KEYWORD BIBLIOMETRIC ANALYTICS MODULE
    # -------------------------------------------------------------------------
    grp_keyword = FancyBboxPatch((3.3, 5.3), 13.2, 2.2, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=1.4, zorder=3)
    ax.add_patch(grp_keyword)
    ax.text(3.5, 7.28, "C. KEYWORD BIBLIOMETRIC ANALYTICS MODULE", fontsize=9.5, fontweight='bold', color="#0284C7")

    draw_usecase_oval(ax, 4.8, 6.35, 2.4, 0.65, "Analyse Keywords", "(5-Phase Computation Pipeline)", fillcolor="#F0F9FF", edgecolor="#0284C7", is_base=True)

    draw_usecase_oval(ax, 7.9, 6.95, 2.3, 0.48, "Normalize & Alias Map", "(AST Parser & Deduplication)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 6.35, 2.3, 0.48, "View Frequency & Rank", "(Distribution Bar Charts)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 5.75, 2.3, 0.48, "NetworkX Centralities", "(Degree, Betweenness, Eigen)", fillcolor="#F8FAFC", edgecolor="#64748B")

    draw_usecase_oval(ax, 10.9, 6.75, 2.4, 0.52, "Explore SVG Word Cloud", "(Interactive Zoom / Pan / Tooltips)", fillcolor="#EFF6FF", edgecolor="#3B82F6")
    draw_usecase_oval(ax, 10.9, 5.95, 2.4, 0.52, "Explore Co-Occurrence Graph", "(Weighted Pairwise Links)", fillcolor="#EFF6FF", edgecolor="#3B82F6")

    draw_usecase_oval(ax, 14.2, 6.75, 2.4, 0.52, "Binary Presence Matrix", "(Paper-Keyword 0/1 Association)", fillcolor="#F0FDF4", edgecolor="#16A34A")
    draw_usecase_oval(ax, 14.2, 5.95, 2.4, 0.52, "Export Analytics Artifacts", "(CSV, JSON & Visual Exports)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Keywords
    # Includes: AnalyseKW -> Norm, Freq, Centrality
    ax.annotate("", xy=(6.75, 6.9), xytext=(6.0, 6.5), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 6.35), xytext=(6.0, 6.35), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 5.8), xytext=(6.0, 6.2), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(6.15, 6.75, "<<include>>", fontsize=7, color="#475569", fontweight='bold')

    # Extends: WordCloud, Cooccur -> AnalyseKW
    ax.annotate("", xy=(6.0, 6.45), xytext=(9.7, 6.75), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.0, 6.25), xytext=(9.7, 5.95), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2, ls="--", mutation_scale=10))
    ax.text(8.2, 6.62, "<<extend>>", fontsize=7.5, color="#2563EB", fontweight='bold')

    # -------------------------------------------------------------------------
    # D. COUNTRY & INTERNATIONAL COLLABORATION MODULE
    # -------------------------------------------------------------------------
    grp_country = FancyBboxPatch((3.3, 3.0), 13.2, 2.15, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#FFFFFF", edgecolor="#A7F3D0", linewidth=1.4, zorder=3)
    ax.add_patch(grp_country)
    ax.text(3.5, 4.95, "D. COUNTRY & INTERNATIONAL COLLABORATION MODULE", fontsize=9.5, fontweight='bold', color="#047857")

    draw_usecase_oval(ax, 4.8, 4.05, 2.4, 0.65, "Country Analysis", "(Bibliometric Affiliation Mapping)", fillcolor="#ECFDF5", edgecolor="#059669", is_base=True)

    draw_usecase_oval(ax, 7.9, 4.65, 2.3, 0.48, "Extract Affiliations", "(Regex & ISO-3166-1 Lexicon)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 4.05, 2.3, 0.48, "Track Unassigned Papers", "(Data Quality & Transparency)", fillcolor="#FFF7ED", edgecolor="#EA580C")
    draw_usecase_oval(ax, 7.9, 3.45, 2.3, 0.48, "Country Rankings Table", "(Searchable Volumes & Share)", fillcolor="#F8FAFC", edgecolor="#64748B")

    draw_usecase_oval(ax, 10.9, 4.45, 2.4, 0.52, "Explore TopoJSON World Map", "(Choropleth Shading & Tooltips)", fillcolor="#ECFDF5", edgecolor="#10B981")
    draw_usecase_oval(ax, 10.9, 3.65, 2.4, 0.52, "Explore 2D/3D Collaboration", "(Force-Directed & Three.js Graphs)", fillcolor="#ECFDF5", edgecolor="#10B981")

    draw_usecase_oval(ax, 14.2, 4.05, 2.4, 0.55, "Export Country Data", "(Rankings & Collaboration CSVs)", fillcolor="#F8FAFC", edgecolor="#64748B")

    # Connectors for Country
    ax.annotate("", xy=(6.75, 4.6), xytext=(6.0, 4.2), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 4.05), xytext=(6.0, 4.05), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.75, 3.5), xytext=(6.0, 3.9), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(6.15, 4.45, "<<include>>", fontsize=7, color="#475569", fontweight='bold')

    ax.annotate("", xy=(6.0, 4.15), xytext=(9.7, 4.45), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--", mutation_scale=10))
    ax.annotate("", xy=(6.0, 3.95), xytext=(9.7, 3.65), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--", mutation_scale=10))
    ax.text(8.2, 4.35, "<<extend>>", fontsize=7.5, color="#059669", fontweight='bold')

    # -------------------------------------------------------------------------
    # E. AI RESEARCH ASSISTANT (CONVERSATIONAL RAG) MODULE
    # -------------------------------------------------------------------------
    grp_ai = FancyBboxPatch((3.3, 0.95), 13.2, 1.9, boxstyle="round,pad=0,rounding_size=0.18",
                            facecolor="#FFFFFF", edgecolor="#DDD6FE", linewidth=1.4, zorder=3)
    ax.add_patch(grp_ai)
    ax.text(3.5, 2.65, "E. AI RESEARCH ASSISTANT (CONVERSATIONAL RAG) MODULE", fontsize=9.5, fontweight='bold', color="#6D28D9")

    draw_usecase_oval(ax, 4.8, 1.85, 2.4, 0.65, "Ask Research Questions", "(Conversational RAG Q&A)", fillcolor="#F5F3FF", edgecolor="#7C3AED", is_base=True)

    draw_usecase_oval(ax, 7.9, 2.3, 2.3, 0.48, "Generate Vector Embeddings", "(all-mpnet-base-v2, 768-d)", fillcolor="#F8FAFC", edgecolor="#64748B")
    draw_usecase_oval(ax, 7.9, 1.4, 2.3, 0.48, "Decompose Query", "(Sub-Question Search Strategy)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")

    draw_usecase_oval(ax, 10.9, 2.3, 2.4, 0.48, "Retrieve FAISS Chunks", "(Top-K Nearest Neighbor Vector Search)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")
    draw_usecase_oval(ax, 10.9, 1.4, 2.4, 0.48, "Scrape Full-Text Content", "(Deep Web Scraper with Fallback)", fillcolor="#FAF5FF", edgecolor="#8B5CF6")

    draw_usecase_oval(ax, 14.2, 1.85, 2.4, 0.58, "Synthesize Grounded Answer", "(Gemini LLM + Paper Citations)", fillcolor="#FDF2F8", edgecolor="#DB2777", is_base=True)

    # Connectors for AI
    ax.annotate("", xy=(6.75, 1.4), xytext=(6.0, 1.75), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(6.15, 1.6, "<<include>>", fontsize=7, color="#475569", fontweight='bold')

    ax.annotate("", xy=(9.7, 2.3), xytext=(6.0, 1.85), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(8.0, 2.1, "<<include>>", fontsize=7, color="#475569", fontweight='bold')

    ax.annotate("", xy=(13.0, 1.85), xytext=(6.0, 1.85), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2, ls="--", mutation_scale=10))
    ax.text(9.5, 1.92, "<<include>>", fontsize=7.5, color="#475569", fontweight='bold')

    # Extend Scrape -> Embeddings
    ax.annotate("", xy=(7.9, 2.06), xytext=(9.7, 1.55), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.2, ls="--", mutation_scale=10))
    ax.text(8.5, 1.7, "<<extend>>", fontsize=7, color="#8B5CF6", fontweight='bold')

    # =========================================================================
    # ASSOCIATIONS: PRIMARY USER -> BASE USE CASES
    # =========================================================================
    # User -> Search
    ax.annotate("", xy=(3.6, 10.35), xytext=(2.7, 6.8), arrowprops=dict(arrowstyle="-", color="#2563EB", lw=1.8))
    # User -> Dataset
    ax.annotate("", xy=(3.75, 8.25), xytext=(2.7, 6.7), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.8))
    # User -> Keyword
    ax.annotate("", xy=(3.6, 6.35), xytext=(2.7, 6.6), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.8))
    # User -> Country
    ax.annotate("", xy=(3.6, 4.05), xytext=(2.7, 6.4), arrowprops=dict(arrowstyle="-", color="#059669", lw=1.8))
    # User -> AI
    ax.annotate("", xy=(3.6, 1.85), xytext=(2.7, 6.2), arrowprops=dict(arrowstyle="-", color="#7C3AED", lw=1.8))

    # =========================================================================
    # EXTERNAL SYSTEM ACTORS (RIGHT)
    # =========================================================================
    draw_external_actor(ax, 18.2, 11.0, 2.4, 0.9, "NCBI Entrez API", "esearch / efetch / espell", tag_color="#0284C7")
    draw_external_actor(ax, 18.2, 9.8, 2.4, 0.9, "OpenAlex API", "Works, Citations & OA Data", tag_color="#0D9488")
    draw_external_actor(ax, 18.2, 8.4, 2.4, 0.9, "Publishers & PMC", "Open-Access PDF Providers", tag_color="#E11D48")
    draw_external_actor(ax, 18.2, 1.85, 2.4, 0.9, "Google Gemini AI", "LLM Grounded Synthesis", tag_color="#9333EA")

    # Dotted Associations to External Systems
    ax.annotate("", xy=(17.0, 11.0), xytext=(8.85, 10.35), arrowprops=dict(arrowstyle="-", color="#0284C7", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 9.8), xytext=(8.85, 9.7), arrowprops=dict(arrowstyle="-", color="#0D9488", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 8.4), xytext=(14.5, 9.85), arrowprops=dict(arrowstyle="-", color="#E11D48", lw=1.3, ls=":"))
    ax.annotate("", xy=(17.0, 1.85), xytext=(15.4, 1.85), arrowprops=dict(arrowstyle="-", color="#9333EA", lw=1.3, ls=":"))

    # =========================================================================
    # LEGEND BAR AT BOTTOM
    # =========================================================================
    legend_bar = FancyBboxPatch((0.5, 0.1), 19.0, 0.45, boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0, zorder=3)
    ax.add_patch(legend_bar)
    
    ax.text(0.8, 0.32, "UML 2.5 NOTATION LEGEND:", fontsize=8.5, fontweight='bold', color="#1E293B")
    
    # Association line
    ax.plot([3.5, 4.1], [0.32, 0.32], color="#2563EB", lw=2.0)
    ax.text(4.2, 0.32, "Actor Association", fontsize=8, color="#334155", va='center')
    
    # <<include>> line
    ax.annotate("", xy=(7.2, 0.32), xytext=(6.5, 0.32), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.4, ls="--", mutation_scale=9))
    ax.text(7.3, 0.32, "<<include>> Mandatory Reused Behaviour", fontsize=8, color="#334155", va='center')
    
    # <<extend>> line
    ax.annotate("", xy=(11.5, 0.32), xytext=(10.8, 0.32), arrowprops=dict(arrowstyle="->", color="#9333EA", lw=1.4, ls="--", mutation_scale=9))
    ax.text(11.6, 0.32, "<<extend>> Conditional / Optional Extension", fontsize=8, color="#334155", va='center')
    
    # Generalization line
    ax.annotate("", xy=(16.2, 0.32), xytext=(15.5, 0.32), arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=1.4, mutation_scale=10))
    ax.text(16.3, 0.32, "Generalization (Specialized Search Mode)", fontsize=8, color="#334155", va='center')

    # Save to disk at 300 DPI
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Successfully generated 300 DPI UML Use Case Diagram at: {output_path}")

if __name__ == '__main__':
    out_file = Path("docs/uml/use_case_diagram.png")
    generate_use_case_diagram_png(out_file)
