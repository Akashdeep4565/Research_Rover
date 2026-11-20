"""
scripts/execute_cleanup.py
Executes Phase 6A (Deletion of Category D temporary & duplicate files)
and Phase 6B (Reorganization of Category B & C files into docs/ and scripts/).

All actions are logged and verified.
"""

import os
import shutil
from pathlib import Path

REPO_ROOT = Path("e:/Research_Rover").resolve()

def log(msg):
    print(f"[CLEANUP] {msg}")

def safe_remove_file(rel_path):
    p = REPO_ROOT / rel_path
    if p.exists() and p.is_file():
        try:
            sz = p.stat().st_size
            p.unlink()
            log(f"Deleted file: {rel_path} ({sz} bytes)")
            return sz
        except Exception as e:
            log(f"ERROR deleting {rel_path}: {e}")
    else:
        log(f"File already absent or not a file: {rel_path}")
    return 0

def safe_remove_dir(rel_path):
    p = REPO_ROOT / rel_path
    if p.exists() and p.is_dir():
        try:
            shutil.rmtree(p)
            log(f"Deleted directory: {rel_path}")
            return True
        except Exception as e:
            log(f"ERROR deleting dir {rel_path}: {e}")
    else:
        log(f"Directory already absent: {rel_path}")
    return False

def safe_move_file(src_rel, dst_rel):
    src = REPO_ROOT / src_rel
    dst = REPO_ROOT / dst_rel
    if src.exists() and src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        log(f"Moved: {src_rel} -> {dst_rel}")
        return True
    else:
        log(f"Cannot move (source absent): {src_rel}")
        return False

def clean_pycache_and_pytest():
    log("Scanning and cleaning __pycache__ and .pytest_cache...")
    deleted_pyc = 0
    EXCLUDED = {'.git', 'node_modules', '.venv', 'venv'}
    
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT, topdown=False):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED]
        p = Path(dirpath)
        if p.name == '__pycache__':
            for f in filenames:
                try:
                    (p / f).unlink()
                    deleted_pyc += 1
                except Exception:
                    pass
            try:
                p.rmdir()
            except Exception:
                pass
        elif '.pytest_cache' in p.parts:
            for f in filenames:
                try:
                    (p / f).unlink()
                except Exception:
                    pass
            try:
                p.rmdir()
            except Exception:
                pass
    log(f"Cleaned {deleted_pyc} .pyc files and associated cache directories.")

def run_phase_6a():
    log("=" * 60)
    log("STARTING PHASE 6A: Deletion of Category D (Safe to Remove) Files")
    log("=" * 60)
    
    # 1. Stale frontend build directory
    safe_remove_dir("frontend/dist")
    
    # 2. Browser Crashpad telemetry
    safe_remove_dir("docs/uml/edge_profile")
    
    # 3. Dead / 0-byte / abandoned stubs
    safe_remove_file("backend/features/search_pubmed.py")
    safe_remove_file("generate_seven_layer_flowcharts.py")
    safe_remove_file("scripts/generate_all_extracted_diagrams.py")
    safe_remove_file("scripts/generate_extracted_seven_layers.py")
    
    # 4. Duplicate datasets
    safe_remove_file("data/screen_time_2001-2026.csv.backup")
    safe_remove_file("data/screen_time_2001-2026(ResearchRover Downloaded)_analysis_keyword_presence_matrix.csv")
    safe_remove_file("data/smart_healthcare (1).csv")
    safe_remove_file("data/speaker_identification_and_verification_i.csv")
    safe_remove_file("data/empty_affiliations_test.csv")
    safe_remove_file("data/screen_time_2001-2026_analysis_keyword_frequency_analysis_keyword_frequency.csv")
    safe_remove_file("data/openalex-group-by-20261004(1)_analysis_keyword_frequency.csv")
    
    # 5. Redundant use_case_diagram aliases in docs/uml/
    for ext in ["pdf", "png", "puml", "svg", "dot", "mmd"]:
        safe_remove_file(f"docs/uml/use_case_diagram.{ext}")
        safe_remove_file(f"frontend/public/assets/uml/use_case_diagram.{ext}")
        
    # 6. Truncate / clean unrotated runtime logs
    backend_log = REPO_ROOT / "backend/logs/research_rover.log"
    if backend_log.exists():
        with open(backend_log, "w", encoding="utf-8") as f:
            f.write("")
        log("Truncated backend/logs/research_rover.log to 0 bytes.")
    safe_remove_file("logs/research_rover.log")
    
    # 7. Clean pycache and pytest caches
    clean_pycache_and_pytest()
    
    log("Phase 6A completed successfully.")

