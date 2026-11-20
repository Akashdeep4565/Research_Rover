"""
Script to generate the short 2-page Project Progress Document for Research Rover.
File: Research_Rover_Data_Ingestion_Progress.docx
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

OUTPUT_FILE = os.path.abspath("Research_Rover_Data_Ingestion_Progress.docx")

def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_document():
    doc = docx.Document()

    # Set margins to 0.75 in to cleanly fit into ~2 pages
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Base typography (Times New Roman, 12 pt body text as specified)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(3)

    # Running Footer with Page Numbering
    section = doc.sections[0]
    footer = section.footer
    p_f = footer.paragraphs[0]
    p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_f = p_f.add_run("Research Rover: Universal Data Ingestion & Quality Analysis  |  Akashdeep Singha  |  Page ")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(8.5)
    r_f.font.color.rgb = RGBColor(100, 116, 139)
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    p_f._p.append(fld)

    # ---------------------------------------------------------------------------
    # HEADER / TITLE BLOCK
    # ---------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("Implementation of Universal Data Ingestion and Dataset Quality Analysis in Research Rover")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(20, 43, 101)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("Project Progress Brief — M.Tech in Data Science")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(19, 140, 140)

    # Student & Institutional Metadata Box (Single-row 2-column compact table)
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    set_table_borders(meta_table, color="CBD5E1", sz="6")

    c0 = meta_table.cell(0, 0)
    c1 = meta_table.cell(0, 1)
    c0.width = Inches(3.5)
    c1.width = Inches(3.5)
    set_cell_background(c0, "F8FAFC")
    set_cell_background(c1, "F8FAFC")
    set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
    set_cell_margins(c1, top=60, bottom=60, left=100, right=100)

    p_meta0 = c0.paragraphs[0]
    p_meta0.paragraph_format.space_after = Pt(0)
    p_meta0.paragraph_format.line_spacing = 1.1
    r_m0 = p_meta0.add_run("Prepared by: ")
    r_m0.font.bold = True
    r_m0.font.size = Pt(9.5)
    p_meta0.add_run("Akashdeep Singha\n").font.size = Pt(9.5)
    r_m1 = p_meta0.add_run("Programme: ")
    r_m1.font.bold = True
    r_m1.font.size = Pt(9.5)
    p_meta0.add_run("M.Tech in Data Science").font.size = Pt(9.5)

    p_meta1 = c1.paragraphs[0]
    p_meta1.paragraph_format.space_after = Pt(0)
    p_meta1.paragraph_format.line_spacing = 1.1
    r_m2 = p_meta1.add_run("Department: ")
    r_m2.font.bold = True
    r_m2.font.size = Pt(9.5)
    p_meta1.add_run("Computer Science and Engineering, Tezpur University\n").font.size = Pt(9.5)
    r_m3 = p_meta1.add_run("Date of Submission: ")
    r_m3.font.bold = True
    r_m3.font.size = Pt(9.5)
    p_meta1.add_run("17 November 2026").font.size = Pt(9.5)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(0)

    # ---------------------------------------------------------------------------
    # Helper for Headings
    # ---------------------------------------------------------------------------
    def add_sec_heading(title: str):
        p = doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(20, 43, 101)

    def add_sub_heading(title: str):
        p = doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)

    # ---------------------------------------------------------------------------
    # SECTION 1: PURPOSE OF THE WORK – WHY IT WAS ADDED
    # ---------------------------------------------------------------------------
    add_sec_heading("1. Purpose of the Work — Why It Was Added")
    doc.add_paragraph(
        "The pre-existing Research Rover platform provided research discovery, live PubMed API integration, bibliometric "
        "keyword analytics, country collaboration networks, dense vector embeddings via Sentence Transformers, and AI-assisted "
        "RAG synthesis. However, these analytical and AI features relied upon rigid, pre-configured CSV column naming structures. "
        "In practical academic and data science workflows, bibliographic datasets originate from diverse platforms—such as PubMed, "
        "Scopus, Web of Science, OpenAlex, Semantic Scholar, and arXiv—each employing distinct naming conventions, heterogeneous "
        "metadata fields, missing attributes, and duplicate records."
    )
    doc.add_paragraph(
        "Directly uploading non-standard CSV files previously led to silent data loss, dropped affiliation or abstract columns, "
        "and unexpected runtime failures during downstream processing. To resolve this critical usability and data integrity bottleneck, "
        "I implemented a Universal Dataset Ingestion and Quality Analysis layer that automatically standardizes uploaded bibliographic "
        "records into a canonical format, evaluates comprehensive dataset quality, and deterministically computes feature readiness before "
        "any analytical service is executed."
    )

    # ---------------------------------------------------------------------------
    # SECTION 2: WORK COMPLETED – WHAT I ADDED
    # ---------------------------------------------------------------------------
    add_sec_heading("2. Work Completed — What I Added")

    add_sub_heading("A. Canonical Dataset Normalization (dataset_normalizer.py)")
    doc.add_paragraph(
        "• Standardized 20-Field Schema: Defined a unified representation covering core research metadata (id, title, abstract, "
        "authors, year, doi, pmid, pmcid, journal, publisher, keywords, mesh_terms, affiliations, countries, citation_count, "
        "reference_count, url, pdf_url, source_database, raw_data).\n"
        "• Automatic Column Recognition: Implemented a four-tier cascade combining curated database alias dictionaries, normalized header "
        "transformations (punctuation stripping, case folding), token set containment, and SequenceMatcher fuzzy matching (threshold 0.85).\n"
        "• Conflict Resolution & Raw Preservation: Resolves ambiguous or competing column assignments through hierarchical confidence weighting, "
        "while storing all unmapped columns into a structured raw_data dictionary per record, ensuring complete non-destructive preservation."
    )

    add_sub_heading("B. Dataset Quality Assessment (dataset_quality.py)")
    doc.add_paragraph(
        "• Multi-Attribute Scoring (0–100): Evaluates field completeness across seven weighted dimensions: Title (25%), Abstract (20%), "
        "Keywords (15%), Affiliations/Countries (10%), Authors (10%), Publication Year (10%), and Identifiers (DOI/PMID: 10%).\n"
        "• Record Deduplication & Validation: Flags duplicates via exact DOI normalization and lowercase alphanumeric title hashing; detects "
        "invalid values (malformed years outside 1800–2100, corrupted DOIs, blank titles); applies proportional duplicate and invalid penalties.\n"
        "• Grading & Actionable Recommendations: Assigns categorical quality tiers (Excellent ≥85, Good ≥70, Fair ≥50, Poor <50) with "
        "per-field coverage statistics and specific suggestions for remediation."
    )

    add_sub_heading("C. Feature Readiness Assessment Engine")
    doc.add_paragraph(
        "Implemented deterministic eligibility assessment for all seven Research Rover analytical and AI capabilities:\n"
        "1. Keyword Analysis: Requires ≥30% keyword or title text availability.\n"
        "2. Keyword Co-occurrence Analysis: Requires ≥40% keyword coverage and ≥3 valid papers.\n"
        "3. Country Collaboration Analysis: Requires ≥20% affiliation/country field presence.\n"
        "4. Author Analysis: Requires ≥40% author name completeness.\n"
        "5. Publication Trend Analysis: Requires ≥50% valid publication year availability.\n"
        "6. Semantic Search: Requires ≥30% abstract completeness and an active FAISS index.\n"
        "7. AI Research Assistant (RAG Chat): Requires ≥20% abstract completeness and an active FAISS index.\n"
        "Classifies each capability as Ready, Partially Ready, or Not Ready with clear diagnostic explanations."
    )

    add_sub_heading("D. Backend Integration and Frontend User Interface")
    doc.add_paragraph(
        "• Unified Ingestion Dispatch (canonical_loader.py): Serves as the single integration point between normalized data and downstream "
        "analytics (analysis_service.py, country_service.py, search_service.py), eliminating duplicate CSV reading logic.\n"
        "• REST API Enhancements: Refactored POST /api/v1/files/upload to return ExtendedFileUploadResponse with complete normalization metadata; "
        "added GET /api/v1/files/{filename}/quality for on-demand telemetry retrieval.\n"
        "• Interactive UI Components: Authoring of DatasetQualityModal.tsx (multi-tab modal for overview scores, column mappings, and readiness) "
        "and DatasetFeatureReadinessBanner.tsx, actively mounted across AnalyticsPage and ChatPage."
    )

    # ---------------------------------------------------------------------------
    # SECTION 3: HOW THE NEW SYSTEM WORKS
    # ---------------------------------------------------------------------------
    add_sec_heading("3. How the New System Works")
    doc.add_paragraph(
        "The end-to-end operational workflow follows a disciplined, transparent data pipeline:\n"
        "1. Upload & Encoding Detection: User uploads a CSV; the system validates file format, checks size limits, and detects character encoding (UTF-8/Latin-1).\n"
        "2. Normalization & Deduplication: The normalizer standardizes column headers against the 20 canonical fields, strips HTML/markup, resolves "
        "data types, detects duplicate records, and archives unmapped headers into raw_data.\n"
        "3. Quality & Readiness Assessment: The quality engine calculates coverage metrics, evaluates penalties, and computes feature readiness statuses.\n"
        "4. Sidecar Metadata Persistence: Canonical metadata is saved alongside the original CSV as {filename}_canonical_metadata.json for instant caching.\n"
        "5. Downstream Dispatch: Downstream analytical services consume canonical fields through CanonicalDataLoader.load_canonical_dataframe()."
    )
    doc.add_paragraph(
        "Crucially, the original uploaded CSV file is preserved untouched on disk. Furthermore, generating dense vector embeddings for FAISS semantic search "
        "remains decoupled as an explicit user-initiated process to prevent latency spikes during upload. When a FAISS index is not yet built, "
        "the system dynamically overlays a clear warning and marks Semantic Search and AI RAG Chat as Partially Ready."
    )

    # ---------------------------------------------------------------------------
    # SECTION 4: TESTING AND VERIFICATION
    # ---------------------------------------------------------------------------
    add_sec_heading("4. Testing and Verification")
    doc.add_paragraph(
        "The implementation was thoroughly verified through multi-tier automated test suites, production build validation, and live end-to-end browser smoke testing:"
    )

    # Verification Summary Table
    v_table = doc.add_table(rows=6, cols=3)
    v_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    v_table.autofit = False
    set_table_borders(v_table, color="CBD5E1", sz="4")

    headers = [("Verification Dimension", 2.2), ("Empirical Result", 1.8), ("Status / Validation Scope", 3.0)]
    for col_idx, (h_text, w) in enumerate(headers):
        cell = v_table.cell(0, col_idx)
        cell.width = Inches(w)
        set_cell_background(cell, "142B65")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_rows = [
        ("Backend Unit & Integration Tests", "57 / 57 Passing (100%)", "Normalizer (18), Quality Engine (10), API Integration (29)"),
        ("Frontend Production Build", "1,945 Modules Transformed", "Zero TypeScript or Vite compilation errors in 33.01s"),
        ("Smoke Test Dataset Upload", "6 Records (5 Unique, 1 Dup)", "Verified duplicate DOI/title detection and exclusion"),
        ("Dataset Quality Telemetry", "81.7 / 100 (Grade: Good)", "High title/year coverage, penalised for duplicate & missing abstract"),
        ("Feature Readiness Verification", "5 Ready, 2 Partially Ready", "Correctly flagged missing FAISS index for Semantic Search & RAG Chat"),
    ]

    for row_idx, data in enumerate(test_rows, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = v_table.cell(row_idx, col_idx)
            cell.width = Inches(headers[col_idx][1])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 1:
                r.font.bold = True
                r.font.color.rgb = RGBColor(20, 83, 45) if "Passing" in text or "Good" in text or "Ready" in text else RGBColor(15, 23, 42)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(3)
    p_sp2.paragraph_format.space_after = Pt(0)

    doc.add_paragraph(
        "Live interactive smoke testing confirmed that dataset upload, automatic modal presentation, multi-tab switching, "
        "and dataset selection across AnalyticsPage and ChatPage operate seamlessly without console or runtime exceptions. "
        "Broader empirical benchmarking across large-scale exports (10,000+ papers) from Scopus, Web of Science, and OpenAlex "
        "remains designated for subsequent evaluation phases."
    )

    # ---------------------------------------------------------------------------
    # SECTION 5: OUTCOME
    # ---------------------------------------------------------------------------
    add_sec_heading("5. Outcome and Project Contribution")
    doc.add_paragraph(
        "This completed work establishes a robust, standardized data preparation and quality evaluation layer for the Research Rover platform. "
        "By replacing brittle column dependencies with an intelligent canonical mapping cascade and transparent quality telemetry, "
        "the platform now reliably ingests diverse bibliographic formats while guarding downstream analytics against corrupted or incomplete data. "
        "Researchers are given immediate, actionable insight into dataset completeness, duplicate records, and analytical feature readiness "
        "before initiating computationally intensive bibliometric modeling and AI synthesis."
    )

    doc.save(OUTPUT_FILE)
    print(f"SUCCESS: Short progress document generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_document()
