"""
Research Rover - Publication-Ready Feature Workflow Flowchart Generator (Polished)
Generates 5 distinct, logically authentic, publication-quality PNG flowcharts:
1. 01_research_search_workflow.png (Vertical Search & Refinement Loop)
2. 02_bibliometric_analysis_workflow.png (3-Way Analytical Fork-and-Join)
3. 03_country_analysis_workflow.png (Affiliation Gate & Dual Geographical/Network Stream)
4. 04_dataset_analysis_workflow.png (Two-Gate Data Quality & Validation Pipeline)
5. ai_research_chat_workflow.png (RAG Pipeline with Index Prep & Conversational Loop)
"""

import os
os.environ["MPLCONFIGDIR"] = r"E:\Research_Rover\scratch"
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch, Ellipse
from PIL import Image

OUT_DIR = r"E:\Research_Rover\diagram\feature_workflows"
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

c_edge = '#000000'
c_fill = '#FFFFFF'
c_text = '#000000'
lw = 1.3


def draw_oval(ax, x, y, w, h, text):
    oval = Ellipse((x, y), w, h, facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(oval)
    ax.text(x, y, text, fontsize=10.5, fontfamily='Times New Roman', color=c_text,
            ha='center', va='center', zorder=6)


def draw_box(ax, x, y, w, h, text, font_size=10.0):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.0,rounding_size=1.2',
                         facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(box)
    ax.text(x, y, text, fontsize=font_size, fontfamily='Times New Roman', color=c_text,
            ha='center', va='center', linespacing=1.25, zorder=6)


def draw_diamond(ax, x, y, w, h, text, font_size=9.5):
    pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
    poly = Polygon(pts, closed=True, facecolor=c_fill, edgecolor=c_edge, linewidth=lw, zorder=5)
    ax.add_patch(poly)
    ax.text(x, y, text, fontsize=font_size, fontfamily='Times New Roman', color=c_text,
            ha='center', va='center', linespacing=1.2, zorder=6)


def draw_arrow(ax, x1, y1, x2, y2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='-|>', mutation_scale=11,
                            color=c_edge, linewidth=1.1, zorder=4)
    ax.add_patch(arrow)


def save_transparent(fig, filename):
    filepath = os.path.join(OUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, transparent=True, facecolor='none', edgecolor='none',
                bbox_inches='tight', pad_inches=0.08)
    plt.close()
    im = Image.open(filepath)
    print(f"Saved {filename}: {im.size} px, mode={im.mode}, alpha(0,0)={im.getpixel((0,0))[3]}")


# ==============================================================================
# 1. RESEARCH SEARCH WORKFLOW (Vertical Pipeline with Refinement Loop)
# ==============================================================================
def make_search_workflow():
    fig, ax = plt.subplots(figsize=(6.8, 10.2), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis('off')

    cx = 45.0  # Main vertical spine
    loop_x = 84.0

    # 1. Start
    draw_oval(ax, cx, 114, 18, 5.5, 'Start')
    draw_arrow(ax, cx, 111.25, cx, 106.8)

    # 2. Enter Search Query & Filters
    draw_box(ax, cx, 103, 42, 7.5, 'Enter Research Query\n& Select Search Filters')
    draw_arrow(ax, cx, 99.25, cx, 94.8)

    # 3. Retrieve & Deduplicate
    draw_box(ax, cx, 91, 46, 7.5, 'Query APIs & Deduplicate Papers\n(OpenAlex, arXiv, Crossref)')
    draw_arrow(ax, cx, 87.25, cx, 81.8)

    # 4. Decision: Relevant Papers Found?
    draw_diamond(ax, cx, 76, 32, 10.0, 'Relevant Papers\nFound?')

    # Branch No -> loop back to Box 2
    # Horizontal line out to loop_x
    ax.plot([cx + 16, loop_x, loop_x], [76, 76, 103], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, loop_x, 103, cx + 21, 103)
    ax.text(cx + 17.5, 77.8, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom')

    # Branch Yes -> proceed to results
    draw_arrow(ax, cx, 71.0, cx, 65.8)
    ax.text(cx + 2.0, 68.5, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 5. Display Paper Cards
    draw_box(ax, cx, 62, 44, 7.5, 'Display Interactive Paper Cards\n& Metadata Summary')
    draw_arrow(ax, cx, 58.25, cx, 53.8)

    # 6. Inspect Abstracts & Citations
    draw_box(ax, cx, 50, 44, 7.5, 'Inspect Full Abstracts,\nAuthor Metadata & Citations')
    draw_arrow(ax, cx, 46.25, cx, 41.8)

    # 7. Download Open-Access PDFs
    draw_box(ax, cx, 38, 44, 7.5, 'Download Open-Access PDFs\nvia System Backend Proxy')
    draw_arrow(ax, cx, 34.25, cx, 29.8)

    # 8. Save Corpus CSV
    draw_box(ax, cx, 26, 44, 7.5, 'Save Standardized Corpus (CSV)\nto System Data Repository')
    draw_arrow(ax, cx, 22.25, cx, 17.8)

    # 9. Hand off to Analytics / Chat
    draw_box(ax, cx, 14, 44, 7.5, 'Hand Off Corpus Directly to\nAnalytics or AI Research Chat')
    draw_arrow(ax, cx, 10.25, cx, 6.0)

    # 10. Finish
    draw_oval(ax, cx, 3.25, 18, 5.5, 'Finish')

    save_transparent(fig, "01_research_search_workflow.png")


# ==============================================================================
# 2. KEYWORD BIBLIOMETRIC ANALYSIS WORKFLOW (3-Way Analytical Fork-and-Join)
# ==============================================================================
def make_bibliometric_workflow():
    fig, ax = plt.subplots(figsize=(10.5, 9.2), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.axis('off')

    cx = 52.5

    # 1. Start
    draw_oval(ax, cx, 100, 18, 5.5, 'Start')
    draw_arrow(ax, cx, 97.25, cx, 93.3)

    # 2. Select Corpus
    draw_box(ax, cx, 89.5, 42, 7.5, 'Select Literature Corpus\n(Active Search / Saved CSV)')
    draw_arrow(ax, cx, 85.75, cx, 81.8)

    # 3. Configure Parameters
    draw_box(ax, cx, 78, 42, 7.5, 'Configure Keyword Limits\n& Frequency Thresholds')
    draw_arrow(ax, cx, 74.25, cx, 70.3)

    # 4. Extract & Normalize Keywords
    draw_box(ax, cx, 66.5, 44, 7.5, 'Extract, Clean & Merge Synonyms\nvia Keyword Alias Dictionary')

    # Fork junction at Y = 57.5
    fork_y = 57.0
    ax.plot([cx, cx], [62.75, fork_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([19, 86], [fork_y, fork_y], color=c_edge, linewidth=1.1, zorder=4)

    # 3 Parallel Columns: X = 19, X = 52.5, X = 86
    # Left Branch: Word Cloud
    draw_arrow(ax, 19, fork_y, 19, 52.3)
    draw_box(ax, 19, 46.5, 29, 9.5, 'Render Interactive\nWord Cloud View\n(Visual Prominence)')

    # Center Branch: Frequency Table
    draw_arrow(ax, cx, fork_y, cx, 52.3)
    draw_box(ax, cx, 46.5, 29, 9.5, 'Compute Top Keyword\nFrequency Rankings\n(Counts & Shares)')

    # Right Branch: Co-occurrence Matrix
    draw_arrow(ax, 86, fork_y, 86, 52.3)
    draw_box(ax, 86, 46.5, 29, 9.5, 'Generate Co-occurrence\nPresence Matrix\n(N x N Network Edges)')

    # Merge junction at Y = 36.5
    merge_y = 36.5
    ax.plot([19, 19], [41.75, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([cx, cx], [41.75, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([86, 86], [41.75, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([19, 86], [merge_y, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, cx, merge_y, cx, 30.8)

    # 5. Network Centrality
    draw_box(ax, cx, 27, 44, 7.5, 'Calculate Degree Centrality\n& Keyword Association Metrics')
    draw_arrow(ax, cx, 23.25, cx, 19.3)

    # 6. Export Data
    draw_box(ax, cx, 15.5, 42, 7.5, 'Export Frequency Tables &\nCo-occurrence Matrix (CSV)')
    draw_arrow(ax, cx, 11.75, cx, 7.8)

    # 7. Finish
    draw_oval(ax, cx, 5.25, 18, 5.5, 'Finish')

    save_transparent(fig, "02_bibliometric_analysis_workflow.png")


# ==============================================================================
# 3. COUNTRY ANALYSIS WORKFLOW (Affiliation Gate & Dual Geographical/Network Stream)
# ==============================================================================
def make_country_workflow():
    fig, ax = plt.subplots(figsize=(10.0, 10.5), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis('off')

    cx = 45.0
    loop_x = 84.0

    # 1. Start
    draw_oval(ax, cx, 114, 18, 5.5, 'Start')
    draw_arrow(ax, cx, 111.25, cx, 106.8)

    # 2. Select Corpus
    draw_box(ax, cx, 103, 38, 7.5, 'Select Literature Corpus\n(CSV Dataset)')
    draw_arrow(ax, cx, 99.25, cx, 94.8)

    # 3. Parse Affiliation Strings
    draw_box(ax, cx, 91, 40, 7.5, 'Parse Author Affiliation\nStrings from Metadata')
    draw_arrow(ax, cx, 87.25, cx, 81.8)

    # 4. Decision: Affiliations Detected?
    draw_diamond(ax, cx, 76, 30, 9.5, 'Affiliations\nDetected?')

    # No branch -> prompt corpus selection loopback
    ax.plot([cx + 15, loop_x, loop_x], [76, 76, 103], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, loop_x, 103, cx + 19, 103)
    ax.text(cx + 16.5, 77.8, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom')

    # Yes branch -> normalize ISO-3
    draw_arrow(ax, cx, 71.25, cx, 66.3)
    ax.text(cx + 2.0, 68.8, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 5. Normalize ISO-3
    draw_box(ax, cx, 62.5, 42, 7.5, 'Normalize Country Entities\nto Standard ISO-3 Codes')

    # Dual Stream Fork at Y = 53.5
    fork_y = 53.5
    ax.plot([cx, cx], [58.75, fork_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([23, 67], [fork_y, fork_y], color=c_edge, linewidth=1.1, zorder=4)

    # Stream A: Geographical Distribution (X = 23)
    draw_arrow(ax, 23, fork_y, 23, 48.8)
    draw_box(ax, 23, 45, 34, 7.5, 'Calculate National\nPublication Shares')
    draw_arrow(ax, 23, 41.25, 23, 36.8)
    draw_box(ax, 23, 33, 34, 7.5, 'Render Interactive\nChoropleth World Map')

    # Stream B: Collaboration Network (X = 67)
    draw_arrow(ax, 67, fork_y, 67, 48.8)
    draw_box(ax, 67, 45, 34, 7.5, 'Extract Cross-Border\nCo-authorship Links')
    draw_arrow(ax, 67, 41.25, 67, 36.8)
    draw_box(ax, 67, 33, 34, 7.5, 'Construct 2D / 3D Force\nCollaboration Graph')

    # Dual Stream Merge at Y = 24.5
    merge_y = 24.5
    ax.plot([23, 23], [29.25, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([67, 67], [29.25, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    ax.plot([23, 67], [merge_y, merge_y], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, cx, merge_y, cx, 19.3)

    # 6. Export Geographical & Network Data
    draw_box(ax, cx, 15.5, 44, 7.5, 'Export Country Statistics &\nCollaboration Edge Data (CSV)')
    draw_arrow(ax, cx, 11.75, cx, 7.3)

    # 7. Finish
    draw_oval(ax, cx, 4.5, 18, 5.5, 'Finish')

    save_transparent(fig, "03_country_analysis_workflow.png")


# ==============================================================================
# 4. DATASET UPLOAD & QUALITY MANAGEMENT WORKFLOW (Two-Gate Validation Pipeline)
# ==============================================================================
def make_dataset_workflow():
    fig, ax = plt.subplots(figsize=(7.6, 11.0), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 135)
    ax.axis('off')

    cx = 42.0
    loop_x = 84.0

    # 1. Start
    draw_oval(ax, cx, 129, 18, 5.5, 'Start')
    draw_arrow(ax, cx, 126.25, cx, 121.8)

    # 2. Select Local CSV
    draw_box(ax, cx, 118, 40, 7.5, 'Initiate Dataset Upload Modal\n& Select Local CSV File')
    draw_arrow(ax, cx, 114.25, cx, 108.8)

    # 3. Gate 1: Valid CSV & Encoding?
    draw_diamond(ax, cx, 103, 30, 9.5, 'Valid CSV &\nEncoding?')

    # No branch -> reject and reselect
    ax.plot([cx + 15, loop_x, loop_x], [103, 103, 118], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, loop_x, 118, cx + 20, 118)
    ax.text(cx + 16.5, 104.8, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom')

    # Yes branch -> inspect schema
    draw_arrow(ax, cx, 98.25, cx, 93.3)
    ax.text(cx + 2.0, 95.8, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 4. Inspect Header Schema
    draw_box(ax, cx, 89.5, 42, 7.5, 'Inspect Header Schema &\nMap Canonical Columns')
    draw_arrow(ax, cx, 85.75, cx, 80.3)

    # 5. Gate 2: Core Fields Present?
    draw_diamond(ax, cx, 74.5, 30, 9.5, 'Core Fields\nPresent?')

    # Branch No -> Auto-map aliases side box (X = 80)
    draw_arrow(ax, cx + 15, 74.5, 68.0, 74.5)
    ax.text(cx + 16.5, 76.3, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom')
    draw_box(ax, 81.0, 74.5, 24, 7.5, 'Auto-Map Aliases &\nFill Missing Defaults', font_size=8.5)
    
    # Path from Auto-Map box down and left to main pipeline
    ax.plot([81.0, 81.0, cx], [70.75, 63.5, 63.5], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, 81.0, 63.5, cx, 63.5)

    # Branch Yes -> directly proceed to Step 6
    draw_arrow(ax, cx, 69.75, cx, 58.3)
    ax.text(cx - 3.5, 66.5, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 6. Compute Data Quality & Deduplicate
    draw_box(ax, cx, 54.5, 44, 7.5, 'Detect Duplicate Rows &\nCalculate Completeness Score %')
    draw_arrow(ax, cx, 50.75, cx, 46.8)

    # 7. Present Quality Report Modal
    draw_box(ax, cx, 43, 44, 7.5, 'Present Dataset Quality Report\nwith Metrics & Warning Badges')
    draw_arrow(ax, cx, 39.25, cx, 35.3)

    # 8. User Confirms Ingestion
    draw_box(ax, cx, 31.5, 44, 7.5, 'User Confirms Ingestion &\nSaves to System Repository')
    draw_arrow(ax, cx, 27.75, cx, 23.8)

    # 9. Sync Across Modules
    draw_box(ax, cx, 20, 44, 7.5, 'Synchronize Active Corpus across\nSearch, Analytics, & AI Chat')
    draw_arrow(ax, cx, 16.25, cx, 11.8)

    # 10. Finish
    draw_oval(ax, cx, 9, 18, 5.5, 'Finish')

    save_transparent(fig, "04_dataset_analysis_workflow.png")


# ==============================================================================
# 5. AI RESEARCH CHAT WORKFLOW (Conversational RAG Loop with Index Bootstrap)
# ==============================================================================
def make_chat_workflow():
    fig, ax = plt.subplots(figsize=(8.2, 11.5), dpi=300)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 135)
    ax.axis('off')

    cx = 46.0
    chat_loop_x = 12.0

    # 1. Start
    draw_oval(ax, cx, 129, 18, 5.5, 'Start')
    draw_arrow(ax, cx, 126.25, cx, 121.8)

    # 2. Open Chat & Select Corpus
    draw_box(ax, cx, 118, 42, 7.5, 'Open AI Research Chat &\nSelect Target Literature Corpus')
    draw_arrow(ax, cx, 114.25, cx, 108.8)

    # 3. Decision 1: FAISS Index Exists?
    draw_diamond(ax, cx, 103, 30, 9.5, 'FAISS Index\nExists?')

    # Branch No -> Chunk & Generate Embeddings side box (X = 81)
    draw_arrow(ax, cx + 15, 103, 69.0, 103)
    ax.text(cx + 16.5, 104.8, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom')
    draw_box(ax, 81.0, 103, 24, 7.5, 'Chunk Texts & Build\nFAISS Vector Index', font_size=8.5)
    
    # Path from Index Box down and left to Question Box
    ax.plot([81.0, 81.0, cx], [99.25, 91.5, 91.5], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, 81.0, 91.5, cx, 91.5)

    # Branch Yes -> proceed to question input
    draw_arrow(ax, cx, 98.25, cx, 86.8)
    ax.text(cx - 3.5, 94.0, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 4. User Enters Research Question (Return target for follow-up loop)
    draw_box(ax, cx, 83, 42, 7.5, 'User Enters Research Question\ninto Chat Interface')
    draw_arrow(ax, cx, 79.25, cx, 74.8)

    # 5. Query FAISS & Retrieve Chunks
    draw_box(ax, cx, 71, 44, 7.5, 'Query FAISS Vector Store &\nRetrieve Top Semantic Chunks')
    draw_arrow(ax, cx, 67.25, cx, 62.8)

    # 6. Assemble Grounded Context & Synthesize
    draw_box(ax, cx, 59, 44, 7.5, 'Assemble Grounded Context &\nSynthesize AI Answer via LLM')
    draw_arrow(ax, cx, 55.25, cx, 50.8)

    # 7. Render Answer with Interactive Citations
    draw_box(ax, cx, 47, 44, 7.5, 'Display Markdown Response with\nClickable DOI / Author Citations')
    draw_arrow(ax, cx, 43.25, cx, 38.8)

    # 8. User Verifies Source Papers
    draw_box(ax, cx, 35, 44, 7.5, 'Click Citation Pill to Inspect\nSource Abstract & Paper Details')
    draw_arrow(ax, cx, 31.25, cx, 26.0)

    # 9. Decision 2: Follow-up Question?
    draw_diamond(ax, cx, 20.5, 30, 9.5, 'Follow-up\nQuestion?')

    # Branch Yes -> Loop back to Question Box (X = chat_loop_x)
    ax.plot([cx - 15, chat_loop_x, chat_loop_x], [20.5, 20.5, 83], color=c_edge, linewidth=1.1, zorder=4)
    draw_arrow(ax, chat_loop_x, 83, cx - 21, 83)
    ax.text(cx - 16.5, 22.2, 'Yes', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='bottom', ha='right')

    # Branch No -> Finish
    draw_arrow(ax, cx, 15.75, cx, 10.3)
    ax.text(cx + 2.5, 13.0, 'No', fontsize=9.5, fontfamily='Times New Roman', color=c_text, va='center')

    # 10. Finish
    draw_oval(ax, cx, 7.5, 18, 5.5, 'Finish')

    save_transparent(fig, "ai_research_chat_workflow.png")


if __name__ == '__main__':
    print("=" * 70)
    print("GENERATING 5 DISTINCT AUTHENTIC WORKFLOW FLOWCHARTS")
    print("=" * 70)
    make_search_workflow()
    make_bibliometric_workflow()
    make_country_workflow()
    make_dataset_workflow()
    make_chat_workflow()
    print("=" * 70)
    print("ALL 5 DISTINCT DIAGRAMS GENERATED SUCCESSFULLY")
    print("=" * 70)
