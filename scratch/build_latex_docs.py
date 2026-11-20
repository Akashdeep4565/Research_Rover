"""
Builder script to generate the complete LaTeX technical documentation for Research Rover.
Target: E:/Research_Rover_Documentation/
"""

import os
import sys

BASE_DIR = os.path.abspath("E:/Research_Rover_Documentation")
SECTIONS_DIR = os.path.join(BASE_DIR, "sections")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")

os.makedirs(SECTIONS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# REFERENCES.BIB
# ---------------------------------------------------------------------------
BIB_CONTENT = r"""@article{fastapi2020,
  author = {Ram{\'\i}rez, Sebasti{\'a}n},
  title = {{FastAPI}: Modern, high-performance web framework for {Python}},
  journal = {GitHub repository},
  year = {2020},
  url = {https://github.com/tiangolo/fastapi}
}

@article{reimers2019sentence,
  author = {Reimers, Nils and Gurevych, Iryna},
  title = {Sentence-{BERT}: Sentence Embeddings using Siamese {BERT}-Networks},
  journal = {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing},
  year = {2019},
  pages = {3982--3992}
}

@article{johnson2019billion,
  author = {Johnson, Jeff and Douze, Matthijs and J{\'e}gou, Herv{\'e}},
  title = {Billion-scale similarity search with {GPUs}},
  journal = {IEEE Transactions on Big Data},
  volume = {7},
  number = {3},
  pages = {535--547},
  year = {2019}
}

@article{jin2023medcpt,
  author = {Jin, Qiao and Kim, Won and Chen, Qingyu and Comeau, Donald C. and Lu, Zhiyong},
  title = {{MedCPT}: Contrastive Pre-trained Transformers with Large-scale PubMed Search Logs for Zero-shot Biomedical Information Retrieval},
  journal = {Bioinformatics},
  volume = {39},
  number = {11},
  pages = {btad651},
  year = {2023}
}

@article{sayers2022eutilities,
  author = {Sayers, Eric W. and Beck, Jeff and Bolton, Evan E. and Bourexis, Dennis and Brister, J. Rodney and Federhen, Scott and Lu, Zhiyong and Madden, Thomas L. and Ostell, James and Sharma, Stephen and others},
  title = {Database resources of the {National Center for Biotechnology Information}},
  journal = {Nucleic Acids Research},
  volume = {50},
  number = {D1},
  pages = {D20--D26},
  year = {2022}
}

@article{priem2022openalex,
  author = {Priem, Jason and Piwowar, Heather and Orr, Richard},
  title = {{OpenAlex}: A fully-open index of scholarly works, authors, venues, institutions, and concepts},
  journal = {arXiv preprint arXiv:2205.01833},
  year = {2022}
}
"""

# ---------------------------------------------------------------------------
# MAIN.TEX
# ---------------------------------------------------------------------------
MAIN_TEX_CONTENT = r"""\documentclass[12pt,a4paper]{article}

% --- Typography and Academic Standards ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx} % Times New Roman-like academic typography
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{setspace}
\onehalfspacing
\usepackage{microtype}

% --- Tables, Graphics, and Formatting ---
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{array}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}
\usepackage{amsmath,amssymb}

% --- Code Listings (Strictly Monochrome) ---
\usepackage{listings}
\lstset{
    basicstyle=\ttfamily\footnotesize,
    breaklines=true,
    breakatwhitespace=true,
    frame=single,
    rulecolor=\color{black},
    numbers=left,
    numberstyle=\tiny\ttfamily,
    stepnumber=1,
    numbersep=8pt,
    showstringspaces=false,
    tabsize=2,
    captionpos=b,
    keywordstyle=\bfseries,
    commentstyle=\itshape,
    stringstyle=\ttfamily
}

% --- Hyperlinks (Strictly Monochrome - No Colored Boxes or Links) ---
\usepackage{hyperref}
\hypersetup{
    colorlinks=false,
    hidelinks,
    pdfborder={0 0 0},
    pdftitle={Research Rover: Installation, Configuration and Technical Documentation},
    pdfauthor={Akashdeep Singha},
    pdfsubject={Software Technical Documentation},
    pdfkeywords={Research Rover, Technical Documentation, FastAPI, React, Data Ingestion, Bibliometrics}
}

% --- Page Headers and Footers ---
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\textit{\nouppercase{\rightmark}}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Section depth configuration
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{3}

\begin{document}

% ---------------------------------------------------------------------------
% TITLE PAGE
% ---------------------------------------------------------------------------
\begin{titlepage}
    \begin{center}
        \vspace*{0.5in}
        
        {\Large \textbf{TEZPUR UNIVERSITY}}\\[0.2cm]
        {\large Department of Computer Science and Engineering}\\[0.1cm]
        {\normalsize Napaam, Tezpur, Assam -- 784028, India}\\[1.5cm]
        
        \rule{\linewidth}{1.2pt}\\[0.4cm]
        {\huge \textbf{Research Rover: Installation, Configuration and Technical Documentation}}\\[0.3cm]
        {\large \textbf{An Intelligent Research Discovery, Bibliometric Analysis, and Universal Ingestion Platform}}\\[0.2cm]
        \rule{\linewidth}{1.2pt}\\[2.0cm]
        
        \begin{minipage}{0.85\textwidth}
            \begin{tabular}{ll}
                \textbf{Project Name:} & Research Rover \\
                \textbf{Prepared By:} & Akashdeep Singha \\
                \textbf{Programme:} & M.Tech in Data Science \\
                \textbf{Department:} & Computer Science and Engineering \\
                \textbf{Institution:} & Tezpur University \\
                \textbf{Documentation Version:} & 1.0 \\
                \textbf{Date of Documentation:} & 17 November 2026 \\
                \textbf{Repository URL:} & \url{https://github.com/Akashdeep4565/Research_Rover} \\
            \end{tabular}
        \end{minipage}
        
        \vfill
        
        {\normalsize A Formal Academic Software Engineering Technical Reference\\Prepared for Project Review and Developer Onboarding}
        
        \vspace*{0.5in}
    \end{center}
\end{titlepage}

% ---------------------------------------------------------------------------
% TABLE OF CONTENTS & LISTS
% ---------------------------------------------------------------------------
\newpage
\pagenumbering{roman}
\tableofcontents
\newpage
\listoffigures
\vspace{1cm}
\listoftables
\newpage
\pagenumbering{arabic}
\setcounter{page}{1}

% ---------------------------------------------------------------------------
% SECTIONS
% ---------------------------------------------------------------------------
\input{sections/introduction.tex}
\newpage
\input{sections/requirements.tex}
\newpage
\input{sections/installation.tex}
\newpage
\input{sections/execution.tex}
\newpage
\input{sections/architecture.tex}
\newpage
\input{sections/modules.tex}
\newpage
\input{sections/data_ingestion.tex}
\newpage
\input{sections/api_reference.tex}
\newpage
\input{sections/troubleshooting.tex}
\newpage
\input{sections/directory_structure.tex}
\newpage
\input{sections/conclusion.tex}

% ---------------------------------------------------------------------------
% BIBLIOGRAPHY
% ---------------------------------------------------------------------------
\newpage
\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""

def write_files():
    print(f"Writing master files to {BASE_DIR}...")
    
    with open(os.path.join(BASE_DIR, "main.tex"), "w", encoding="utf-8") as f:
        f.write(MAIN_TEX_CONTENT.strip())
        
    with open(os.path.join(BASE_DIR, "references.bib"), "w", encoding="utf-8") as f:
        f.write(BIB_CONTENT.strip())

    print("Master LaTeX and BibTeX files written successfully.")

if __name__ == "__main__":
    write_files()
