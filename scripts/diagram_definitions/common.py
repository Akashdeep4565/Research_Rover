"""
Common utilities, styling constants, and rendering primitives for Research Rover flowcharts.
"""

import os
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch

# Layer Color Themes
THEMES = {
    "layer_01": {
        "name": "User Interaction Layer",
        "primary": "#2563EB",       # Royal Blue
        "primary_dark": "#1D4ED8",
        "primary_light": "#EFF6FF",
        "accent": "#0284C7",        # Sky Blue
        "border": "#3B82F6",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#DBEAFE",
        "badge_text": "#1E40AF",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_02": {
        "name": "Frontend / API Client Layer",
        "primary": "#4F46E5",       # Indigo
        "primary_dark": "#4338CA",
        "primary_light": "#EEF2FF",
        "accent": "#7C3AED",        # Violet
        "border": "#6366F1",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#E0E7FF",
        "badge_text": "#3730A3",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_03": {
        "name": "Backend Processing & Controller Layer",
        "primary": "#9333EA",       # Purple
        "primary_dark": "#7E22CE",
        "primary_light": "#FAF5FF",
        "accent": "#C026D3",        # Fuchsia
        "border": "#A855F7",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#F3E8FF",
        "badge_text": "#6B21A8",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_04": {
        "name": "Data Collection & External Sources",
        "primary": "#0891B2",       # Cyan
        "primary_dark": "#0E7490",
        "primary_light": "#ECFEFF",
        "accent": "#0D9488",        # Teal
        "border": "#06B6D4",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#CFFAFE",
        "badge_text": "#155E75",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_05": {
        "name": "Data Cleaning & Enrichment Layer",
        "primary": "#059669",       # Emerald
        "primary_dark": "#047857",
        "primary_light": "#ECFDF5",
        "accent": "#16A34A",        # Green
        "border": "#10B981",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#D1FAE5",
        "badge_text": "#065F46",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_06": {
        "name": "Analysis & Computation Layer",
        "primary": "#D97706",       # Amber
        "primary_dark": "#B45309",
        "primary_light": "#FFFBEB",
        "accent": "#EA580C",        # Orange
        "border": "#F59E0B",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#FEF3C7",
        "badge_text": "#92400E",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "layer_07": {
        "name": "Visualization & Output Layer",
        "primary": "#E11D48",       # Rose
        "primary_dark": "#BE123C",
        "primary_light": "#FFF1F2",
        "accent": "#DB2777",        # Pink
        "border": "#F43F5E",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#FFE4E6",
        "badge_text": "#9F1239",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    },
    "overview": {
        "name": "Complete System Architecture",
        "primary": "#1E293B",       # Slate
        "primary_dark": "#0F172A",
        "primary_light": "#F8FAFC",
        "accent": "#2563EB",
        "border": "#475569",
        "text": "#0F172A",
        "subtext": "#475569",
        "badge_bg": "#E2E8F0",
        "badge_text": "#1E293B",
        "decision_fill": "#FEF3C7",
        "decision_stroke": "#D97706",
        "decision_text": "#78350F",
        "storage_fill": "#F1F5F9",
        "storage_stroke": "#64748B",
        "output_fill": "#ECFDF5",
        "output_stroke": "#10B981",
        "output_text": "#064E3B",
    }
}

def get_svg_header(width, height, title, subtitle, layer_badge, theme_key="layer_01"):
    theme = THEMES[theme_key]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background:#ffffff; font-family:'Segoe UI', Inter, -apple-system, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.10"/>
    </filter>
    <filter id="shadow-sm" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-opacity="0.08"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="{theme['primary']}" />
    </marker>
    <marker id="arrow-dash" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#64748b" />
    </marker>
    <marker id="arrow-success" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#10b981" />
    </marker>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{theme['primary_dark']}"/>
      <stop offset="100%" stop-color="{theme['primary']}"/>
    </linearGradient>
    <linearGradient id="nodeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f8fafc"/>
    </linearGradient>
  </defs>

  <!-- Header Banner -->
  <rect x="25" y="20" width="{width - 50}" height="80" rx="14" fill="url(#headerGrad)" filter="url(#shadow)"/>
  <rect x="45" y="36" width="130" height="24" rx="12" fill="{theme['badge_bg']}"/>
  <text x="110" y="52" fill="{theme['badge_text']}" font-size="11" font-weight="800" text-anchor="middle" letter-spacing="1">{layer_badge}</text>
  <text x="190" y="54" fill="#ffffff" font-size="21" font-weight="bold">{title}</text>
  <text x="45" y="84" fill="#e2e8f0" font-size="12" font-weight="400">{subtitle}</text>
  <text x="{width - 45}" y="62" fill="#cbd5e1" font-size="11" font-weight="600" text-anchor="end">Research Rover Architecture v2.0 • Verified Implementation</text>
'''

def get_svg_footer():
    return '</svg>'