def run_phase_6b():
    log("=" * 60)
    log("STARTING PHASE 6B: Directory Reorganization (Categories B & C)")
    log("=" * 60)
    
    # 1. Delete redundant copies from root that already exist in docs/ or assets/
    safe_remove_file("COMPONENT_SOURCE_MAPPING.md")
    safe_remove_file("RESEARCH_ROVER_SEVEN_LAYER_ARCHITECTURE_REPORT.md")
    
    # Root Use Case diagram copies (already in docs/uml/ and frontend/public/assets/uml/)
    for ext in ["pdf", "png", "puml", "svg"]:
        safe_remove_file(f"Research_Rover_Use_Case_Diagram.{ext}")
        safe_remove_file(f"Research_Rover_Simple_User_Use_Case_Diagram.{ext}")
        
    # Root architecture overview copies (already in docs/architecture_flowcharts/ and frontend/public/assets/)
    safe_remove_file("system_architecture_overview.mmd")
    safe_remove_file("system_architecture_overview.svg")
    
    # 2. Relocate academic & architectural documentation from root to docs/
    safe_move_file("ARCHITECTURE.md", "docs/architecture/ARCHITECTURE.md")
    safe_move_file("RESEARCH_ROVER_SYSTEM_ARCHITECTURE.md", "docs/architecture/RESEARCH_ROVER_SYSTEM_ARCHITECTURE.md")
    safe_move_file("FEATURES_2026-05-29.md", "docs/FEATURES_2026-05-29.md")
    safe_move_file("Research_Rover_Analysis_Phases_Documentation.md", "docs/Research_Rover_Analysis_Phases_Documentation.md")
    safe_move_file("Research_Rover_New_Changes_Documentation.md", "docs/Research_Rover_New_Changes_Documentation.md")
    safe_move_file("RESEARCH_ROVER_USER_JOURNEY.md", "docs/RESEARCH_ROVER_USER_JOURNEY.md")
    
    # 3. Relocate root utility scripts into scripts/
    safe_move_file("generate_use_case_all_formats.py", "scripts/generate_use_case_all_formats.py")
    safe_move_file("render_simple_use_case_diagram.py", "scripts/render_simple_use_case_diagram.py")
    
    log("Phase 6B completed successfully.")

def update_gitignore():
    log("Hardening .gitignore...")
    gi_path = REPO_ROOT / ".gitignore"
    
    content = """# Environment & secrets
secrets.txt
.env
.env.*

# Dependencies
frontend/node_modules/
backend/.venv/
venv/

# Python compiled bytecode & caches
**/__pycache__/
*.pyc
*.pyo
.pytest_cache/
backend/.pytest_cache/

# Frontend build outputs
frontend/dist/

# Logs & telemetry
logs/
*.log
backend/logs/
**/edge_profile/

# Temporary & backup datasets
*.backup
*.tmp
"""
    gi_path.write_text(content.strip() + "\n", encoding="utf-8")
    log("Updated .gitignore with comprehensive ignore rules.")

def fix_generate_all_flowcharts():
    log("Updating scripts/generate_all_flowcharts.py to prevent root dumping...")
    p = REPO_ROOT / "scripts/generate_all_flowcharts.py"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        # Comment out copying to REPO_ROOT
        text = text.replace("shutil.copy2(mmd_path, REPO_ROOT / f\"{stem}.mmd\")", "# shutil.copy2(mmd_path, REPO_ROOT / f\"{stem}.mmd\")")
        text = text.replace("shutil.copy2(svg_path, REPO_ROOT / f\"{stem}.svg\")", "# shutil.copy2(svg_path, REPO_ROOT / f\"{stem}.svg\")")
        text = text.replace("shutil.copy2(png_path, REPO_ROOT / f\"{stem}.png\")", "# shutil.copy2(png_path, REPO_ROOT / f\"{stem}.png\")")
        p.write_text(text, encoding="utf-8")
        log("scripts/generate_all_flowcharts.py updated successfully.")

if __name__ == "__main__":
    run_phase_6a()
    run_phase_6b()
    update_gitignore()
    fix_generate_all_flowcharts()
    log("=" * 60)
    log("CLEANUP PROCESS COMPLETE!")
    log("=" * 60)
