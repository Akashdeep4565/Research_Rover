"""
Research Rover - Publication-Ready Feature Workflow Flowchart Generator
Generates 5 separate, high-resolution, transparent-background (RGBA) PNG flowcharts
strictly matching the academic journal visual style of the reference flowchart:
- 01_research_search_workflow.png
- 02_bibliometric_analysis_workflow.png
- 03_country_analysis_workflow.png
- 04_dataset_analysis_workflow.png
- ai_research_chat_workflow.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch, Ellipse
from PIL import Image

OUT_DIR = r"E:\Research_Rover\diagram\feature_workflows"
os.makedirs(OUT_DIR, exist_ok=True)

# Publication styling: Times New Roman, black & white, transparent canvas
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

c_edge = '#000000'
c_fill = '#FFFFFF'
c_text = '#000000'
lw = 1.5


def draw_oval(ax, x, y, w, h, text):
    """Start and Finish terminator ovals"""
    oval = Ellipse((x, y), w, h, facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(oval)
    ax.text(x, y, text, fontsize=10.5, fontfamily='Times New Roman', color=c_text,
            ha='center', va='center', zorder=6)


def draw_box(ax, x, y, w, h, lines):
    """Rounded rectangle process boxes matching reference"""
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.0,rounding_size=1.2',
                         facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(box)
    if len(lines) == 1:
        ax.text(x, y, lines[0], fontsize=10.5, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)
    elif len(lines) == 2:
        ax.text(x, y + 0.65, lines[0], fontsize=10, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)
        ax.text(x, y - 0.65, lines[1], fontsize=10, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)
    elif len(lines) == 3:
        ax.text(x, y + 1.1, lines[0], fontsize=9.5, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)
        ax.text(x, y, lines[1], fontsize=9.5, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)
        ax.text(x, y - 1.1, lines[2], fontsize=9.5, fontfamily='Times New Roman', color=c_text,
                ha='center', va='center', zorder=6)


def draw_diamond(ax, x, y, w, h, text):
    """Diamond decision symbols matching reference"""
    pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
    poly = Polygon(pts, closed=True, facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(poly)
    ax.text(x, y, text, fontsize=10, fontfamily='Times New Roman', color=c_text,
            ha='center', va='center', zorder=6)


def draw_arrow(ax, x1, y1, x2, y2):
    """Directional connecting arrow"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='-|>', mutation_scale=11,
                            color=c_edge, linewidth=1.2, zorder=4)
    ax.add_patch(arrow)


def draw_loopback_no(ax, box1_x, box2_x, y_top):
    """Draws downward arrow to No diamond and loopback to Box 1 matching reference"""
    box_half_h = 2.8
    diamond_y = 23.0
    diamond_w = 7.0
    diamond_h = 3.6
    
    # Arrow from Box 2 down to No diamond
    draw_arrow(ax, box2_x, y_top - box_half_h, box2_x, diamond_y + diamond_h / 2)
    # Diamond labeled No
    draw_diamond(ax, box2_x, diamond_y, diamond_w, diamond_h, 'No')
    # Line left from No diamond left tip to box1_x
    diamond_left_x = box2_x - diamond_w / 2
    ax.plot([diamond_left_x, box1_x, box1_x], [diamond_y, diamond_y, y_top - box_half_h],
            color=c_edge, linewidth=1.2, zorder=4)
    # Arrow up into bottom of Box 1
    draw_arrow(ax, box1_x, diamond_y + 0.5, box1_x, y_top - box_half_h)


def save_transparent(fig, filename):
    filepath = os.path.join(OUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, transparent=True, facecolor='none', edgecolor='none',
                bbox_inches='tight', pad_inches=0.08)
    plt.close()
    im = Image.open(filepath)
    print(f"Saved {filename}: size={im.size}, mode={im.mode}, alpha(0,0)={im.getpixel((0,0))[3]}")


