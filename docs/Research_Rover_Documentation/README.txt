RESEARCH ROVER - TECHNICAL DOCUMENTATION PACKAGE
=================================================

Document Title: Research Rover: Installation, Configuration and Technical Documentation
Author: Akashdeep Singha (M.Tech in Data Science)
Department: Computer Science and Engineering, Tezpur University
Version: 1.0
Date: 17 November 2026

DIRECTORY STRUCTURE:
-------------------
Research_Rover_Documentation/
│
├── main.tex                       # Master LaTeX document file
├── references.bib                 # BibTeX bibliography database
├── README.txt                     # Documentation compilation instructions
│
├── sections/                      # Modular LaTeX section files
│   ├── introduction.tex           # Section 1: Introduction
│   ├── requirements.tex           # Section 2: System Requirements
│   ├── installation.tex           # Sections 3, 4, 5: Download, Backend & Frontend Setup
│   ├── execution.tex              # Section 6: Two-Terminal Execution Guide
│   ├── architecture.tex           # Section 7: Overall System Architecture
│   ├── modules.tex                # Section 8: Main Application Modules
│   ├── data_ingestion.tex         # Section 9: Universal Dataset Ingestion System
│   ├── api_reference.tex          # Section 10: Complete FastAPI Route Specifications
│   ├── troubleshooting.tex        # Section 11: Troubleshooting & Diagnostic Solutions
│   ├── directory_structure.tex    # Section 12: Project Tree & Folder Responsibilities
│   └── conclusion.tex             # Section 13: Conclusion & Future Extensions
│
└── figures/                       # Vector PDF diagrams (Strictly Monochrome)
    ├── system_architecture.pdf       # Figure 1: Overall System Architecture
    ├── data_ingestion_workflow.pdf   # Figure 2: Universal Ingestion Workflow
    ├── backend_architecture.pdf      # Figure 3: Backend Internal Architecture
    ├── installation_workflow.pdf     # Figure 4: Installation & Setup Workflow
    └── feature_readiness_workflow.pdf# Figure 5: Feature Readiness Decision Logic

HOW TO COMPILE THE LATEX DOCUMENTATION:
--------------------------------------
Prerequisites: A standard LaTeX distribution such as TeX Live, MiKTeX, or MacTeX.

Step 1: Open a terminal in this directory:
    cd E:\Research_Rover_Documentation

Step 2: Run pdflatex and bibtex to resolve all citations, table of contents, and figure references:
    pdflatex main.tex
    bibtex main
    pdflatex main.tex
    pdflatex main.tex

Step 3: Open the generated "main.pdf" in your preferred PDF viewer.

Alternatively, compile using latexmk:
    latexmk -pdf main.tex

DOCUMENT DESIGN AND TYPOGRAPHY:
------------------------------
- Strict monochrome / black-and-white presentation (no colored headings, boxes, or links).
- 12 pt body text with 1.5 line spacing.
- Standard 1.0 inch margins.
- Formal academic documentation structure.
