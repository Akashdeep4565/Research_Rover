"""
scripts/layer_helpers.py
Contains SVG and Matplotlib rendering utilities for creating enlarged, standalone diagrams.
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon

BASE_DIR = Path("e:/Research_Rover")
DOCS_DIR = BASE_DIR / "docs" / "architecture_flowcharts"
ASSETS_DIR = BASE_DIR / "frontend" / "public" / "assets" / "architecture_flowcharts"

def save_all_formats(layer_name: str, mmd_content: str, svg_content: str, fig):
    """Saves .mmd, .svg, and .png across all target directories."""
    targets = [BASE_DIR, DOCS_DIR, ASSETS_DIR]
    
    # Save MMD
    for t in targets:
        with open(t / f"{layer_name}.mmd", "w", encoding="utf-8") as f:
            f.write(mmd_content.strip() + "\n")
            
    # Save SVG
    for t in targets:
        with open(t / f"{layer_name}.svg", "w", encoding="utf-8") as f:
            f.write(svg_content.strip() + "\n")
            
    # Save PNG
    png_path_root = BASE_DIR / f"{layer_name}.png"
    fig.savefig(png_path_root, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    
    # Copy PNG to docs and assets
    import shutil
    for t in [DOCS_DIR, ASSETS_DIR]:
        shutil.copy2(png_path_root, t / f"{layer_name}.png")
        
    print(f"Successfully saved {layer_name} in MMD, SVG, and 300-DPI PNG formats!")