# ==============================================================================
# 1. DIAGRAM 1: RESEARCH SEARCH WORKFLOW
# ==============================================================================
def make_search_workflow():
    fig, ax = plt.subplots(figsize=(13.0, 5.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 40)
    ax.axis('off')

    y1, y2 = 33.0, 11.0

    # Start
    draw_oval(ax, 5.5, y1, 6.0, 4.2, 'Start')
    draw_arrow(ax, 8.5, y1, 11.5, y1)

    # Box 1: Formulate Search Query
    draw_box(ax, 19.5, y1, 15.5, 5.6, ['Formulate Search', 'Query & Filters'])
    draw_arrow(ax, 27.25, y1, 30.5, y1)

    # Box 2: Retrieve & Present Papers
    draw_box(ax, 38.5, y1, 15.5, 5.6, ['Retrieve & Present', 'Literature Results'])
    draw_arrow(ax, 46.25, y1, 50.5, y1)

    # Diamond 1: Relevant?
    draw_diamond(ax, 55.5, y1, 9.8, 4.6, 'Relevant')
    draw_arrow(ax, 60.4, y1, 65.5, y1)

    # No loopback branch (under Box 2)
    draw_loopback_no(ax, 19.5, 38.5, y1)

    # Box 3: Inspect Paper Cards
    draw_box(ax, 73.5, y1, 15.5, 5.6, ['Inspect Paper Cards', '& Metadata'])
    draw_arrow(ax, 81.25, y1, 84.5, y1)

    # Box 4: View Abstracts & Details
    draw_box(ax, 92.5, y1, 15.0, 5.6, ['View Abstracts', '& Citations'])

    # Turn down to Row 2
    draw_arrow(ax, 92.5, y1 - 2.8, 92.5, 24.8)

    # Box 5: Download Open-Access PDFs
    draw_box(ax, 92.5, 22.0, 15.0, 5.6, ['Download Open-Access', 'PDFs via Proxy'])
    draw_arrow(ax, 92.5, 22.0 - 2.8, 92.5, y2 + 2.8)

    # Box 6: Save Standardized Corpus
    draw_box(ax, 92.5, y2, 15.0, 5.6, ['Save Standardized', 'Corpus (CSV)'])
    draw_arrow(ax, 85.0, y2, 81.5, y2)

    # Row 2 (flowing right to left)
    # Box 7: Export Literature Results
    draw_box(ax, 73.5, y2, 15.5, 5.6, ['Export Literature', 'Callset & Tables'])
    draw_arrow(ax, 65.75, y2, 62.5, y2)

    # Box 8: Open in Analytics or AI Chat
    draw_box(ax, 54.5, y2, 15.5, 5.6, ['Open in Analytics', 'or AI Chat'])
    draw_arrow(ax, 46.75, y2, 43.5, y2)

    # Finish
    draw_oval(ax, 40.0, y2, 6.0, 4.2, 'Finish')

    save_transparent(fig, "01_research_search_workflow.png")


# ==============================================================================
# 2. DIAGRAM 2: KEYWORD BIBLIOMETRIC ANALYSIS WORKFLOW
# ==============================================================================
def make_bibliometric_workflow():
    fig, ax = plt.subplots(figsize=(13.0, 5.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 40)
    ax.axis('off')

    y1, y2 = 33.0, 11.0

    # Start
    draw_oval(ax, 5.5, y1, 6.0, 4.2, 'Start')
    draw_arrow(ax, 8.5, y1, 11.5, y1)

    # Box 1: Select Corpus File
    draw_box(ax, 19.5, y1, 15.5, 5.6, ['Select Literature', 'Corpus (CSV)'])
    draw_arrow(ax, 27.25, y1, 30.5, y1)

    # Box 2: Configure Keyword Parameters
    draw_box(ax, 38.5, y1, 15.5, 5.6, ['Configure Keyword', 'Parameters & Bounds'])
    draw_arrow(ax, 46.25, y1, 50.5, y1)

    # Diamond 1: Valid?
    draw_diamond(ax, 55.5, y1, 9.8, 4.6, 'Valid')
    draw_arrow(ax, 60.4, y1, 65.5, y1)

    # No loopback branch (under Box 2)
    draw_loopback_no(ax, 19.5, 38.5, y1)

    # Box 3: Compute Keyword Frequencies
    draw_box(ax, 73.5, y1, 15.5, 5.6, ['Compute Keyword', 'Frequencies & Aliases'])
    draw_arrow(ax, 81.25, y1, 84.5, y1)

    # Box 4: Render Interactive Word Cloud
    draw_box(ax, 92.5, y1, 15.0, 5.6, ['Render Interactive', 'Word Cloud'])

    # Turn down to Row 2
    draw_arrow(ax, 92.5, y1 - 2.8, 92.5, 24.8)

    # Box 5: Inspect Frequency Rankings
    draw_box(ax, 92.5, 22.0, 15.0, 5.6, ['Inspect Keyword', 'Ranking Table'])
    draw_arrow(ax, 92.5, 22.0 - 2.8, 92.5, y2 + 2.8)

    # Box 6: Build Co-occurrence Matrix
    draw_box(ax, 92.5, y2, 15.0, 5.6, ['Generate Co-occurrence', 'Presence Matrix'])
    draw_arrow(ax, 85.0, y2, 81.5, y2)

    # Row 2 (flowing right to left)
    # Box 7: Calculate Centrality Metrics
    draw_box(ax, 73.5, y2, 15.5, 5.6, ['Calculate Network', 'Centrality Metrics'])
    draw_arrow(ax, 65.75, y2, 62.5, y2)

    # Box 8: Export Keyword Data
    draw_box(ax, 54.5, y2, 15.5, 5.6, ['Export Frequency CSV', '& Matrix Data'])
    draw_arrow(ax, 46.75, y2, 43.5, y2)

    # Finish
    draw_oval(ax, 40.0, y2, 6.0, 4.2, 'Finish')

    save_transparent(fig, "02_bibliometric_analysis_workflow.png")


# ==============================================================================
# 3. DIAGRAM 3: COUNTRY & COLLABORATION ANALYSIS WORKFLOW
# ==============================================================================
def make_country_workflow():
    fig, ax = plt.subplots(figsize=(13.0, 5.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 40)
    ax.axis('off')

    y1, y2 = 33.0, 11.0

    # Start
    draw_oval(ax, 5.5, y1, 6.0, 4.2, 'Start')
    draw_arrow(ax, 8.5, y1, 11.5, y1)

    # Box 1: Select Literature Dataset
    draw_box(ax, 19.5, y1, 15.5, 5.6, ['Select Literature', 'Dataset'])
    draw_arrow(ax, 27.25, y1, 30.5, y1)

    # Box 2: Extract Author Affiliations
    draw_box(ax, 38.5, y1, 15.5, 5.6, ['Extract Author', 'Affiliations'])
    draw_arrow(ax, 46.25, y1, 50.5, y1)

    # Diamond 1: Detected?
    draw_diamond(ax, 55.5, y1, 9.8, 4.6, 'Detected')
    draw_arrow(ax, 60.4, y1, 65.5, y1)

    # No loopback branch (under Box 2)
    draw_loopback_no(ax, 19.5, 38.5, y1)

    # Box 3: Normalize Country Codes (ISO-3)
    draw_box(ax, 73.5, y1, 15.5, 5.6, ['Normalize Country', 'Codes (ISO-3)'])
    draw_arrow(ax, 81.25, y1, 84.5, y1)

    # Box 4: Render Choropleth World Map
    draw_box(ax, 92.5, y1, 15.0, 5.6, ['Render Choropleth', 'World Map'])

    # Turn down to Row 2
    draw_arrow(ax, 92.5, y1 - 2.8, 92.5, 24.8)

    # Box 5: Inspect National Shares
    draw_box(ax, 92.5, 22.0, 15.0, 5.6, ['Inspect Country', 'Publication Shares'])
    draw_arrow(ax, 92.5, 22.0 - 2.8, 92.5, y2 + 2.8)

    # Box 6: Build Weighted Collaboration Edges
    draw_box(ax, 92.5, y2, 15.0, 5.6, ['Build Weighted', 'Collaboration Edges'])
    draw_arrow(ax, 85.0, y2, 81.5, y2)

    # Row 2 (flowing right to left)
    # Box 7: Interact with 2D / 3D Network Graphs
    draw_box(ax, 73.5, y2, 15.5, 5.6, ['Interact with 2D / 3D', 'Network Graphs'])
    draw_arrow(ax, 65.75, y2, 62.5, y2)

    # Box 8: Export Country Stats & Network Data
    draw_box(ax, 54.5, y2, 15.5, 5.6, ['Export Country Stats', '& Edge Network Data'])
    draw_arrow(ax, 46.75, y2, 43.5, y2)

    # Finish
    draw_oval(ax, 40.0, y2, 6.0, 4.2, 'Finish')

    save_transparent(fig, "03_country_analysis_workflow.png")


# ==============================================================================
# 4. DIAGRAM 4: DATASET UPLOAD & QUALITY MANAGEMENT WORKFLOW
# ==============================================================================
def make_dataset_workflow():
    fig, ax = plt.subplots(figsize=(13.0, 5.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 40)
    ax.axis('off')

    y1, y2 = 33.0, 11.0

    # Start
    draw_oval(ax, 5.5, y1, 6.0, 4.2, 'Start')
    draw_arrow(ax, 8.5, y1, 11.5, y1)

    # Box 1: Initiate Dataset Upload Action
    draw_box(ax, 19.5, y1, 15.5, 5.6, ['Initiate Dataset', 'Upload Action'])
    draw_arrow(ax, 27.25, y1, 30.5, y1)

    # Box 2: Validate Schema & Encoding
    draw_box(ax, 38.5, y1, 15.5, 5.6, ['Validate CSV Schema', '& Encoding (UTF-8)'])
    draw_arrow(ax, 46.25, y1, 50.5, y1)

    # Diamond 1: Valid?
    draw_diamond(ax, 55.5, y1, 9.8, 4.6, 'Valid')
    draw_arrow(ax, 60.4, y1, 65.5, y1)

    # No loopback branch (under Box 2)
    draw_loopback_no(ax, 19.5, 38.5, y1)

    # Box 3: Inspect Dataset Quality Report
    draw_box(ax, 73.5, y1, 15.5, 5.6, ['Inspect Dataset', 'Quality Report'])
    draw_arrow(ax, 81.25, y1, 84.5, y1)

    # Box 4: Normalize Canonical Fields
    draw_box(ax, 92.5, y1, 15.0, 5.6, ['Normalize Canonical', 'Field Mappings'])

    # Turn down to Row 2
    draw_arrow(ax, 92.5, y1 - 2.8, 92.5, 24.8)

    # Box 5: Clean Missing & Duplicates
    draw_box(ax, 92.5, 22.0, 15.0, 5.6, ['Clean Missing Values', '& Deduplicate Rows'])
    draw_arrow(ax, 92.5, 22.0 - 2.8, 92.5, y2 + 2.8)

    # Box 6: Register in System Repository
    draw_box(ax, 92.5, y2, 15.0, 5.6, ['Register Corpus in', 'System Repository'])
    draw_arrow(ax, 85.0, y2, 81.5, y2)

    # Row 2 (flowing right to left)
    # Box 7: Sync Across Modules
    draw_box(ax, 73.5, y2, 15.5, 5.6, ['Activate Dataset in', 'Search, Analytics, Chat'])
    draw_arrow(ax, 65.75, y2, 62.5, y2)

    # Box 8: Confirm Literature Readiness
    draw_box(ax, 54.5, y2, 15.5, 5.6, ['Confirm Literature', 'Corpus Readiness'])
    draw_arrow(ax, 46.75, y2, 43.5, y2)

    # Finish
    draw_oval(ax, 40.0, y2, 6.0, 4.2, 'Finish')

    save_transparent(fig, "04_dataset_analysis_workflow.png")


# ==============================================================================
# 5. DIAGRAM 5: AI RESEARCH CHAT WORKFLOW
# ==============================================================================
def make_chat_workflow():
    fig, ax = plt.subplots(figsize=(13.0, 5.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(4, 40)
    ax.axis('off')

    y1, y2 = 33.0, 11.0

    # Start
    draw_oval(ax, 5.5, y1, 6.0, 4.2, 'Start')
    draw_arrow(ax, 8.5, y1, 11.5, y1)

    # Box 1: Open AI Research Chat Interface
    draw_box(ax, 19.5, y1, 15.5, 5.6, ['Open AI Research', 'Chat Interface'])
    draw_arrow(ax, 27.25, y1, 30.5, y1)

    # Box 2: Verify Corpus Vector Index
    draw_box(ax, 38.5, y1, 15.5, 5.6, ['Verify Corpus', 'Vector Index (FAISS)'])
    draw_arrow(ax, 46.25, y1, 50.5, y1)

    # Diamond 1: Indexed?
    draw_diamond(ax, 55.5, y1, 9.8, 4.6, 'Indexed')
    draw_arrow(ax, 60.4, y1, 65.5, y1)

    # No loopback branch (under Box 2): If not indexed, build index and loop back
    draw_loopback_no(ax, 19.5, 38.5, y1)

    # Box 3: Submit Research Query / Prompt
    draw_box(ax, 73.5, y1, 15.5, 5.6, ['Submit Research', 'Query / Question'])
    draw_arrow(ax, 81.25, y1, 84.5, y1)

    # Box 4: Retrieve Semantic Context Chunks
    draw_box(ax, 92.5, y1, 15.0, 5.6, ['Retrieve Semantic', 'Context Chunks'])

    # Turn down to Row 2
    draw_arrow(ax, 92.5, y1 - 2.8, 92.5, 24.8)

    # Box 5: Assemble Grounded Context
    draw_box(ax, 92.5, 22.0, 15.0, 5.6, ['Assemble Grounded', 'Literature Context'])
    draw_arrow(ax, 92.5, 22.0 - 2.8, 92.5, y2 + 2.8)

    # Box 6: Synthesize AI Response
    draw_box(ax, 92.5, y2, 15.0, 5.6, ['Synthesize Referenced', 'AI Response (RAG)'])
    draw_arrow(ax, 85.0, y2, 81.5, y2)

    # Row 2 (flowing right to left)
    # Box 7: Inspect Answers & Citations
    draw_box(ax, 73.5, y2, 15.5, 5.6, ['Inspect Answer &', 'Clickable Citations'])
    draw_arrow(ax, 65.75, y2, 62.5, y2)

    # Box 8: Verify Source DOIs / Papers
    draw_box(ax, 54.5, y2, 15.5, 5.6, ['Open Cited DOI &', 'Source Abstracts'])
    draw_arrow(ax, 46.75, y2, 43.5, y2)

    # Finish
    draw_oval(ax, 40.0, y2, 6.0, 4.2, 'Finish')

    save_transparent(fig, "ai_research_chat_workflow.png")


if __name__ == '__main__':
    print("=" * 70)
    print("GENERATING ALL 5 INDEPENDENT RESEARCH ROVER WORKFLOW FLOWCHARTS")
    print("=" * 70)
    make_search_workflow()
    make_bibliometric_workflow()
    make_country_workflow()
    make_dataset_workflow()
    make_chat_workflow()
    print("=" * 70)
    print("ALL 5 DIAGRAMS GENERATED SUCCESSFULLY IN diagram/feature_workflows/")
    print("=" * 70)
