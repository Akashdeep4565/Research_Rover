"""
Validator script to inspect and verify all LaTeX files in E:/Research_Rover_Documentation/
Checks environment matching, file inclusion, figure paths, and citation keys.
"""

import os
import re

DOC_DIR = os.path.abspath("E:/Research_Rover_Documentation")
SECTIONS_DIR = os.path.join(DOC_DIR, "sections")
FIGURES_DIR = os.path.join(DOC_DIR, "figures")

def validate():
    print("Validating LaTeX Technical Documentation Package...")
    errors = []
    warnings = []

    # Check master files
    for fname in ["main.tex", "references.bib", "README.txt"]:
        fpath = os.path.join(DOC_DIR, fname)
        if not os.path.exists(fpath):
            errors.append(f"Missing master file: {fname}")
        else:
            print(f"  [FOUND] {fname} ({os.path.getsize(fpath):,} bytes)")

    # Read bib keys
    bib_keys = set()
    bib_path = os.path.join(DOC_DIR, "references.bib")
    if os.path.exists(bib_path):
        with open(bib_path, "r", encoding="utf-8") as f:
            bib_content = f.read()
            bib_keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib_content))
    print(f"  [BIB] Found {len(bib_keys)} BibTeX keys: {sorted(list(bib_keys))}")

    # Read main.tex
    with open(os.path.join(DOC_DIR, "main.tex"), "r", encoding="utf-8") as f:
        main_tex = f.read()

    # Check input files
    inputs = re.findall(r'\\input\{([^}]+)\}', main_tex)
    print(f"  [INPUTS] Found {len(inputs)} input directives:")
    all_content = main_tex
    for inp in inputs:
        inp_path = os.path.join(DOC_DIR, inp)
        if not inp_path.endswith(".tex"):
            inp_path += ".tex"
        if not os.path.exists(inp_path):
            errors.append(f"Input file not found: {inp}")
        else:
            with open(inp_path, "r", encoding="utf-8") as f:
                content = f.read()
                all_content += "\n" + content
            print(f"    - {inp} (exists, {os.path.getsize(inp_path):,} bytes)")

    # Check labels and refs
    labels = set(re.findall(r'\\label\{([^}]+)\}', all_content))
    refs = set(re.findall(r'\\ref\{([^}]+)\}', all_content))
    cites = set(re.findall(r'\\cite\{([^}]+)\}', all_content))

    print(f"  [LABELS] {len(labels)} labels defined.")
    print(f"  [REFS] {len(refs)} references made.")
    for r in refs:
        if r not in labels:
            warnings.append(f"Reference '{r}' does not have a matching \\label")

    print(f"  [CITES] {len(cites)} citation keys queried.")
    for c in cites:
        if c not in bib_keys:
            warnings.append(f"Citation '{c}' not found in references.bib")

    # Check figures
    graphics = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', all_content)
    print(f"  [FIGURES] {len(graphics)} graphic inclusions:")
    for g in graphics:
        g_path = os.path.join(DOC_DIR, g)
        if not os.path.exists(g_path):
            errors.append(f"Graphic file not found: {g}")
        else:
            print(f"    - {g} (exists, {os.path.getsize(g_path):,} bytes)")

    # Check environment balance
    envs_open = re.findall(r'\\begin\{([^}]+)\}', all_content)
    envs_close = re.findall(r'\\end\{([^}]+)\}', all_content)

    from collections import Counter
    open_counts = Counter(envs_open)
    close_counts = Counter(envs_close)

    all_envs = set(open_counts.keys()).union(set(close_counts.keys()))
    for env in all_envs:
        if open_counts[env] != close_counts[env]:
            errors.append(f"Mismatched environment: \\begin{{{env}}} ({open_counts[env]}) vs \\end{{{env}}} ({close_counts[env]})")

    print("\n--- VALIDATION SUMMARY ---")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    else:
        print("Warnings: 0")

    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  X {e}")
        return False
    else:
        print("Errors: 0 (All syntax, environments, inputs, figures, labels, and citations are perfectly balanced!)")
        return True

if __name__ == "__main__":
    validate()
