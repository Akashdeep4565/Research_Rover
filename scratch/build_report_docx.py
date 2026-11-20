"""
Master Script: Generate Academic Technical Progress Report for Research Rover.
Universal Dataset Ingestion System.
Generates: Research_Rover_Universal_Data_Ingestion_Technical_Report.docx
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Add scratch to path for docx_helpers
sys.path.insert(0, os.path.abspath("scratch"))
import docx_helpers as dh

OUTPUT_DOCX = os.path.abspath("Research_Rover_Universal_Data_Ingestion_Technical_Report.docx")
FIGURES_DIR = os.path.abspath("reports/figures")

def create_report():
    print(f"Creating formal academic progress report: {OUTPUT_DOCX}...")
    doc = docx.Document()

    # Configure Margins (Standard Academic 1.0 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Base Typography Settings
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Configure Running Header and Page Number Footer
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    header = section.header
    p_h = header.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_h = p_h.add_run("M.Tech Technical Progress Report — Dept. of CSE, Tezpur University")
    r_h.font.name = "Times New Roman"
    r_h.font.size = Pt(8.5)
    r_h.font.italic = True
    r_h.font.color.rgb = RGBColor(148, 163, 184)

    footer = section.footer
    p_f = footer.paragraphs[0]
    p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_f = p_f.add_run("Research Rover: Universal Dataset Ingestion System  |  Page ")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(9)
    r_f.font.color.rgb = RGBColor(100, 116, 139)
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    p_f._p.append(fld)

    # ---------------------------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(36)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run("TEZPUR UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nNAPAAM, TEZPUR, ASSAM – 784028, INDIA")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(20, 43, 101)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(28)
    r_div = p_div.add_run("____________________________________________________")
    r_div.font.color.rgb = RGBColor(19, 140, 140)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(12)
    p_proj.paragraph_format.space_after = Pt(12)
    r_proj = p_proj.add_run("RESEARCH ROVER\nAn Intelligent Research Discovery and Bibliometric Analysis Platform")
    r_proj.font.name = "Times New Roman"
    r_proj.font.size = Pt(16)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(30, 58, 138)

    p_rep_title = doc.add_paragraph()
    p_rep_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep_title.paragraph_format.space_before = Pt(24)
    p_rep_title.paragraph_format.space_after = Pt(12)
    r_rep_title = p_rep_title.add_run("TECHNICAL PROGRESS REPORT\nON THE DEVELOPMENT AND INTEGRATION OF THE\nUNIVERSAL DATASET INGESTION SYSTEM")
    r_rep_title.font.name = "Times New Roman"
    r_rep_title.font.size = Pt(20)
    r_rep_title.font.bold = True
    r_rep_title.font.color.rgb = RGBColor(20, 43, 101)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(48)
    r_sub = p_sub.add_run("A Canonical Multi-Schema Normalization, Multi-Attribute Quality Assessment,\nand Feature Compatibility Layer for Academic Publication Ingestion")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(36)
    p_subm.paragraph_format.space_after = Pt(6)
    r_subm = p_subm.add_run("A Technical Report Submitted in Partial Fulfilment of the Requirements for the Degree of\nMASTER OF TECHNOLOGY IN DATA SCIENCE")
    r_subm.font.name = "Times New Roman"
    r_subm.font.size = Pt(12)
    r_subm.font.bold = True
    r_subm.font.color.rgb = RGBColor(30, 41, 59)

    # Metadata Grid
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(32)
    p_meta.paragraph_format.space_after = Pt(0)
    r_meta = p_meta.add_run(
        "Prepared By:\n"
        "AKASHDEEP SINGHA\n"
        "Programme: M.Tech in Data Science\n"
        "Department of Computer Science and Engineering\n"
        "Tezpur University\n\n"
        "Submission Date: 17 November 2026"
    )
    r_meta.font.name = "Times New Roman"
    r_meta.font.size = Pt(12)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(20, 43, 101)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # TABLE OF CONTENTS / OUTLINE OVERVIEW
    # ---------------------------------------------------------------------------
    p_toc_title = doc.add_paragraph()
    p_toc_title.paragraph_format.space_before = Pt(12)
    p_toc_title.paragraph_format.space_after = Pt(16)
    r_toc = p_toc_title.add_run("TABLE OF CONTENTS")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = RGBColor(20, 43, 101)

    toc_items = [
        ("Chapter 1: Introduction", "1"),
        ("    1.1 Context and Background of Research Rover", "1"),
        ("    1.2 The Role of Dataset Ingestion in Scientific Analytics", "2"),
        ("    1.3 Motivation for a Universal Ingestion System", "2"),
        ("Chapter 2: Existing System and Identified Limitations", "3"),
        ("    2.1 The Pre-existing Research Rover Ingestion Architecture", "3"),
        ("    2.2 Inconsistent Column Naming Across Research Databases", "4"),
        ("    2.3 Silent Data Loss and Dropped Metadata Fields", "5"),
        ("    2.4 Duplicate Records Contamination", "5"),
        ("    2.5 Total Lack of Dataset Quality and Hygiene Metrics", "6"),
        ("    2.6 Opaque Feature Compatibility and Runtime Failures", "6"),
        ("Chapter 3: Proposed Universal Dataset Ingestion System", "7"),
        ("    3.1 Design Principles and Architectural Objectives", "7"),
        ("    3.2 Canonical Representation Schema (20 Core Fields)", "8"),
        ("    3.3 Multi-Source Database Compatibility Scope", "10"),
        ("Chapter 4: System Architecture and Workflow", "11"),
        ("    4.1 High-Level Multi-Tier System Architecture", "11"),
        ("    4.2 End-to-End Ingestion and Normalization Sequence Workflow", "13"),
        ("    4.3 Architectural Paradigm Comparison: Pre-existing vs. Universal System", "15"),
        ("Chapter 5: Major Newly Implemented Components", "17"),
        ("    5.1 Canonical Dataset Normalizer (dataset_normalizer.py)", "17"),
        ("    5.2 Dataset Quality Assessment Engine (dataset_quality.py)", "20"),
        ("    5.3 Seven-Feature Readiness Evaluation Engine", "23"),
        ("    5.4 Canonical Data Loader and Unified Dispatch (canonical_loader.py)", "26"),
        ("Chapter 6: Backend Integration and Service Refactoring", "28"),
        ("    6.1 Extended Upload API (POST /api/v1/files/upload)", "28"),
        ("    6.2 Dedicated Quality Endpoint (GET /api/v1/files/{filename}/quality)", "29"),
        ("    6.3 Refactoring of Consuming Research Services", "30"),
        ("    6.4 Non-Automatic Embeddings Policy and Decoupled Processing", "31"),
        ("Chapter 7: Frontend Integration", "33"),
        ("    7.1 Dataset Quality Modal Component (DatasetQualityModal.tsx)", "33"),
        ("    7.2 Dataset Feature Readiness Banner (DatasetFeatureReadinessBanner.tsx)", "35"),
        ("    7.3 User Workflow Integration and Quality State Synchronization", "36"),
        ("    7.4 Visual Verification of Frontend Execution", "37"),
        ("Chapter 8: Testing, Quality Assurance and Verification", "39"),
        ("    8.1 Backend Regression Test Suite (57 Verified Tests)", "39"),
        ("    8.2 Frontend Production Build and Type Verification", "41"),
        ("    8.3 Phase 4.3 Live Browser Smoke Test Empirical Results", "42"),
        ("Chapter 9: Limitations and Future Work", "45"),
        ("    9.1 Evaluation Boundary and Large-Scale Benchmarking", "45"),
        ("    9.2 User-Confirmed Mapping Correction and Persistence", "45"),
        ("    9.3 FAISS Index-to-Dataset Staleness Validation", "46"),
        ("    9.4 Expansion to Additional Bibliographic File Formats", "46"),
        ("Chapter 10: Conclusion", "47"),
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False
    dh.set_table_borders(toc_table, color="FFFFFF") # Invisible borders for clean TOC look

    for i, (item, pg) in enumerate(toc_items):
        c0 = toc_table.cell(i, 0)
        c1 = toc_table.cell(i, 1)
        c0.width = Inches(5.5)
        c1.width = Inches(1.0)
        dh.set_cell_margins(c0, top=40, bottom=40, left=0, right=0)
        dh.set_cell_margins(c1, top=40, bottom=40, left=0, right=0)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(item)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(10.5)
        if item.startswith("Chapter"):
            r0.font.bold = True
            r0.font.color.rgb = RGBColor(20, 43, 101)
        else:
            r0.font.color.rgb = RGBColor(51, 65, 85)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(pg)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        if item.startswith("Chapter"):
            r1.font.bold = True

    doc.add_page_break()

    # Helper function for adding structured chapters
    def add_chapter_heading(number: int, title: str):
        p = doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"CHAPTER {number}: {title.upper()}")
        run.font.name = "Times New Roman"
        run.font.size = Pt(17)
        run.font.bold = True
        run.font.color.rgb = RGBColor(20, 43, 101)

    def add_section_heading(sec_num: str, title: str):
        p = doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"{sec_num} {title}")
        run.font.name = "Times New Roman"
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)

    def add_sub_heading(sub_num: str, title: str):
        p = doc.add_paragraph(style='Heading 3')
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(f"{sub_num} {title}")
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(15, 118, 110)

    # ---------------------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------------------------
    add_chapter_heading(1, "Introduction")

    add_section_heading("1.1", "Context and Background of Research Rover")
    doc.add_paragraph(
        "Modern academic inquiry requires researchers and data scientists to navigate massive volumes of scientific publications, "
        "synthesize multi-disciplinary literature, and detect collaborative and thematic trends. To address these demands, "
        "the Research Rover platform was developed as an intelligent research discovery, bibliometric analytics, and AI-assisted "
        "synthesis platform. Built upon an asynchronous Python 3.11+ / FastAPI backend and a responsive React 18 / Vite / TypeScript "
        "single-page architecture, Research Rover integrates live biomedical literature retrieval via the NCBI E-utilities (PubMed) API, "
        "tabular bibliographic data extraction, dense vector embeddings using Sentence Transformers (all-mpnet-base-v2), hierarchical "
        "density-based spatial clustering (HDBSCAN), similarity search indexing with FAISS, and context-grounded conversational synthesis "
        "powered by Google Gemini with strict numerical citation provenance [n]."
    )
    doc.add_paragraph(
        "Within Research Rover, the user workflow operates across three primary stages: first, discovering and retrieving relevant publications "
        "based on research keywords or importing external datasets; second, computing macro-level bibliometric analytics including keyword "
        "frequencies, presence-absence matrices, NetworkX graph centralities, and international geographic co-authorship distributions; "
        "and third, conducting micro-level semantic exploration through a Retrieval-Augmented Generation (RAG) conversational assistant."
    )

    add_section_heading("1.2", "The Role of Dataset Ingestion in Scientific Analytics")
    doc.add_paragraph(
        "In any data-driven bibliometric and retrieval-augmented platform, the reliability and mathematical validity of downstream "
        "computations are strictly governed by the quality of the ingested metadata. Statistical keyword presence matrices, NetworkX "
        "degree and betweenness centralities, co-authorship collaboration networks, and dense vector embeddings depend fundamentally "
        "on consistent, well-formed input records. If author affiliation strings are missing or placed in an unmapped column, "
        "geographic collaboration graphs fail to render. If publication years are invalid or formatted as full date strings, longitudinal "
        "trend lines break. If duplicate papers are ingested unnoticed, keyword frequencies and centrality scores are artificially inflated, "
        "leading to erroneous scientific conclusions."
    )
    doc.add_paragraph(
        "Consequently, the data ingestion pipeline is not merely a file upload transport mechanism; it represents the primary quality gateway "
        "and hygiene foundation for the entire research discovery system."
    )

    add_section_heading("1.3", "Motivation for a Universal Ingestion System")
    doc.add_paragraph(
        "While Research Rover's initial search capabilities supported direct PubMed queries, academic researchers frequently maintain "
        "existing literature collections exported from external scientific citation indexes, including Scopus, Clarivate Web of Science, "
        "OpenAlex, and bespoke institutional CSV repositories. In the pre-existing system, importing an external CSV was exceedingly fragile. "
        "The system expected an exact, hardcoded column schema matching internal PubMed naming conventions. When an investigator uploaded a "
        "Scopus CSV containing headers such as 'Document Title' and 'Author Keywords', or a Web of Science export containing 'Article Title' "
        "and 'Addresses', the application failed to recognize the fields, leading to silent data loss, dropped metadata, or catastrophic "
        "runtime exceptions during downstream analysis."
    )
    doc.add_paragraph(
        "To eliminate this critical friction, the Universal Dataset Ingestion System was conceptualized, designed, and integrated. "
        "The primary motivation of this project phase is to establish a robust, non-destructive, canonical normalization layer that automatically "
        "maps heterogeneous research CSV exports into a standardized 20-field representation, evaluates dataset completeness and hygiene "
        "through an objective 0–100 quality scoring formula, safely identifies and isolates duplicate records, and provides transparent, "
        "pre-flight feature readiness indicators to guide researchers before analytical execution."
    )

    dh.add_callout_box(
        doc,
        "The Universal Dataset Ingestion System is an architectural extension built upon the existing Research Rover platform. "
        "It preserves all pre-existing search, analysis, embedding, and chat services while establishing an enterprise-grade data hygiene "
        "and multi-schema normalization layer.",
        title="PROJECT SCOPE CLARIFICATION"
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 2: EXISTING SYSTEM AND IDENTIFIED LIMITATIONS
    # ---------------------------------------------------------------------------
    add_chapter_heading(2, "Existing System and Identified Limitations")

    add_section_heading("2.1", "The Pre-existing Research Rover Ingestion Architecture")
    doc.add_paragraph(
        "In the pre-existing Research Rover implementation, dataset ingestion was handled by a rudimentary upload handler within "
        "backend/app/api/routes/files.py. When a user uploaded a CSV file via the frontend interface, the backend executed a simple file "
        "write to the storage folder (data/) and subsequently invoked a basic pandas DataFrame load using pd.read_csv(). The uploaded dataset "
        "was immediately registered in the file listing without any inspection, schema validation, or structural normalization."
    )
    doc.add_paragraph(
        "Downstream services—specifically AnalysisService, CountryService, and EmbeddingService—directly read the stored CSV file using "
        "hardcoded column name assumptions. For instance, the analysis service explicitly queried df['Keywords'], the country extraction "
        "pipeline queried df['Affiliations'], the search service queried df['Title'], and the embedding pipeline queried df['DOI'] and "
        "df['Abstract']. If these exact column names were not present, the services defaulted to empty structures or crashed with KeyError exceptions."
    )

    add_section_heading("2.2", "Inconsistent Column Naming Across Research Databases")
    doc.add_paragraph(
        "A rigorous empirical audit of bibliographic exports across major academic search repositories revealed substantial structural "
        "heterogeneity. Even though these databases describe the identical scientific reality (a paper with authors, an abstract, a publication "
        "year, and a journal source), their export formatting conventions diverge dramatically:"
    )

    # Bullet points on schemas
    p_b1 = doc.add_paragraph(style='List Bullet')
    p_b1.add_run("Paper Title Variations: ").bold = True
    p_b1.add_run("PubMed outputs 'Title'; Scopus outputs 'Document Title'; Web of Science outputs 'Article Title' or abbreviated 'TI'; OpenAlex outputs 'title' or 'display_name'; custom repositories frequently use 'Item Title', 'Paper_Title', or 'name'.")

    p_b2 = doc.add_paragraph(style='List Bullet')
    p_b2.add_run("Keywords & Subject Terms: ").bold = True
    p_b2.add_run("PubMed provides 'Keywords' and 'MeSH_Terms'; Scopus segregates 'Author Keywords' and 'Index Keywords'; Web of Science outputs 'Author Keywords' and 'KeyWords Plus' or 'ID'; OpenAlex produces 'concepts'; custom spreadsheets often label this 'Subject' or 'Tags'.")

    p_b3 = doc.add_paragraph(style='List Bullet')
    p_b3.add_run("Author Affiliations & Geography: ").bold = True
    p_b3.add_run("PubMed outputs 'Affiliations'; Scopus uses 'Affiliations'; Web of Science exports 'Addresses' or 'C1'; OpenAlex provides nested structures such as 'authorships.institutions'; other datasets utilize 'Country', 'Organization', or 'Institution'.")

    p_b4 = doc.add_paragraph(style='List Bullet')
    p_b4.add_run("Chronological Temporal Fields: ").bold = True
    p_b4.add_run("Datasets alternate between 'Publication Year', 'Year_Published', 'Year', 'PY', 'Date', and full ISO timestamps ('Publication Date', 'Cover Date').")

    p_b5 = doc.add_paragraph(style='List Bullet')
    p_b5.add_run("Persistent Unique Identifiers: ").bold = True
    p_b5.add_run("Identifiers alternate between 'DOI', 'Doi', 'doi', 'PMID', 'PubMed ID', 'UT', 'EID', and 'openalex_id'.")

    add_section_heading("2.3", "Silent Data Loss and Dropped Metadata Fields")
    doc.add_paragraph(
        "Because the pre-existing system lacked an alias mapping dictionary or fuzzy matching logic, any CSV whose headers deviated by even a "
        "single character or casing variation suffered silent data loss. For example, if a dataset contained 'Doi' instead of 'DOI', the embedding "
        "pipeline failed to locate the persistent identifier, falling back to synthetic paper numbers and breaking external URL resolution. "
        "Furthermore, custom columns containing supplementary metadata (such as citation counts, funding acknowledgments, or license URLs) were "
        "completely unrecorded, with no sidecar metadata tracking which columns were understood and which were discarded."
    )

    add_section_heading("2.4", "Duplicate Records Contamination")
    doc.add_paragraph(
        "A critical vulnerability identified in the previous system was the absence of duplicate record detection. Researchers frequently "
        "merge query results or upload combined datasets containing overlapping articles. In the pre-existing workflow, identical papers were "
        "treated as distinct records. This caused three severe distortions:"
    )
    p_d1 = doc.add_paragraph(style='List Bullet')
    p_d1.add_run("Keyword Frequency Skewing: ").bold = True
    p_d1.add_run("Keywords appearing in duplicate papers were counted multiple times, distorting Pareto distributions and word cloud visual weights.")
    p_d2 = doc.add_paragraph(style='List Bullet')
    p_d2.add_run("Network Centrality Inflation: ").bold = True
    p_d2.add_run("In the co-occurrence network, artificial duplicate clique edges were formed, distorting NetworkX degree, betweenness, and eigenvector centralities.")
    p_d3 = doc.add_paragraph(style='List Bullet')
    p_d3.add_run("Vector Database Waste: ").bold = True
    p_d3.add_run("In the embedding pipeline, duplicate abstracts were tokenized, embedded via Sentence Transformers, and indexed into FAISS, wasting vector storage and causing redundant search results.")

    add_section_heading("2.5", "Total Lack of Dataset Quality and Hygiene Metrics")
    doc.add_paragraph(
        "Prior to this integration, Research Rover had zero dataset quality assessment capabilities. A user could upload an empty CSV, a corrupted "
        "file with 95% missing abstracts, or a dataset with invalid publication years (such as negative numbers or non-numeric strings), and the "
        "API returned a successful HTTP 200 response. There was no objective metric to quantify dataset completeness, no data hygiene scoring, "
        "and no feedback advising the researcher on how to improve the dataset."
    )

    add_section_heading("2.6", "Opaque Feature Compatibility and Runtime Failures")
    doc.add_paragraph(
        "Finally, the pre-existing system provided no indication of feature readiness. After uploading a file, users navigated to the Analytics "
        "or Chat pages without knowing whether the dataset possessed the required attributes. If the dataset lacked affiliations, the country "
        "analysis page displayed an empty world map without explanation. If the user attempted to chat with a dataset whose FAISS vector index "
        "had not been generated, the system fell back to ungrounded LLM responses. This opacity created substantial user confusion and undermined "
        "the perceived reliability of the platform."
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 3: PROPOSED UNIVERSAL DATASET INGESTION SYSTEM
    # ---------------------------------------------------------------------------
    add_chapter_heading(3, "Proposed Universal Dataset Ingestion System")

    add_section_heading("3.1", "Design Principles and Architectural Objectives")
    doc.add_paragraph(
        "To resolve the aforementioned limitations, the Universal Dataset Ingestion System was designed and integrated into Research Rover. "
        "The architecture adheres to six foundational engineering principles:"
    )
    p_p1 = doc.add_paragraph(style='List Bullet')
    p_p1.add_run("Non-Destructive Ingestion: ").bold = True
    p_p1.add_run("The original uploaded CSV file must never be overwritten, modified, or truncated. It is preserved byte-for-byte in the data/ directory, ensuring an immutable audit trail.")
    p_p2 = doc.add_paragraph(style='List Bullet')
    p_p2.add_run("Canonical Normalization: ").bold = True
    p_p2.add_run("A standardized 20-field internal representation is established to decouple internal analytical services from external vendor export conventions.")
    p_p3 = doc.add_paragraph(style='List Bullet')
    p_p3.add_run("Multi-Tier Intelligent Matching: ").bold = True
    p_p3.add_run("Header mapping employs a four-stage cascade: exact canonical matching, comprehensive alias dictionary lookup, normalized token comparison, and high-confidence Levenshtein fuzzy matching.")
    p_p4 = doc.add_paragraph(style='List Bullet')
    p_p4.add_run("Objective Mathematical Quality Scoring: ").bold = True
    p_p4.add_run("A 0–100 composite quality scoring formula evaluates field-by-field completeness, duplicate penalties, invalid value deductions, and small-sample damping factors.")
    p_p5 = doc.add_paragraph(style='List Bullet')
    p_p5.add_run("Dual-Mode Downstream Consumption: ").bold = True
    p_p5.add_run("Consuming services are empowered to request deduplicated records (for statistical analytics, graph modeling, and vector indexing) or complete record sets (for cataloguing and audit display).")
    p_p6 = doc.add_paragraph(style='List Bullet')
    p_p6.add_run("Pre-flight Feature Readiness: ").bold = True
    p_p6.add_run("All seven Research Rover analytical features are evaluated pre-flight, dynamically overlaying runtime FAISS vector index availability to guarantee transparent user feedback.")

    add_section_heading("3.2", "Canonical Representation Schema (20 Core Fields)")
    doc.add_paragraph(
        "At the core of the ingestion architecture is the CanonicalPaperRecord data model, implemented in backend/app/services/dataset_normalizer.py. "
        "The schema defines exactly 20 canonical fields, providing structured typed attributes while preserving unmapped source columns in a raw_data dictionary:"
    )

    # Table 3.1: Canonical Schema Table
    dh.add_table_caption(doc, "Table 3.1: Complete 20-Field Canonical Paper Schema and Source Alias Mappings")
    schema_cols = [
        ("Field Name", 1.4),
        ("Data Type", 1.0),
        ("Primary Purpose", 2.2),
        ("Recognized Aliases (PubMed, Scopus, WoS, OpenAlex)", 1.9)
    ]
    
    schema_data = [
        ("title", "str", "Primary paper title used for display, indexing, and deduplication", "Document Title, Article Title, TI, title, display_name, Paper_Title"),
        ("abstract", "str", "Text abstract for semantic chunking, FAISS vectors, and NLP", "Abstract, Abstract Note, AB, abstract, description, Summary"),
        ("authors", "List[str]", "Normalized list of individual author names", "Authors, Author Names, AU, authorships.author.display_name, Creators"),
        ("affiliations", "List[str]", "Author institutions, universities, departments, addresses", "Affiliations, Addresses, C1, AD, authorships.institutions, Institution"),
        ("countries", "List[str]", "Pre-extracted ISO-3/standard country names from affiliations", "Country, Countries, Affiliation_Country, Nation, Geographic_Location"),
        ("keywords", "List[str]", "Author and indexed topical keywords for frequency & graphs", "Keywords, Author Keywords, Index Keywords, KeyWords Plus, concepts, DE, ID"),
        ("publication_year", "int", "Validated 4-digit Gregorian calendar publication year", "Publication Year, Year_Published, Year, PY, publication_year, Date_Year"),
        ("publication_date", "date / str", "Exact publication date if available (YYYY-MM-DD)", "Publication Date, Date, PD, publication_date, cover_date, Issue_Date"),
        ("journal", "str", "Journal name, book title, conference proceedings, or venue", "Source, Journal/Book, SO, Journal, Source title, host_venue.display_name"),
        ("doi", "str", "Digital Object Identifier (sanitized, lowercase, un-prefixed)", "DOI, Doi, doi, Digital Object Identifier, persistent_identifier"),
        ("pmid", "str", "NCBI PubMed Unique Identifier (digits only)", "PMID, pmid, PubMed ID, Medline_ID, Entrez_ID"),
        ("pmcid", "str", "PubMed Central full-text open access identifier (PMC...)", "PMCID, pmcid, PMC ID, PubMedCentral_ID"),
        ("openalex_id", "str", "OpenAlex global entity URI / identifier (W...)", "openalex_id, OpenAlex ID, openalex, OpenAlex_URI"),
        ("citation_count", "int", "Total citations received by the paper across databases", "Citation Count, Times Cited, TC, cited_by_count, Cited_References"),
        ("publication_type", "str", "Article classification (Journal, Review, Conference, Letter)", "Publication Type, Document Type, DT, type, genre, Item_Type"),
        ("url", "str", "Primary landing page or publisher article link", "URL, Link, Article_URL, Landing_Page, host_venue.url"),
        ("download_url", "str", "Direct open-access PDF download link or repository URL", "Download_URL, PDF_URL, FullText_URL, open_access.oa_url"),
        ("is_open_access", "bool", "Boolean indicator of open-access availability", "Is_Open_Access, Open Access, OA, is_oa, open_access_status"),
        ("paper_id", "str", "Deterministic record hash or unique dataset-scoped identifier", "id, ID, paper_id, Article_ID, Unique_ID"),
        ("raw_data", "Dict[str, Any]", "Complete key-value store of all unmapped original columns", "Internal non-destructive preservation dictionary (zero data loss)")
    ]

    schema_table = doc.add_table(rows=len(schema_data)+1, cols=4)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    schema_table.autofit = False
    dh.set_table_borders(schema_table)

    for c_idx, (hdr_text, w) in enumerate(schema_cols):
        dh.style_header_cell(schema_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(schema_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "142B65" if c_idx == 0 else "0F172A"
            dh.style_body_cell(schema_table.cell(r_idx+1, c_idx), val, schema_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    add_section_heading("3.3", "Multi-Source Database Compatibility Scope")
    doc.add_paragraph(
        "The canonical alias dictionary in CANONICAL_ALIASES maps headers across four premier scholarly databases: NCBI PubMed, "
        "Elsevier Scopus, Clarivate Web of Science (WoS), and OurResearch OpenAlex. In addition, generic alias tokens accommodate "
        "common variations found in Mendeley, Zotero, Google Scholar Harvester, and user-compiled spreadsheets."
    )
    doc.add_paragraph(
        "It is essential to clarify that broad compatibility is the foundational design objective of this system. While the normalizer "
        "successfully parses standard exports from these sources, exhaustive empirical validation across every historical CSV dialect, "
        "custom RIS-to-CSV converters, and localized institutional repositories remains an ongoing research milestone."
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 4: SYSTEM ARCHITECTURE AND WORKFLOW
    # ---------------------------------------------------------------------------
    add_chapter_heading(4, "System Architecture and Workflow")

    add_section_heading("4.1", "High-Level Multi-Tier System Architecture")
    doc.add_paragraph(
        "The Universal Dataset Ingestion System is structured as a cohesive, five-tier pipeline bridging frontend interaction and backend "
        "computational services. Figure 4.1 illustrates the structural relationship between the components:"
    )

    # Insert Figure 4.1
    fig1_path = os.path.join(FIGURES_DIR, "figure_1_system_architecture.png")
    if os.path.exists(fig1_path):
        dh.add_figure_with_caption(doc, fig1_path, "Figure 4.1: High-Level Architecture of the Universal Dataset Ingestion & Quality System", width_inches=6.2)

    doc.add_paragraph(
        "As depicted in Figure 4.1, the architecture establishes strict encapsulation between stages:"
    )
    p_a1 = doc.add_paragraph(style='List Bullet')
    p_a1.add_run("Client Interaction Layer: ").bold = True
    p_a1.add_run("The React/Vite interface manages file selection, displays immediate post-upload quality telemetry via DatasetQualityModal, and maintains persistent state awareness through DatasetFeatureReadinessBanner.")

    p_a2 = doc.add_paragraph(style='List Bullet')
    p_a2.add_run("Ingestion Controller: ").bold = True
    p_a2.add_run("FastAPI routes enforce file-extension filtering, execute streaming size validation (50 MB cap), detect file encodings (UTF-8, Latin-1, CP1252), and store the unmodified CSV stream.")

    p_a3 = doc.add_paragraph(style='List Bullet')
    p_a3.add_run("Core Normalization & Quality Layer: ").bold = True
    p_a3.add_run("DatasetNormalizer transforms heterogeneous DataFrames into CanonicalPaperRecord lists, while DatasetQualityAssessor calculates composite quality scores, letter grades, and 7-feature readiness.")

    p_a4 = doc.add_paragraph(style='List Bullet')
    p_a4.add_run("Unified Storage & Canonical Loader: ").bold = True
    p_a4.add_run("CanonicalDataLoader serializes the NormalizationReport and DatasetQualityReport into a sidecar JSON file (<filename>_canonical_metadata.json), overlays live FAISS vector index status, and provides cached O(1) retrieval.")

    p_a5 = doc.add_paragraph(style='List Bullet')
    p_a5.add_run("Downstream Consuming Services: ").bold = True
    p_a5.add_run("Research services (AnalysisService, CountryService, SearchService, EmbeddingService, ChatService) query the loader with parameterized duplicate exclusion flags, operating entirely on canonical fields.")

    add_section_heading("4.2", "End-to-End Ingestion and Normalization Sequence Workflow")
    doc.add_paragraph(
        "To understand the runtime execution flow, Figure 4.2 presents the sequence workflow executed when a user uploads a dataset:"
    )

    # Insert Figure 4.2
    fig2_path = os.path.join(FIGURES_DIR, "figure_2_ingestion_workflow.png")
    if os.path.exists(fig2_path):
        dh.add_figure_with_caption(doc, fig2_path, "Figure 4.2: End-to-End Dataset Ingestion, Quality Assessment & Downstream Dispatch Workflow", width_inches=6.2)

    doc.add_paragraph(
        "The sequence execution proceeds through eleven distinct, deterministic steps:"
    )
    p_s1 = doc.add_paragraph(style='List Bullet')
    p_s1.add_run("Step 1 (Upload): ").bold = True
    p_s1.add_run("The client initiates an asynchronous multipart/form-data POST request to /api/v1/files/upload.")
    p_s2 = doc.add_paragraph(style='List Bullet')
    p_s2.add_run("Step 2 (Validation): ").bold = True
    p_s2.add_run("The controller validates that the file has a .csv suffix and does not exceed the 50 MB threshold, then writes the exact byte stream to data/<filename>.csv.")
    p_s3 = doc.add_paragraph(style='List Bullet')
    p_s3.add_run("Step 3 (Normalization Trigger): ").bold = True
    p_s3.add_run("The controller loads the DataFrame via multi-encoding fallback and invokes DatasetNormalizer.normalize_dataframe().")
    p_s4 = doc.add_paragraph(style='List Bullet')
    p_s4.add_run("Step 4 (Canonical Normalization): ").bold = True
    p_s4.add_run("Headers are sanitised, matched against alias tables, resolved via Levenshtein fuzzy metrics, cleaned, and deduplicated via multi-pass hashing.")
    p_s5 = doc.add_paragraph(style='List Bullet')
    p_s5.add_run("Step 5 (Quality Assessment Trigger): ").bold = True
    p_s5.add_run("The generated canonical records and NormalizationReport are passed to DatasetQualityAssessor.assess().")
    p_s6 = doc.add_paragraph(style='List Bullet')
    p_s6.add_run("Step 6 (Quality Scoring): ").bold = True
    p_s6.add_run("Field completeness is weighted, duplicate and malformed deductions are subtracted, small-sample damping is applied, and 7-feature readiness is evaluated.")
    p_s7 = doc.add_paragraph(style='List Bullet')
    p_s7.add_run("Step 7 (Persistence): ").bold = True
    p_s7.add_run("CanonicalDataLoader.process_and_save_canonical() caches the metadata sidecar to disk.")
    p_s8 = doc.add_paragraph(style='List Bullet')
    p_s8.add_run("Step 8 (Runtime Overlay): ").bold = True
    p_s8.add_run("The loader checks if a matching FAISS index file exists, dynamically downgrading semantic search and AI chat readiness if unindexed.")
    p_s9 = doc.add_paragraph(style='List Bullet')
    p_s9.add_run("Steps 9–11 (Response & UI Update): ").bold = True
    p_s9.add_run("An ExtendedFileUploadResponse is returned to the client, the uploaded dataset is automatically selected in all dropdowns, and the DatasetQualityModal opens instantly.")

    add_section_heading("4.3", "Architectural Paradigm Comparison: Pre-existing vs. Universal System")
    doc.add_paragraph(
        "Figure 4.3 and Table 4.1 contrast the architectural paradigm of the pre-existing system against the newly integrated Universal Ingestion System:"
    )

    # Insert Figure 4.3
    fig3_path = os.path.join(FIGURES_DIR, "figure_3_before_after_comparison.png")
    if os.path.exists(fig3_path):
        dh.add_figure_with_caption(doc, fig3_path, "Figure 4.3: Architectural Paradigm Comparison: Pre-existing Ingestion vs. Universal Ingestion System", width_inches=6.2)

    # Table 4.1 Comparison Table
    dh.add_table_caption(doc, "Table 4.1: Technical Comparison of Ingestion Capabilities Before and After Integration")
    comp_cols = [
        ("Evaluation Dimension", 1.5),
        ("Pre-existing Ingestion Architecture", 2.5),
        ("Universal Dataset Ingestion System", 2.5)
    ]
    comp_data = [
        ("Source Compatibility", "Restricted strictly to PubMed/Rover CSVs with exact column names.", "Universal mapping across PubMed, Scopus, Web of Science, OpenAlex, and custom CSVs."),
        ("Header Matching", "Rigid case-sensitive equality matching. Single-character mismatch failed.", "Four-stage cascade: exact, alias dictionary, token normalization, Levenshtein fuzzy match (>0.85)."),
        ("Raw Data Preservation", "Unmapped custom columns were discarded during downstream loading.", "Zero data loss. Unmapped columns preserved in raw_data dictionary; conflicting mappings reported."),
        ("Duplicate Detection", "None. Duplicate records were double-counted in frequency and graphs.", "Multi-pass duplicate identification: normalized DOI strip + normalized title alphanumeric hash."),
        ("Data Quality Telemetry", "None. Corrupted or empty datasets accepted with HTTP 200 without warning.", "Objective 0–100 composite score, letter grade (A/B/C/D/F), field completeness, and hygiene warnings."),
        ("Feature Compatibility", "Opaque. Users discovered missing columns only when analysis crashed.", "Pre-flight readiness checks across all 7 analytical features with dynamic FAISS index overlay."),
        ("Downstream Service API", "Services directly executed pd.read_csv() with hardcoded assumptions.", "Centralized CanonicalDataLoader providing load_canonical_dataframe(exclude_duplicates=True/False)."),
        ("User Experience", "Blind upload. No post-upload feedback or validation telemetry.", "Automatic dataset selection, instant modal display, and persistent readiness banner across pages.")
    ]

    comp_table = doc.add_table(rows=len(comp_data)+1, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    dh.set_table_borders(comp_table)

    for c_idx, (hdr_text, w) in enumerate(comp_cols):
        dh.style_header_cell(comp_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(comp_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "142B65" if c_idx == 0 else "0F172A"
            dh.style_body_cell(comp_table.cell(r_idx+1, c_idx), val, comp_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 5: MAJOR NEWLY IMPLEMENTED COMPONENTS
    # ---------------------------------------------------------------------------
    add_chapter_heading(5, "Major Newly Implemented Components")

    add_section_heading("5.1", "Canonical Dataset Normalizer (dataset_normalizer.py)")
    doc.add_paragraph(
        "The Canonical Dataset Normalizer is encapsulated in the DatasetNormalizer class within backend/app/services/dataset_normalizer.py. "
        "It provides deterministic, idempotent normalization of arbitrary tabular DataFrames into canonical schema instances."
    )
    
    add_sub_heading("5.1.1", "Four-Stage Header Matching Cascade")
    doc.add_paragraph(
        "To reliably map diverse column names, the identify_column() method employs a four-stage hierarchical matching cascade:"
    )
    p_m1 = doc.add_paragraph(style='List Bullet')
    p_m1.add_run("Stage 1 — Exact Canonical Match (Confidence: 1.0): ").bold = True
    p_m1.add_run("Direct case-insensitive check against the 20 canonical field names. If the sanitized header exactly matches a canonical field, it is accepted immediately.")

    p_m2 = doc.add_paragraph(style='List Bullet')
    p_m2.add_run("Stage 2 — Alias Dictionary Lookup (Confidence: 0.95): ").bold = True
    p_m2.add_run("Lookup in CANONICAL_ALIASES. Each canonical field maintains an extensive list of known vendor synonyms. For example, 'Document Title', 'Article Title', and 'TI' map directly to 'title'.")

    p_m3 = doc.add_paragraph(style='List Bullet')
    p_m3.add_run("Stage 3 — Normalized Token Comparison (Confidence: 0.90): ").bold = True
    p_m3.add_run("Both header and alias strings are stripped of punctuation, underscores, dashes, and extra whitespace, converting strings to clean alphanumeric tokens (e.g., 'Author_Keywords' becomes 'authorkeywords').")

    p_m4 = doc.add_paragraph(style='List Bullet')
    p_m4.add_run("Stage 4 — Levenshtein Fuzzy Matching (Confidence: 0.85): ").bold = True
    p_m4.add_run("For unmapped columns, difflib.SequenceMatcher calculates similarity ratios against known aliases. A match is accepted only if similarity exceeds 0.85 AND the header length is >= 4 characters to prevent short abbreviations (e.g., 'ID', 'NO') from erroneously fuzzy matching.")

    add_sub_heading("5.1.2", "Conflict Resolution and Non-Destructive Raw Data Preservation")
    doc.add_paragraph(
        "A common hazard in automated normalization is the collision of multiple source columns mapping to the same canonical field "
        "(for example, a dataset containing both 'Title' and 'Article_Title'). The normalizer handles this deterministically:"
    )
    doc.add_paragraph(
        "1. Primary Selection: The column with the highest matching confidence (or first encountered in case of a tie) is designated as primary.\n"
        "2. Conflict Recording: All secondary columns are recorded in NormalizationReport.conflicts and stored in CanonicalPaperRecord.conflicting_values.\n"
        "3. Raw Data Preservation: Regardless of mapping outcome, every original column value for every record is preserved in CanonicalPaperRecord.raw_data. "
        "No data is ever discarded."
    )

    add_sub_heading("5.1.3", "Data Cleaning and Multi-Pass Deduplication Engine")
    doc.add_paragraph(
        "During row-by-row normalization (normalize_row_to_record()), specialized hygiene routines clean extracted values:"
    )
    p_c1 = doc.add_paragraph(style='List Bullet')
    p_c1.add_run("DOI Sanitization: ").bold = True
    p_c1.add_run("Strips URL prefixes ('https://doi.org/', 'http://dx.doi.org/'), removes whitespace, and converts to lowercase.")
    p_c2 = doc.add_paragraph(style='List Bullet')
    p_c2.add_run("Year Extraction: ").bold = True
    p_c2.add_run("Applies regex pattern r'\\b(1[89]\\d\\d|20\\d\\d)\\b' to extract valid 4-digit Gregorian years (1800–2099) from complex strings (e.g., '2024 Oct 15' becomes 2024).")
    p_c3 = doc.add_paragraph(style='List Bullet')
    p_c3.add_run("Author and Keyword Tokenization: ").bold = True
    p_c3.add_run("Splits multi-value delimited strings (separated by semicolons, commas, or pipes) into clean, trimmed lists while filtering empty values.")

    doc.add_paragraph(
        "Deduplication is executed via a deterministic multi-pass algorithm:"
    )
    doc.add_paragraph(
        "• Primary Pass (DOI Matching): If a valid DOI is present, a hash set tracks seen DOIs. Any subsequent record with the identical DOI is flagged as duplicate (is_duplicate: True) and linked to the primary record ID (duplicate_of: primary_id).\n"
        "• Secondary Pass (Title Hash Matching): If DOI is missing or identical, a normalized title key (lowercase, alphanumeric characters only, stripped of stop-punctuation) is matched. If title similarity equals 1.0, the record is flagged as a duplicate."
    )

    add_section_heading("5.2", "Dataset Quality Assessment Engine (dataset_quality.py)")
    doc.add_paragraph(
        "The Dataset Quality Assessment Engine is implemented in backend/app/services/dataset_quality.py within the DatasetQualityAssessor class. "
        "It evaluates the structural integrity, completeness, and hygiene of the normalized dataset, producing an objective score on a 0.0 to 100.0 scale."
    )

    add_sub_heading("5.2.1", "Mathematical Quality Scoring Formula")
    doc.add_paragraph(
        "The overall quality score is calculated according to the following mathematical formulation:"
    )
    doc.add_paragraph(
        "Base Score = 25*(Cov_Title) + 20*(Cov_Abstract) + 15*(Cov_Keywords) + 10*(Cov_Affil) + 10*(Cov_Authors) + 10*(Cov_Year) + 10*(Cov_ID)\n\n"
        "Where Cov_X represents the populated coverage percentage (0.0 to 1.0) of field X across N records. Deductions are subtracted as follows:\n\n"
        "Duplicate Penalty = min(10.0, (duplicate_count / N) * 20.0)\n"
        "Invalid Value Penalty = min(5.0, (total_invalid_cells / (N * field_count)) * 25.0)\n"
        "Net Score = max(0.0, Base Score - Duplicate Penalty - Invalid Value Penalty)\n"
        "Final Quality Score = round(Net Score * min(1.0, N / 5.0), 1)"
    )

    # Table 5.1 Quality Weights Table
    dh.add_table_caption(doc, "Table 5.1: Multi-Attribute Quality Scoring Weights, Penalties, and Damping Factors")
    q_cols = [
        ("Attribute / Component", 1.8),
        ("Weight / Impact", 1.2),
        ("Evaluation Criterion", 2.2),
        ("Rationale in Research Rover", 1.3)
    ]
    q_data = [
        ("Paper Title", "25.0 Points", "Populated, non-empty title string >= 5 chars", "Core identifier; indispensable for search and cited RAG answers."),
        ("Abstract Text", "20.0 Points", "Populated abstract body text >= 20 chars", "Essential for HDBSCAN semantic chunks and vector embeddings."),
        ("Keywords", "15.0 Points", "At least one valid keyword or MeSH term list", "Required for keyword frequency, word clouds, and presence matrices."),
        ("Affiliations / Country", "10.0 Points", "Resolved affiliation string or country code", "Drives 2D/3D country maps and international collaboration graphs."),
        ("Authors List", "10.0 Points", "At least one author name populated", "Required for author co-authorship analytics and publication attribution."),
        ("Publication Year", "10.0 Points", "Valid 4-digit Gregorian year (1800–2099)", "Required for longitudinal publication trends and temporal filtering."),
        ("Persistent Identifier", "10.0 Points", "Presence of valid DOI, PMID, or OpenAlex ID", "Guarantees publication provenance, link-outs, and deduplication."),
        ("Duplicate Deductions", "Up to -10.0 Pts", "Proportional: min(10.0, (Dup / N) * 20.0)", "Penalizes contaminated datasets that distort frequency statistics."),
        ("Invalid Cell Deductions", "Up to -5.0 Pts", "Proportional to malformed cells across fields", "Penalizes corrupt datasets containing unparseable characters."),
        ("Small-Sample Damping", "Scale: min(1.0, N/5)", "Damps datasets with fewer than 5 records", "Prevents a 1-paper dataset from claiming a 100/100 'Excellent' rating.")
    ]

    q_table = doc.add_table(rows=len(q_data)+1, cols=4)
    q_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    q_table.autofit = False
    dh.set_table_borders(q_table)

    for c_idx, (hdr_text, w) in enumerate(q_cols):
        dh.style_header_cell(q_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(q_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "142B65" if c_idx == 0 else "0F172A"
            dh.style_body_cell(q_table.cell(r_idx+1, c_idx), val, q_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    add_sub_heading("5.2.2", "Quality Grades and Actionable Recommendations")
    doc.add_paragraph(
        "Based on the final quality score, datasets are classified into five standard quality tiers:\n"
        "• Excellent (Score 90.0 – 100.0): Highly complete, clean dataset suitable for all analytical features.\n"
        "• Good (Score 80.0 – 89.9): High quality; minor missing fields (such as a few missing abstracts or DOIs).\n"
        "• Fair (Score 70.0 – 79.9): Moderate quality; noticeable gaps in keywords or affiliations; some features partially ready.\n"
        "• Poor (Score 60.0 – 69.9): Substantial metadata deficits; multiple analytical features disabled.\n"
        "• Critical (Score < 60.0): Severely degraded or incomplete data; unmapped columns or widespread missing titles/abstracts."
    )
    doc.add_paragraph(
        "The engine also synthesizes actionable natural-language recommendations (DatasetQualityReport.recommendations), "
        "explicitly instructing the researcher on how to improve the dataset (e.g., 'Add missing abstracts to enable vector embeddings and semantic search')."
    )

    add_section_heading("5.3", "Seven-Feature Readiness Evaluation Engine")
    doc.add_paragraph(
        "Rather than providing a single generic compatibility flag, the evaluate_feature_readiness() method independently inspects "
        "the requirements of each of the seven core analytical features available in Research Rover:"
    )

    # Table 5.2 Feature Readiness Table
    dh.add_table_caption(doc, "Table 5.2: Research Rover Seven-Feature Readiness Criteria, Thresholds, and Status Rules")
    feat_cols = [
        ("Feature Identifier", 1.6),
        ("Target Application Feature", 1.8),
        ("Minimum Prerequisites", 1.5),
        ("Ready Threshold", 1.6)
    ]
    feat_data = [
        ("keyword_analysis", "Keyword Frequency & Word Clouds", "keywords column populated", "Coverage >= 50.0% AND >= 3 unique terms across dataset."),
        ("cooccurrence_analysis", "Keyword Co-occurrence & Centrality", "keywords column populated", ">= 2 papers containing multi-keyword combinations."),
        ("country_analysis", "Country Collaboration & 2D/3D Maps", "affiliations OR countries", "Coverage >= 20.0% of records with resolved country."),
        ("author_analysis", "Author Collaboration & Statistics", "authors column populated", "Coverage >= 30.0% of records with valid author lists."),
        ("trend_analysis", "Longitudinal Publication Trends", "publication_year column", "Coverage >= 30.0% AND >= 2 distinct publication years."),
        ("semantic_search", "FAISS Vector Similarity Search", "title AND abstract columns", "Combined coverage >= 30.0% AND FAISS index file exists."),
        ("ai_chat_rag", "AI Conversational Research Assistant", "title AND abstract columns", "Combined coverage >= 30.0% AND FAISS index file exists.")
    ]

    feat_table = doc.add_table(rows=len(feat_data)+1, cols=4)
    feat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_table.autofit = False
    dh.set_table_borders(feat_table)

    for c_idx, (hdr_text, w) in enumerate(feat_cols):
        dh.style_header_cell(feat_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(feat_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "142B65" if c_idx == 0 else "0F172A"
            dh.style_body_cell(feat_table.cell(r_idx+1, c_idx), val, feat_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    doc.add_paragraph(
        "Each feature is assigned one of three mutually exclusive status classifications:\n"
        "• READY: All required fields are present, populated above readiness thresholds, and runtime prerequisites are met.\n"
        "• PARTIALLY READY: Feature can execute, but outputs will be incomplete or degraded (e.g., single publication year prevents multi-year trend graphing; low keyword coverage skews frequency; or vector index is missing on disk).\n"
        "• NOT READY: Indispensable prerequisite fields are completely absent (e.g., dataset contains zero keywords; co-occurrence graphs cannot be built)."
    )

    dh.add_callout_box(
        doc,
        "Feature readiness is strictly an assessment of available input data and infrastructure prerequisites. "
        "It guarantees that a feature has sufficient metadata to compute without throwing exceptions, but does not constitute "
        "a mathematical guarantee of scientific accuracy or analytical precision.",
        title="ACADEMIC RIGOR PRINCIPLE"
    )

    add_section_heading("5.4", "Canonical Data Loader and Unified Dispatch (canonical_loader.py)")
    doc.add_paragraph(
        "To decouple consuming services from file system details, the CanonicalDataLoader class (backend/app/services/canonical_loader.py) "
        "serves as the single access point for loading and caching normalized research data. Key methods include:"
    )
    p_l1 = doc.add_paragraph(style='List Bullet')
    p_l1.add_run("load_canonical_dataframe(exclude_duplicates=True/False): ").bold = True
    p_l1.add_run("Loads the dataset as a pandas DataFrame. When exclude_duplicates=True, records flagged with is_duplicate: True are filtered out. Downstream analytics (AnalysisService, CountryService, EmbeddingService) default to True to prevent distorted statistics, whereas cataloguing routes use False to display full audit rows.")

    p_l2 = doc.add_paragraph(style='List Bullet')
    p_l2.add_run("apply_index_status_overlay(): ").bold = True
    p_l2.add_run("Inspects disk storage for matching FAISS vector artifacts (<name>_paper_chunks_hdbscan.index). If the vector index is missing, semantic_search and ai_chat_rag are dynamically downgraded from READY to PARTIALLY_READY with explicit warnings: 'Vector index has not been built yet. Generate embeddings to enable vector retrieval.'")

    p_l3 = doc.add_paragraph(style='List Bullet')
    p_l3.add_run("get_quality_report(): ").bold = True
    p_l3.add_run("Provides high-speed O(1) retrieval of the cached quality report from the sidecar JSON file, avoiding redundant re-normalization on repeated API queries.")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 6: BACKEND INTEGRATION AND SERVICE REFACTORING
    # ---------------------------------------------------------------------------
    add_chapter_heading(6, "Backend Integration and Service Refactoring")

    add_section_heading("6.1", "Extended Upload API (POST /api/v1/files/upload)")
    doc.add_paragraph(
        "The primary upload endpoint in backend/app/api/routes/files.py was upgraded to return an ExtendedFileUploadResponse. "
        "Upon receiving a CSV upload, the endpoint saves the original file untouched, triggers canonical normalization, evaluates dataset "
        "quality, writes the canonical metadata sidecar, checks runtime FAISS index availability, and returns comprehensive telemetry:"
    )
    doc.add_paragraph(
        "{\n"
        "  'filename': 'scopus_cancer_study.csv',\n"
        "  'total_records': 100,\n"
        "  'valid_records': 98,\n"
        "  'duplicate_records': 2,\n"
        "  'overall_quality_score': 94.5,\n"
        "  'quality_grade': 'Excellent',\n"
        "  'canonical_fields_detected': ['title', 'abstract', 'authors', 'keywords', 'publication_year', 'doi'],\n"
        "  'unmapped_columns': ['Editor', 'Volume_Issue'],\n"
        "  'feature_readiness': { ... },\n"
        "  'recommendations': [ ... ]\n"
        "}"
    )

    add_section_heading("6.2", "Dedicated Quality Endpoint (GET /api/v1/files/{filename}/quality)")
    doc.add_paragraph(
        "To allow client-side components to inspect dataset quality at any time (e.g., when switching between existing files in a dropdown), "
        "a dedicated REST endpoint was introduced: GET /api/v1/files/{filename}/quality. This endpoint loads the cached sidecar JSON in O(1) "
        "time, checks current FAISS index availability, overlays vector status, and returns the full DatasetQualityReport."
    )

    add_section_heading("6.3", "Refactoring of Consuming Research Services")
    doc.add_paragraph(
        "Existing Research Rover backend services were refactored to consume data through the CanonicalDataLoader:"
    )
    p_r1 = doc.add_paragraph(style='List Bullet')
    p_r1.add_run("AnalysisService (backend/app/services/analysis_service.py): ").bold = True
    p_r1.add_run("Updated to load canonical DataFrames with exclude_duplicates=True. Keyword extraction now reads canonical 'keywords', ensuring clean frequency distributions and uncorrupted NetworkX centralities.")

    p_r2 = doc.add_paragraph(style='List Bullet')
    p_r2.add_run("CountryService (backend/app/services/country_service.py): ").bold = True
    p_r2.add_run("Updated to consume canonical records with exclude_duplicates=True. The service prioritizes pre-extracted canonical 'countries', falling back to regex parsing on canonical 'affiliations'.")

    p_r3 = doc.add_paragraph(style='List Bullet')
    p_r3.add_run("EmbeddingService & Features (backend/features/embedding_and_indexing.py): ").bold = True
    p_r3.add_run("Updated to index deduplicated canonical records, preventing duplicate chunks from consuming FAISS vector index slots.")

    p_r4 = doc.add_paragraph(style='List Bullet')
    p_r4.add_run("SearchService (backend/app/services/search_service.py): ").bold = True
    p_r4.add_run("Preserves the full catalogue of papers (exclude_duplicates=False) for user browsing, injecting is_duplicate badges so users can identify duplicate records.")

    add_section_heading("6.4", "Non-Automatic Embeddings Policy and Decoupled Processing")
    doc.add_paragraph(
        "An important architectural decision is the explicit decoupling of vector embedding generation from dataset upload. "
        "Creating dense vector embeddings via Sentence Transformers and HDBSCAN chunking is a compute-intensive operation taking "
        "several seconds to minutes depending on paper volume. Uploading a CSV must remain instantaneous (sub-second response). "
        "Therefore, upload evaluates data readiness for embeddings without automatically building them. Vector indexing remains an "
        "explicit user-triggered action via POST /api/v1/embeddings/{filename}."
    )

    # Table 6.1 Implementation Inventory Table
    dh.add_table_caption(doc, "Table 6.1: Implementation Inventory of Newly Implemented and Modified Repository Files")
    file_cols = [
        ("File Path", 2.3),
        ("Classification", 1.2),
        ("Architectural Role", 2.0),
        ("Key Modifications / Capabilities", 1.0)
    ]
    file_data = [
        ("backend/app/services/dataset_normalizer.py", "Newly Created", "Canonical Schema Normalizer", "20-field schema, 4-stage matching, hygiene, deduplication"),
        ("backend/app/services/dataset_quality.py", "Newly Created", "Quality & Readiness Assessor", "0–100 score formula, grade mapping, 7-feature evaluator"),
        ("backend/app/services/canonical_loader.py", "Newly Created", "Unified Data Dispatch Layer", "Sidecar metadata caching, duplicate filtering, index overlay"),
        ("backend/app/models/schemas.py", "Modified", "Pydantic API Data Models", "Added ExtendedFileUploadResponse and quality models"),
        ("backend/app/api/routes/files.py", "Modified", "File Ingestion Controllers", "Upgraded /upload and implemented /{filename}/quality"),
        ("backend/app/services/analysis_service.py", "Modified", "Keyword & Network Analytics", "Refactored to consume deduplicated canonical DataFrames"),
        ("backend/app/services/country_service.py", "Modified", "Country & Collaboration Graphs", "Refactored to use canonical affiliations and countries"),
        ("backend/features/embedding_and_indexing.py", "Modified", "FAISS Vector Index Builder", "Refactored to index deduplicated canonical records"),
        ("frontend/src/components/DatasetQualityModal.tsx", "Newly Created", "Interactive Quality UI Modal", "3 Tabs: Overview, Column Mappings, Feature Readiness"),
        ("frontend/src/components/DatasetFeatureReadinessBanner.tsx", "Newly Created", "Inline Status Indicator Pill", "Shows quality grade, score, and feature count across pages"),
        ("frontend/src/types/index.ts", "Modified", "TypeScript Type Definitions", "Added interfaces for quality report and upload response"),
        ("frontend/src/services/api.ts", "Modified", "Axios API Client Wrappers", "Implemented filesApi.getQuality() and updated upload()"),
        ("frontend/src/pages/AnalyticsPage.tsx", "Modified", "Keyword Analytics Page", "Mounted readiness banner and quality inspection modal"),
        ("frontend/src/pages/ChatPage.tsx", "Modified", "Conversational RAG Chat Page", "Mounted readiness banner and quality inspection modal")
    ]

    file_table = doc.add_table(rows=len(file_data)+1, cols=4)
    file_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    file_table.autofit = False
    dh.set_table_borders(file_table)

    for c_idx, (hdr_text, w) in enumerate(file_cols):
        dh.style_header_cell(file_table.cell(0, c_idx), hdr_text, w, font_size=9)

    for r_idx, row in enumerate(file_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "059669" if row[1] == "Newly Created" and c_idx == 1 else ("142B65" if c_idx == 0 else "0F172A")
            dh.style_body_cell(file_table.cell(r_idx+1, c_idx), val, file_cols[c_idx][1], font_size=8.0, is_bold=is_bold, bg_color=bg, text_color=t_color)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 7: FRONTEND INTEGRATION
    # ---------------------------------------------------------------------------
    add_chapter_heading(7, "Frontend Integration")

    add_section_heading("7.1", "Dataset Quality Modal Component (DatasetQualityModal.tsx)")
    doc.add_paragraph(
        "To provide a rich, interactive presentation of ingestion results, the DatasetQualityModal component was implemented in "
        "frontend/src/components/DatasetQualityModal.tsx. The modal utilizes Framer Motion for smooth transitions, Tailwind CSS for "
        "styling, and Heroicons for visual status indicators. It is organized into three distinct tabs:"
    )
    p_t1 = doc.add_paragraph(style='List Bullet')
    p_t1.add_run("Tab 1 — Quality & Hygiene Overview: ").bold = True
    p_t1.add_run("Displays the prominent circular score badge (0–100), the letter grade pill (Excellent, Good, Fair, Poor, Critical), total records, valid records, duplicate counts, field-by-field population percentages, and actionable recommendations.")

    p_t2 = doc.add_paragraph(style='List Bullet')
    p_t2.add_run("Tab 2 — Column Mappings & Schema Alignment: ").bold = True
    p_t2.add_run("Presents a detailed tabular view of every original column uploaded in the CSV, its mapped canonical field, confidence score (e.g. 1.0, 0.95, 0.85), matching methodology (exact, alias, fuzzy), mapping status (mapped, unmapped, uncertain), and any recorded conflicts.")

    p_t3 = doc.add_paragraph(style='List Bullet')
    p_t3.add_run("Tab 3 — Feature Readiness Assessment: ").bold = True
    p_t3.add_run("Details the readiness status of all seven analytical features, displaying green 'Ready' badges, amber 'Partially Ready' warnings, or rose 'Not Ready' indicators, complete with required fields, coverage metrics, and actionable missing-index alerts.")

    add_section_heading("7.2", "Dataset Feature Readiness Banner (DatasetFeatureReadinessBanner.tsx)")
    doc.add_paragraph(
        "While the modal offers deep inspection, researchers also require persistent, ambient awareness of dataset quality while working. "
        "The DatasetFeatureReadinessBanner component (frontend/src/components/DatasetFeatureReadinessBanner.tsx) was created as a compact, "
        "interactive status strip positioned directly beneath the dataset selector on both AnalyticsPage and ChatPage."
    )
    doc.add_paragraph(
        "The banner displays: (1) Quality Shield icon with score and grade, (2) Ready feature count (e.g., '6/7 Features Ready'), "
        "and (3) Warning counters. Clicking anywhere on the banner opens the full DatasetQualityModal."
    )

    add_section_heading("7.3", "User Workflow Integration and Quality State Synchronization")
    doc.add_paragraph(
        "The frontend integration incorporates seamless state synchronization:\n"
        "• Automatic Selection: When a user uploads a new CSV via the upload modal or dropzone, the returned filename is automatically set as the active dataset in SearchContext and AnalyticsContext.\n"
        "• Instant Modal Display: Upon successful upload, the DatasetQualityModal automatically triggers, immediately showing the researcher the quality score and column mappings of their newly uploaded file.\n"
        "• Dataset Switching Synchronization: When an investigator selects a different file from the dataset dropdown on AnalyticsPage or ChatPage, DatasetFeatureReadinessBanner triggers an asynchronous fetch to /api/v1/files/{filename}/quality, updating the score and readiness metrics without page reload."
    )

    add_section_heading("7.4", "Visual Verification of Frontend Execution")
    doc.add_paragraph(
        "Figure 7.1 shows an authentic, unedited screenshot captured during live browser execution of the Research Rover frontend, "
        "illustrating the Dataset Quality Modal and feature readiness indicators:"
    )

    # Insert Figure 7.1 Screenshot
    fig4_path = os.path.join(FIGURES_DIR, "figure_modal_screenshot.png")
    if os.path.exists(fig4_path):
        dh.add_figure_with_caption(doc, fig4_path, "Figure 7.1: Live Application Execution: Dataset Quality Modal & Feature Readiness Verification", width_inches=5.8)

    doc.add_paragraph(
        "As verified in Figure 7.1, the modal successfully renders the quality telemetry, demonstrates active tab switching, "
        "and clearly communicates feature availability to the end user."
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 8: TESTING, QUALITY ASSURANCE AND VERIFICATION
    # ---------------------------------------------------------------------------
    add_chapter_heading(8, "Testing, Quality Assurance and Verification")

    add_section_heading("8.1", "Backend Regression Test Suite (57 Verified Tests)")
    doc.add_paragraph(
        "To verify structural stability, mathematical correctness, and backward compatibility, an exhaustive automated test suite was "
        "implemented across three test files in backend/tests/. All 57 tests passed with zero failures:"
    )

    # Table 8.1 Test Results Table
    dh.add_table_caption(doc, "Table 8.1: Comprehensive Backend Ingestion Test Suite Verification Results")
    test_cols = [
        ("Test Suite File", 2.2),
        ("Focus Area & Scope", 2.4),
        ("Tests", 0.8),
        ("Execution Result", 1.1)
    ]
    test_data = [
        ("test_dataset_normalizer.py", "Header sanitization, alias dictionary resolution, fuzzy Levenshtein bounds, conflicting scalar preservation, DOI sanitization, year regex extraction, multi-pass deduplication.", "18 Tests", "18 PASSED (100%)"),
        ("test_dataset_quality.py", "Weighted quality scoring formula (0–100), duplicate and invalid penalties, small-sample damping factors, letter grade mapping, 7-feature readiness threshold evaluations.", "10 Tests", "10 PASSED (100%)"),
        ("test_dataset_integration.py", "POST /files/upload route handler, multi-source Scopus/WoS/PubMed scenarios, metadata sidecar serialization, O(1) quality retrieval, downstream duplicate filtering, runtime FAISS index overlay.", "29 Tests", "29 PASSED (100%)"),
        ("TOTAL VERIFIED TESTS", "Comprehensive regression and integration test coverage across the ingestion layer.", "57 Tests", "57 PASSED (100%)")
    ]

    test_table = doc.add_table(rows=len(test_data)+1, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_table.autofit = False
    dh.set_table_borders(test_table)

    for c_idx, (hdr_text, w) in enumerate(test_cols):
        dh.style_header_cell(test_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(test_data):
        bg = "F0FDF4" if r_idx == len(test_data)-1 else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, val in enumerate(row):
            is_bold = (r_idx == len(test_data)-1) or (c_idx == 0)
            t_color = "059669" if (c_idx == 3 or r_idx == len(test_data)-1) else ("142B65" if c_idx == 0 else "0F172A")
            dh.style_body_cell(test_table.cell(r_idx+1, c_idx), val, test_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    add_section_heading("8.2", "Frontend Production Build and Type Verification")
    doc.add_paragraph(
        "The frontend integration was subjected to strict TypeScript type-checking and production compilation via the Vite bundler. "
        "Execution of npm run build verified that all 1,945 project modules transformed cleanly with zero type errors, generating optimized "
        "minified distribution bundles in frontend/dist/:"
    )
    doc.add_paragraph(
        "• vite v6.3.5 building for production...\n"
        "• 1,945 modules transformed cleanly.\n"
        "• dist/index.html: 0.92 kB (gzip: 0.49 kB)\n"
        "• dist/assets/index.css: 92.83 kB (gzip: 14.42 kB)\n"
        "• dist/assets/index.js: 962.60 kB (gzip: 288.43 kB)\n"
        "• Build completed successfully in 33.01 seconds."
    )

    add_section_heading("8.3", "Phase 4.3 Live Browser Smoke Test Empirical Results")
    doc.add_paragraph(
        "In Phase 4.3, an end-to-end live browser smoke test was executed against a running FastAPI backend (port 8000) and Vite frontend "
        "(localhost:3000) using a real custom academic CSV dataset (smoke_test_papers.csv). Table 8.2 summarizes the empirical findings:"
    )

    # Table 8.2 Smoke Test Table
    dh.add_table_caption(doc, "Table 8.2: Phase 4.3 Live Browser Smoke Test Empirical Verification Matrix")
    smoke_cols = [
        ("Verification Dimension", 1.8),
        ("Empirically Measured Output", 2.2),
        ("Technical Evaluation & Verification Status", 2.5)
    ]
    smoke_data = [
        ("System Health & Availability", "HTTP 200 OK on /health", "Verified. Backend models initialized and database folder mounted."),
        ("Custom Header Mapping", "Mapped 7 custom headers: 'Item Title', 'Summary', 'Author Names', 'Addresses', 'Keywords List', 'Year Published', 'Digital Object Identifier'", "Verified. Normalizer mapped 100% of custom non-standard headers to canonical fields without manual user intervention."),
        ("Record Counts & Validity", "6 Total Records | 5 Valid Unique Records | 1 Duplicate Record identified", "Verified. Multi-pass hashing accurately isolated the duplicate entry, setting is_duplicate: True and linking duplicate_of."),
        ("Quality Score & Grade", "Overall Quality Score: 81.7 / 100 | Quality Grade: 'Good'", "Verified. Mathematical scoring accurately applied weights, deductions, and small-sample damping factor (6/5 = 1.0)."),
        ("Feature Readiness Display", "All 7 features rendered: Country (Ready), Author (Ready), Trends (Ready), Keywords (Not Ready - no terms), Co-occurrence (Not Ready)", "Verified. Feature readiness accurately reflected input data characteristics without false-positive claims."),
        ("Runtime FAISS Index Warning", "RAG Chat displayed missing vector index warning; downgraded to 'Partially Ready'", "Verified. Runtime overlay accurately prevented false claims of RAG readiness prior to embedding generation."),
        ("Dataset Switching State", "Switching datasets dynamically refreshed quality score and readiness without page reload", "Verified. Zero stale state leakage across file transitions in AnalyticsPage and ChatPage.")
    ]

    smoke_table = doc.add_table(rows=len(smoke_data)+1, cols=3)
    smoke_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    smoke_table.autofit = False
    dh.set_table_borders(smoke_table)

    for c_idx, (hdr_text, w) in enumerate(smoke_cols):
        dh.style_header_cell(smoke_table.cell(0, c_idx), hdr_text, w, font_size=9.5)

    for r_idx, row in enumerate(smoke_data):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            is_bold = (c_idx == 0)
            t_color = "142B65" if c_idx == 0 else "0F172A"
            dh.style_body_cell(smoke_table.cell(r_idx+1, c_idx), val, smoke_cols[c_idx][1], font_size=8.5, is_bold=is_bold, bg_color=bg, text_color=t_color)

    dh.add_callout_box(
        doc,
        "The Phase 4.3 browser smoke test successfully confirmed the functional mechanics of the complete pipeline under real user conditions. "
        "However, because the smoke test operated on a focused 6-record sample, it serves as a functional proof-of-concept rather than an "
        "exhaustive stress test across massive citation datasets.",
        title="EMPIRICAL VALIDATION SCOPE"
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 9: LIMITATIONS AND FUTURE WORK
    # ---------------------------------------------------------------------------
    add_chapter_heading(9, "Limitations and Future Work")

    add_section_heading("9.1", "Evaluation Boundary and Large-Scale Benchmarking")
    doc.add_paragraph(
        "While the system has been verified with 57 automated regression tests and live browser execution, a primary limitation is that "
        "testing has centered on focused unit fixtures and moderate-scale datasets (100 to 1,000 papers). Large-scale benchmarking "
        "evaluating ingestion latency, memory consumption, and fuzzy-matching throughput across datasets with >50,000 papers represents "
        "the immediate next phase of investigation."
    )

    add_section_heading("9.2", "User-Confirmed Mapping Correction and Persistence")
    doc.add_paragraph(
        "In the current implementation, column mappings are determined automatically during upload based on confidence scores. If a dataset "
        "presents ambiguous headers (confidence between 0.80 and 0.85), the column is marked as 'uncertain' in the NormalizationReport. "
        "Planned future work includes introducing an interactive Mapping Correction UI allowing users to manually adjust column assignments "
        "and persist custom schema profiles for recurring institutional exports."
    )

    add_section_heading("9.3", "FAISS Index-to-Dataset Staleness Validation")
    doc.add_paragraph(
        "Currently, CanonicalDataLoader verifies whether a vector index file (*.index) exists on disk. However, if a user re-uploads an "
        "edited CSV under the identical filename, the pre-existing index may become temporally out of sync with the underlying paper rows. "
        "Future enhancements will incorporate cryptographic hashing (SHA-256) or timestamp comparisons between the CSV file and the index "
        "artifact to proactively notify users when an index is stale."
    )

    add_section_heading("9.4", "Expansion to Additional Bibliographic File Formats")
    doc.add_paragraph(
        "At present, the universal normalizer operates on comma-separated and tab-separated tabular data (.csv, .tsv). In future development "
        "cycles, the ingestion layer will be extended to ingest native RIS (Research Information Systems) files, BibTeX (.bib) citation databases, "
        "and direct EndNote XML archives, translating them into CanonicalPaperRecord instances through a unified parser adapter."
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 10: CONCLUSION
    # ---------------------------------------------------------------------------
    add_chapter_heading(10, "Conclusion")

    add_section_heading("10.1", "Summary of Completed Work")
    doc.add_paragraph(
        "This technical report has documented the design, implementation, and empirical verification of the Universal Dataset Ingestion System "
        "developed as a foundational enhancement to the Research Rover academic discovery platform. By introducing a 20-field canonical schema, "
        "a four-stage header matching cascade, non-destructive raw data preservation, multi-pass paper deduplication, a mathematical 0–100 quality "
        "scoring engine, and pre-flight readiness checks across seven analytical features, the platform has eliminated its previous vulnerability "
        "to format fragmentation and silent data loss."
    )
    doc.add_paragraph(
        "Furthermore, by refactoring backend downstream services to consume canonical data through CanonicalDataLoader and deploying an "
        "intuitive, three-tab DatasetQualityModal in the React frontend, researchers are provided with immediate transparency into the health "
        "and analytical potential of their datasets."
    )

    add_section_heading("10.2", "Academic Significance for M.Tech Data Science Project")
    doc.add_paragraph(
        "From an academic and engineering standpoint, this completed phase establishes the essential data preparation and quality assurance "
        "foundation required for high-order bibliometric research. With 57 passing automated tests, a successful 1,945-module production build, "
        "and verified live browser execution, the Universal Dataset Ingestion System elevates Research Rover from a prototype into an extensible, "
        "resilient, and scientifically rigorous research discovery platform."
    )

    # Final signature sign-off block
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(36)
    p_sign.paragraph_format.space_after = Pt(0)
    p_sign.paragraph_format.keep_with_next = True
    r_sign = p_sign.add_run(
        "Report Compiled and Submitted By:\n\n\n"
        "_____________________________________\n"
        "Akashdeep Singha\n"
        "M.Tech in Data Science, Department of CSE\n"
        "Tezpur University, Napaam, Assam"
    )
    r_sign.font.name = "Times New Roman"
    r_sign.font.size = Pt(11)
    r_sign.font.bold = True
    r_sign.font.color.rgb = RGBColor(20, 43, 101)

    # Save Document
    doc.save(OUTPUT_DOCX)
    size_kb = os.path.getsize(OUTPUT_DOCX) / 1024
    print(f"SUCCESS: Report saved to {OUTPUT_DOCX} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    create_report()
