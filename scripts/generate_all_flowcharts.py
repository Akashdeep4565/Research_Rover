"""
Master Orchestration Script to Generate All Seven Architectural Flowcharts and Documentation.
Target: M.Tech Data Science project report, mid-semester presentation, and viva examination.
"""

import os
import sys
import shutil
from pathlib import Path

# Ensure script directory is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT))

# Set matplotlib cache to temp before importing matplotlib
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Users/AkashDeep/AppData/Local/Temp")

import matplotlib
matplotlib.use('Agg')

from diagram_definitions import (
    layer_01,
    layer_02,
    layer_03,
    layer_04,
    layer_05,
    layer_06,
    layer_07,
    system_overview
)

DIAGRAM_MODULES = [
    ("layer_01_user_interaction", layer_01),
    ("layer_02_frontend_api", layer_02),
    ("layer_03_backend_controllers", layer_03),
    ("layer_04_data_collection", layer_04),
    ("layer_05_data_cleaning", layer_05),
    ("layer_06_analysis_computation", layer_06),
    ("layer_07_visualization_output", layer_07),
    ("system_architecture_overview", system_overview),
]

def main():
    print("=" * 80)
    print("RESEARCH ROVER: GENERATING SEVEN ARCHITECTURAL FLOWCHARTS")
    print("=" * 80)

    docs_dir = REPO_ROOT / "docs" / "architecture_flowcharts"
    docs_dir.mkdir(parents=True, exist_ok=True)

    for stem, mod in DIAGRAM_MODULES:
        print(f"\nProcessing [{stem}]...")
        
        # 1. Mermaid Source (.mmd)
        mmd_content = mod.get_mermaid()
        mmd_path = docs_dir / f"{stem}.mmd"
        mmd_path.write_text(mmd_content, encoding="utf-8")
        print(f"  [OK] Wrote Mermaid: {mmd_path.name}")

        # 2. Standalone Scalable SVG (.svg)
        svg_content = mod.get_svg()
        svg_path = docs_dir / f"{stem}.svg"
        svg_path.write_text(svg_content, encoding="utf-8")
        print(f"  [OK] Wrote SVG:     {svg_path.name}")

        # 3. High-Resolution PNG (300 DPI) (.png)
        png_path = docs_dir / f"{stem}.png"
        mod.render_matplotlib(str(png_path))
        print(f"  [OK] Rendered PNG:  {png_path.name}")

    print("\n" + "=" * 80)
    print("ALL 8 DIAGRAM ARTIFACTS GENERATED SUCCESSFULLY (.mmd, .svg, .png)!")
    print("=" * 80)

if __name__ == "__main__":
    main()
