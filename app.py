"""
Synora — Executive Intelligence for Healthcare Operations
Executive dashboard for KPI analysis, operational intelligence, and decision support.
"""
from typing import Optional
import re
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Synora · Executive Intelligence for Healthcare Operations",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Premium dark healthcare SaaS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

:root {
    --synora-bg: #060912;
    --synora-surface: #0D1321;
    --synora-elevated: #141C2E;
    --synora-card: #111827;
    --synora-border: rgba(148, 163, 184, 0.12);
    --synora-cyan: #22D3EE;
    --synora-indigo: #818CF8;
    --synora-text: #F1F5F9;
    --synora-muted: #94A3B8;
    --synora-dim: #64748B;
    --synora-success: #34D399;
    --synora-warning: #FBBF24;
    --synora-critical: #F87171;
}

.stApp {
    background: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(34, 211, 238, 0.08), transparent),
                radial-gradient(ellipse 60% 40% at 100% 0%, rgba(129, 140, 248, 0.06), transparent),
                var(--synora-bg);
    color: var(--synora-text);
}

.main .block-container {
    color: var(--synora-text);
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080D18 0%, #0D1321 50%, #0A1020 100%);
    border-right: 1px solid var(--synora-border);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.75rem;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] label {
    color: var(--synora-muted) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--synora-border) !important;
    margin: 1.25rem 0 !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: var(--synora-muted) !important;
    font-weight: 500;
    font-size: 0.875rem !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 0.25rem;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 0.55rem 0.75rem;
    margin: 0;
    transition: all 0.18s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(34, 211, 238, 0.06);
    border-color: rgba(34, 211, 238, 0.15);
    color: var(--synora-text) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: rgba(34, 211, 238, 0.1) !important;
    border-color: rgba(34, 211, 238, 0.25) !important;
    color: var(--synora-cyan) !important;
}

/* Global markdown */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: var(--synora-muted);
}
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: var(--synora-text);
    font-family: 'DM Sans', sans-serif;
    letter-spacing: -0.02em;
}
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: var(--synora-text);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--synora-elevated) !important;
    border-color: var(--synora-border) !important;
    border-radius: 14px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li,
[data-testid="stVerticalBlockBorderWrapper"] span {
    color: var(--synora-muted) !important;
}
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: var(--synora-text) !important;
}

/* Sidebar brand */
.synora-sidebar-brand {
    padding: 0 0 1.5rem 0;
    margin-bottom: 0.25rem;
}
.synora-logo-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, rgba(34,211,238,0.2), rgba(129,140,248,0.2));
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-radius: 10px;
    font-size: 1rem;
    color: var(--synora-cyan);
    margin-bottom: 0.85rem;
}
.synora-logo {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--synora-text);
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.1;
}
.synora-logo span {
    background: linear-gradient(135deg, #22D3EE, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.synora-sidebar-tag {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: var(--synora-dim);
    margin-top: 0.4rem;
}
.synora-nav-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: var(--synora-dim);
    margin: 0.5rem 0 0.75rem 0;
}
.synora-sidebar-status {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid var(--synora-border);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-top: 0.5rem;
}
.synora-sidebar-status .status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    margin-right: 0.4rem;
    vertical-align: middle;
}
.status-dot-live { background: var(--synora-success); box-shadow: 0 0 8px rgba(52,211,153,0.5); }
.status-dot-idle { background: var(--synora-dim); }

/* Hero */
.synora-hero {
    background: linear-gradient(135deg, #0A1020 0%, #111827 45%, #0D1528 100%);
    border-radius: 20px;
    padding: 3rem 3.25rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(34, 211, 238, 0.15);
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
}
.synora-hero::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -8%;
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(34, 211, 238, 0.14) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.synora-hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 10%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(129, 140, 248, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.synora-hero-inner { position: relative; z-index: 1; }
.synora-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(34, 211, 238, 0.08);
    border: 1px solid rgba(34, 211, 238, 0.25);
    color: var(--synora-cyan);
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    padding: 0.35rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1.25rem;
}
.synora-hero-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--synora-text);
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.04em;
    line-height: 1.05;
}
.synora-hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 500;
    color: var(--synora-cyan);
    margin: 0 0 1rem 0;
    letter-spacing: -0.01em;
}
.synora-hero-desc {
    font-size: 0.95rem;
    color: var(--synora-muted);
    margin: 0 0 1.75rem 0;
    max-width: 560px;
    line-height: 1.7;
}
.synora-hero-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--synora-border);
}
.synora-hero-stat {
    min-width: 120px;
}
.synora-hero-stat-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--synora-text);
    letter-spacing: -0.02em;
}
.synora-hero-stat-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--synora-dim);
    margin-top: 0.2rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}

/* Page headers */
.page-header {
    margin-bottom: 2rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--synora-border);
}
.page-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--synora-text);
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.03em;
}
.page-subtitle {
    font-size: 0.925rem;
    color: var(--synora-muted);
    margin: 0;
    line-height: 1.5;
}

.section-header {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--synora-cyan);
    margin: 2rem 0 1rem 0;
}

/* Executive KPI cards */
.metric-card {
    background: linear-gradient(145deg, var(--synora-elevated) 0%, var(--synora-card) 100%);
    border-radius: 16px;
    padding: 1.5rem 1.35rem;
    border: 1px solid var(--synora-border);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
    height: 100%;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--synora-cyan), var(--synora-indigo));
    opacity: 0.7;
}
.metric-card:hover {
    border-color: rgba(34, 211, 238, 0.25);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--synora-dim);
    margin-bottom: 0.75rem;
}
.metric-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--synora-text);
    line-height: 1;
    margin-bottom: 0.35rem;
    letter-spacing: -0.03em;
}
.metric-unit {
    font-size: 0.78rem;
    color: var(--synora-muted);
    font-weight: 500;
    margin-bottom: 0.85rem;
}
.metric-status {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
}
.status-success { background: rgba(52, 211, 153, 0.12); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.25); }
.status-warning { background: rgba(251, 191, 36, 0.12); color: #FBBF24; border: 1px solid rgba(251, 191, 36, 0.25); }
.status-critical { background: rgba(248, 113, 113, 0.12); color: #F87171; border: 1px solid rgba(248, 113, 113, 0.25); }
.status-neutral { background: rgba(148, 163, 184, 0.1); color: var(--synora-muted); border: 1px solid var(--synora-border); }

/* App cards */
.app-card {
    background: var(--synora-elevated);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    border: 1px solid var(--synora-border);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    margin-bottom: 1.25rem;
    color: var(--synora-muted);
}
.app-card-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--synora-text);
    margin-bottom: 0.5rem;
}

/* Alerts */
.alert-critical {
    background: rgba(248, 113, 113, 0.06);
    border: 1px solid rgba(248, 113, 113, 0.2);
    border-left: 4px solid var(--synora-critical);
    border-radius: 12px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.85rem;
}
.alert-warning {
    background: rgba(251, 191, 36, 0.06);
    border: 1px solid rgba(251, 191, 36, 0.2);
    border-left: 4px solid var(--synora-warning);
    border-radius: 12px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.85rem;
}
.alert-success {
    background: rgba(52, 211, 153, 0.06);
    border: 1px solid rgba(52, 211, 153, 0.2);
    border-left: 4px solid var(--synora-success);
    border-radius: 12px;
    padding: 1.15rem 1.35rem;
    margin-bottom: 0.85rem;
}
.alert-title {
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
    color: var(--synora-text);
}
.alert-body {
    font-size: 0.85rem;
    color: var(--synora-muted);
    line-height: 1.55;
}

/* Summary & recommendations */
.summary-card {
    background: var(--synora-elevated);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    border: 1px solid var(--synora-border);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    margin-bottom: 1.25rem;
    color: var(--synora-muted);
}
.summary-heading {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--synora-text);
    margin-bottom: 0.65rem;
}
.summary-body {
    font-size: 0.88rem;
    color: var(--synora-muted);
    line-height: 1.65;
}
.summary-body p { color: var(--synora-muted); margin: 0 0 0.5rem 0; }
.summary-body strong { color: var(--synora-text); font-weight: 600; }

.report-section {
    background: var(--synora-elevated);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    border: 1px solid var(--synora-border);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    margin-bottom: 1.25rem;
    color: var(--synora-muted);
}
.report-section h2 {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--synora-text) !important;
    margin: 0 0 0.85rem 0;
}
.report-section h3 {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--synora-cyan) !important;
    margin: 0.85rem 0 0.45rem 0;
}
.report-section p, .report-section li {
    color: var(--synora-muted) !important;
    font-size: 0.88rem;
    line-height: 1.65;
}
.report-section strong { color: var(--synora-text) !important; }

.rec-card {
    background: var(--synora-elevated);
    border-radius: 14px;
    padding: 1.35rem 1.5rem;
    border: 1px solid var(--synora-border);
    border-left: 4px solid var(--synora-cyan);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    margin-bottom: 1rem;
}
.rec-priority-high { border-left-color: var(--synora-critical); }
.rec-priority-med  { border-left-color: var(--synora-warning); }
.rec-priority-low  { border-left-color: var(--synora-success); }
.rec-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--synora-text);
    margin-bottom: 0.35rem;
}
.rec-body {
    font-size: 0.85rem;
    color: var(--synora-muted);
    line-height: 1.6;
}
.priority-badge {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.55rem;
}
.badge-high { background: rgba(248, 113, 113, 0.12); color: var(--synora-critical); border: 1px solid rgba(248, 113, 113, 0.25); }
.badge-med  { background: rgba(251, 191, 36, 0.12); color: var(--synora-warning); border: 1px solid rgba(251, 191, 36, 0.25); }
.badge-low  { background: rgba(52, 211, 153, 0.12); color: var(--synora-success); border: 1px solid rgba(52, 211, 153, 0.25); }

/* Upload zone */
.upload-panel {
    background: var(--synora-elevated);
    border: 1px solid var(--synora-border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.upload-zone {
    background: rgba(6, 9, 18, 0.5);
    border: 2px dashed rgba(34, 211, 238, 0.25);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    transition: border-color 0.2s ease;
}
.upload-zone:hover {
    border-color: rgba(34, 211, 238, 0.45);
}
.upload-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    background: rgba(34, 211, 238, 0.08);
    border: 1px solid rgba(34, 211, 238, 0.2);
    border-radius: 14px;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}
.upload-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: var(--synora-text);
    font-size: 1rem;
    margin-bottom: 0.35rem;
}
.upload-hint {
    font-size: 0.8rem;
    color: var(--synora-dim);
    margin-top: 0.5rem;
    line-height: 1.5;
}
.upload-columns {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-top: 1.25rem;
}
.upload-col-tag {
    font-size: 0.68rem;
    font-weight: 500;
    color: var(--synora-muted);
    background: rgba(17, 24, 39, 0.8);
    border: 1px solid var(--synora-border);
    border-radius: 6px;
    padding: 0.25rem 0.55rem;
    font-family: 'Inter', monospace;
}

/* Executive stat cards */
.fin-card {
    background: linear-gradient(145deg, var(--synora-elevated) 0%, var(--synora-card) 100%);
    border-radius: 16px;
    padding: 1.5rem 1.25rem;
    border: 1px solid var(--synora-border);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.fin-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--synora-cyan), transparent);
    opacity: 0.5;
}
.fin-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--synora-text);
    line-height: 1;
    letter-spacing: -0.03em;
}
.fin-label {
    font-size: 0.72rem;
    color: var(--synora-dim);
    margin-top: 0.5rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Buttons */
.stButton > button[kind="primary"],
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(129,140,248,0.15)) !important;
    color: var(--synora-cyan) !important;
    border: 1px solid rgba(34, 211, 238, 0.35) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 1.35rem !important;
    box-shadow: 0 4px 16px rgba(34, 211, 238, 0.1) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(34,211,238,0.25), rgba(129,140,248,0.2)) !important;
    border-color: var(--synora-cyan) !important;
    box-shadow: 0 6px 24px rgba(34, 211, 238, 0.2) !important;
    color: var(--synora-text) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--synora-elevated) !important;
    color: var(--synora-muted) !important;
    border: 1px solid var(--synora-border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: transparent;
}
[data-testid="stFileUploader"] section {
    background: rgba(6, 9, 18, 0.4) !important;
    border: 1px dashed rgba(34, 211, 238, 0.2) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section small {
    color: var(--synora-muted) !important;
}

/* Dataframe & expander */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.stExpander {
    background: var(--synora-elevated);
    border: 1px solid var(--synora-border);
    border-radius: 12px;
}

.chart-wrap {
    background: var(--synora-elevated);
    border-radius: 16px;
    border: 1px solid var(--synora-border);
    padding: 0.75rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.section-divider {
    height: 1px;
    background: var(--synora-border);
    margin: 2rem 0;
}

.synora-footer {
    text-align: center;
    font-size: 0.72rem;
    color: var(--synora-dim);
    padding: 2.5rem 0 1rem 0;
    border-top: 1px solid var(--synora-border);
    margin-top: 2rem;
}

.empty-state {
    background: var(--synora-elevated);
    border: 1px dashed rgba(34, 211, 238, 0.2);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    text-align: center;
    color: var(--synora-muted);
}
.empty-state strong { color: var(--synora-text); }

/* Platform showcase cards */
.platform-banner {
    background: linear-gradient(135deg, #0A1020 0%, #141C2E 55%, #0D1528 100%);
    border-radius: 20px;
    padding: 2.25rem 2.75rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(34, 211, 238, 0.15);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
}
.platform-metric {
    text-align: center;
    padding: 1.25rem 0.75rem;
}
.platform-metric-value {
    font-family: 'DM Sans', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--synora-text);
    line-height: 1;
    letter-spacing: -0.03em;
}
.platform-metric-label {
    font-size: 0.75rem;
    color: var(--synora-dim);
    margin-top: 0.4rem;
    line-height: 1.45;
}
.tech-stack-bar {
    background: var(--synora-elevated);
    border: 1px solid var(--synora-border);
    border-radius: 14px;
    padding: 1.35rem 1.75rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI DEFINITIONS: thresholds and metadata
# ─────────────────────────────────────────────
KPI_CONFIG = {
    "ED Visits":           {"col": "ED_Visits",          "unit": "visits/day", "threshold": None,  "higher_is_bad": False},
    "Length of Stay":      {"col": "LOS_Hours",           "unit": "hrs",        "threshold": 7.0,   "higher_is_bad": True},
    "Door-to-Provider":    {"col": "Door_to_Provider_Min","unit": "min",        "threshold": None,  "higher_is_bad": True},
    "LWBS Rate":           {"col": "LWBS_Rate",           "unit": "%",          "threshold": 4.0,   "higher_is_bad": True},
    "Boarding Hours":      {"col": "Boarding_Hours",      "unit": "hrs",        "threshold": 15.0,  "higher_is_bad": True},
    "Staff Gap":           {"col": "Staff_Gap",           "unit": "FTEs",       "threshold": 5.0,   "higher_is_bad": True},
    "Admission Rate":      {"col": "Admission_Rate",      "unit": "%",          "threshold": None,  "higher_is_bad": False},
}

# Chart accent colors (Synora dark palette)
CHART_COLORS = [
    "#22D3EE", "#818CF8", "#34D399", "#FBBF24",
    "#F87171", "#A78BFA", "#38BDF8"
]

NAV_PAGES = [
    "Overview",
    "Upload Data",
    "ED Operations",
    "Financial Impact",
    "AI Advisor",
    "Reports",
]

NAV_ICONS = {
    "Overview": "◈",
    "Upload Data": "↑",
    "ED Operations": "◉",
    "Financial Impact": "◆",
    "AI Advisor": "✦",
    "Reports": "▤",
}


# ─────────────────────────────────────────────
# HELPER: Generate sample CSV for download
# ─────────────────────────────────────────────
def generate_sample_csv() -> bytes:
    """Create a realistic sample hospital KPI CSV with 12 weeks of data."""
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=12, freq="W")
    data = {
        "Date":                pd.Series(dates).dt.strftime("%Y-%m-%d"),
        "ED_Visits":           np.random.randint(280, 420, 12),
        "LOS_Hours":           np.round(np.random.uniform(5.5, 9.5, 12), 1),
        "Door_to_Provider_Min":np.random.randint(18, 55, 12),
        "LWBS_Rate":           np.round(np.random.uniform(1.5, 6.5, 12), 1),
        "Boarding_Hours":      np.round(np.random.uniform(8.0, 22.0, 12), 1),
        "Staff_Gap":           np.random.randint(0, 12, 12),
        "Admission_Rate":      np.round(np.random.uniform(18.0, 35.0, 12), 1),
    }
    return pd.DataFrame(data).to_csv(index=False).encode()


# ─────────────────────────────────────────────
# HELPER: Render a single metric card via HTML
# ─────────────────────────────────────────────
def kpi_status_for_display(col: str, avg: float, cfg: dict) -> tuple[str, str]:
    """Return (status_css_class, status_label) for KPI card display only."""
    threshold = cfg.get("threshold")
    if threshold is None:
        if col == "Door_to_Provider_Min" and avg > 35:
            return "status-warning", "Above benchmark"
        return "status-neutral", "Tracking"
    higher_is_bad = cfg.get("higher_is_bad", True)
    if higher_is_bad:
        if avg > threshold:
            return ("status-critical", "Critical") if avg > threshold * 1.1 else ("status-warning", "Needs attention")
        return "status-success", "On track"
    return "status-neutral", "Tracking"


def metric_card(label: str, value: str, unit: str, status_class: str = "status-neutral",
                status_label: str = "Tracking"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
        <span class="metric-status {status_class}">{status_label}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: Build a styled Plotly line chart
# ─────────────────────────────────────────────
def build_line_chart(df: pd.DataFrame, col: str, label: str, unit: str,
 color: str, threshold: Optional[float]) -> go.Figure:
    """Return a clean Plotly figure for a single KPI over time."""
    fig = go.Figure()

    # KPI line
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df[col],
        mode="lines+markers",
        name=label,
        line=dict(color=color, width=2.5),
        marker=dict(size=6, color=color),
        hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y}} {unit}<extra></extra>",
    ))

    # Optional threshold reference line
    if threshold is not None:
        fig.add_hline(
            y=threshold,
            line_dash="dot",
            line_color="#DC2626",
            line_width=1.5,
            annotation_text=f"  Threshold: {threshold} {unit}",
            annotation_font=dict(size=10, color="#DC2626"),
        )

    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11, color="#94A3B8"),
        title=dict(text=label, font=dict(size=13, color="#F1F5F9", family="DM Sans"), x=0.02),
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#64748B"), linecolor="rgba(148,163,184,0.15)"),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.08)",
            tickfont=dict(size=9, color="#64748B"),
            linecolor="rgba(148,163,184,0.15)",
            title=dict(text=unit, font=dict(size=9, color="#64748B")),
        ),
        legend=dict(orientation="h", y=-0.25, font=dict(size=9, color="#94A3B8")),
        hovermode="x unified",
    )
    return fig


# ─────────────────────────────────────────────
# SECTION 4: Problem Area Detection
# ─────────────────────────────────────────────
def detect_problems(df: pd.DataFrame) -> list[dict]:
    """
    Evaluate KPI averages against clinical thresholds.
    Returns a list of alert dicts with level, title, and message.
    """
    alerts = []
    avgs = df.mean(numeric_only=True)

    # Length of Stay > 7 hours
    if "LOS_Hours" in avgs and avgs["LOS_Hours"] > 7.0:
        alerts.append({
            "level": "critical",
            "title": "⚠ Elevated Length of Stay",
            "msg": f"Average LOS is {avgs['LOS_Hours']:.1f} hrs (threshold: 7.0 hrs). "
                   "Prolonged stays reduce bed availability and increase patient risk."
        })

    # LWBS Rate > 4%
    if "LWBS_Rate" in avgs and avgs["LWBS_Rate"] > 4.0:
        alerts.append({
            "level": "critical",
            "title": "⚠ High Left-Without-Being-Seen Rate",
            "msg": f"Average LWBS is {avgs['LWBS_Rate']:.1f}% (threshold: 4.0%). "
                   "High LWBS signals overcrowding and may indicate revenue leakage."
        })

    # Staff Gap > 5 FTEs
    if "Staff_Gap" in avgs and avgs["Staff_Gap"] > 5.0:
        alerts.append({
            "level": "warning",
            "title": "⚠ Persistent Staffing Deficit",
            "msg": f"Average staff gap is {avgs['Staff_Gap']:.1f} FTEs (threshold: 5.0). "
                   "Sustained gaps increase burnout risk and care quality concerns."
        })

    # Boarding Hours > 15
    if "Boarding_Hours" in avgs and avgs["Boarding_Hours"] > 15.0:
        alerts.append({
            "level": "warning",
            "title": "⚠ Excessive ED Boarding",
            "msg": f"Average boarding is {avgs['Boarding_Hours']:.1f} hrs (threshold: 15.0 hrs). "
                   "Boarding reflects downstream throughput failures in inpatient units."
        })

    return alerts


# ─────────────────────────────────────────────
# SECTION 5: Executive Summary
# ─────────────────────────────────────────────
def render_executive_summary(df: pd.DataFrame, alerts: list[dict]):
    """Generate a narrative executive summary from KPI data."""
    avgs = df.mean(numeric_only=True)

    # Trend analysis: compare first half vs second half of the period
    mid = len(df) // 2
    first_half  = df.iloc[:mid].mean(numeric_only=True)
    second_half = df.iloc[mid:].mean(numeric_only=True)

    # Identify improving vs worsening KPIs
    improving, worsening = [], []
    for name, cfg in KPI_CONFIG.items():
        col = cfg["col"]
        if col not in df.columns:
            continue
        delta = second_half[col] - first_half[col]
        if cfg["higher_is_bad"]:
            if delta < -0.5:
                improving.append(name)
            elif delta > 0.5:
                worsening.append(name)
        else:
            if delta > 0.5:
                improving.append(name)
            elif delta < -0.5:
                worsening.append(name)

    # Build summary text
    risk_count = len(alerts)
    risk_label = "no critical risk flags" if risk_count == 0 else \
                 f"{risk_count} operational risk area{'s' if risk_count > 1 else ''}"

    # Overview
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-heading">📋 Overview</div>
        <div class="summary-body">
            <p>Analysis of the uploaded KPI dataset covering <strong>{len(df)} reporting periods</strong>
            identified <strong>{risk_label}</strong> against established clinical thresholds.
            The ED processed an average of <strong>{avgs.get('ED_Visits', 0):.0f} visits per period</strong>
            with a mean admission rate of <strong>{avgs.get('Admission_Rate', 0):.1f}%</strong>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        trend_parts = []
        if worsening:
            trend_parts.append(
                f"<p>📈 <strong>Worsening:</strong> {', '.join(worsening)} trended higher "
                "in the latter portion of the reporting period.</p>"
            )
        if improving:
            trend_parts.append(
                f"<p>📉 <strong>Improving:</strong> {', '.join(improving)} showed measurable "
                "improvement over time.</p>"
            )
        if not worsening and not improving:
            trend_parts.append(
                "<p>Metrics remained relatively stable across the reporting period "
                "with no pronounced directional trends.</p>"
            )
        trends_html = "\n".join(trend_parts)
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-heading">📈 Major Trends</div>
            <div class="summary-body">{trends_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if alerts:
            risk_items = "".join(
                f"<p>{'🔴' if a['level'] == 'critical' else '🟡'} "
                f"{a['title'].replace('⚠ ', '')}</p>"
                for a in alerts
            )
        else:
            risk_items = "<p>✅ No KPIs exceeded defined thresholds during this period.</p>"
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-heading">⚠️ Operational Risks</div>
            <div class="summary-body">{risk_items}</div>
        </div>
        """, unsafe_allow_html=True)

    # Areas performing well
    well = []
    if "LOS_Hours" in avgs and avgs["LOS_Hours"] <= 7.0:
        well.append(f"<p>✅ Length of Stay ({avgs['LOS_Hours']:.1f} hrs) is within target</p>")
    if "LWBS_Rate" in avgs and avgs["LWBS_Rate"] <= 4.0:
        well.append(f"<p>✅ LWBS Rate ({avgs['LWBS_Rate']:.1f}%) is within acceptable range</p>")
    if "Staff_Gap" in avgs and avgs["Staff_Gap"] <= 5.0:
        well.append(f"<p>✅ Staffing Gap ({avgs['Staff_Gap']:.1f} FTEs) is manageable</p>")
    if "Boarding_Hours" in avgs and avgs["Boarding_Hours"] <= 15.0:
        well.append(f"<p>✅ Boarding Hours ({avgs['Boarding_Hours']:.1f} hrs) remain below threshold</p>")
    if not well:
        well.append("<p>All monitored KPIs require attention in the current period.</p>")
    well_html = "\n".join(well)
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-heading">✅ Areas Performing Well</div>
        <div class="summary-body">{well_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 6: Recommendations Engine
# ─────────────────────────────────────────────
def render_recommendations(df: pd.DataFrame, alerts: list[dict]):
    """Produce prioritized, evidence-based recommendations from alert signals."""
    avgs = df.mean(numeric_only=True)
    recs = []

    # High LOS → discharge process improvement
    if "LOS_Hours" in avgs and avgs["LOS_Hours"] > 7.0:
        recs.append({
            "priority": "high",
            "title": "Improve Discharge Planning Processes",
            "body": (
                "Implement a multidisciplinary discharge rounds model beginning at 7 AM daily. "
                "Introduce anticipated discharge date flags in the EMR to activate social work, "
                "case management, and pharmacy earlier in the admission. "
                "Target same-day discharge before noon for eligible patients."
            )
        })

    # High LWBS → patient flow & triage redesign
    if "LWBS_Rate" in avgs and avgs["LWBS_Rate"] > 4.0:
        recs.append({
            "priority": "high",
            "title": "Redesign Triage and Patient Flow in the ED",
            "body": (
                "Deploy a provider-in-triage (PIT) model during peak hours (10 AM – 10 PM) "
                "to initiate workups before a bed is available. "
                "Evaluate fast-track or split-flow pathways for low-acuity ESI 4/5 patients. "
                "Target LWBS reduction to below 2% within 90 days."
            )
        })

    # High Staff Gap → workforce optimization
    if "Staff_Gap" in avgs and avgs["Staff_Gap"] > 5.0:
        recs.append({
            "priority": "high" if avgs["Staff_Gap"] > 8 else "medium",
            "title": "Launch Workforce Optimization Initiative",
            "body": (
                "Conduct an immediate staffing demand forecast by shift and service line. "
                "Explore float pool expansion, per-diem contracting, and cross-training programs. "
                "Review scheduling software for demand-matching capability "
                "and address root causes of turnover through retention analysis."
            )
        })

    # High Boarding → inpatient throughput
    if "Boarding_Hours" in avgs and avgs["Boarding_Hours"] > 15.0:
        recs.append({
            "priority": "medium",
            "title": "Accelerate Inpatient Throughput Initiatives",
            "body": (
                "Establish an executive-level Bed Management Committee with daily huddles. "
                "Implement real-time bed tracking and nursing communication protocols. "
                "Evaluate the feasibility of a 'pull until full' model from the ED. "
                "Boarding above 15 hours is a system-wide throughput signal—not an ED-only issue."
            )
        })

    # Door-to-Provider time secondary recommendation
    if "Door_to_Provider_Min" in avgs and avgs["Door_to_Provider_Min"] > 35:
        recs.append({
            "priority": "medium",
            "title": "Reduce Door-to-Provider Time",
            "body": (
                f"Current average door-to-provider time of {avgs['Door_to_Provider_Min']:.0f} min "
                "exceeds the recommended 30-minute benchmark. "
                "Evaluate bedside registration processes, immediate bedding protocols, "
                "and team-triage models to compress the patient arrival-to-assessment interval."
            )
        })

    # If everything is in range, celebrate and encourage monitoring
    if not recs:
        recs.append({
            "priority": "low",
            "title": "Sustain Current Performance Standards",
            "body": (
                "All monitored KPIs are within defined thresholds. "
                "Continue bi-weekly KPI review cadence with department leads. "
                "Consider benchmarking against national ED performance databases (e.g., ACEP, CMS) "
                "to set stretch targets for continuous improvement."
            )
        })

    # Render recommendation cards
    priority_labels = {"high": "High Priority", "medium": "Medium Priority", "low": "Sustain"}
    badge_classes   = {"high": "badge-high",     "medium": "badge-med",        "low": "badge-low"}
    card_classes    = {"high": "rec-priority-high","medium": "rec-priority-med","low": "rec-priority-low"}

    for rec in recs:
        p  = rec["priority"]
        st.markdown(f"""
        <div class="rec-card {card_classes[p]}">
            <span class="priority-badge {badge_classes[p]}">{priority_labels[p]}</span>
            <div class="rec-title">{rec['title']}</div>
            <div class="rec-body">{rec['body']}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SECTION 7: AI Consultant Report Generator
# Rule-based logic that produces a COO-grade
# consulting narrative from KPI thresholds.
# ─────────────────────────────────────────────
def generate_consultant_report(df: pd.DataFrame, alerts: list[dict]) -> str:
    """
    Synthesize KPI data into a structured consultant report.
    Returns a multi-section markdown string.
    """
    avgs   = df.mean(numeric_only=True)
    mid    = len(df) // 2
    first  = df.iloc[:mid].mean(numeric_only=True)
    second = df.iloc[mid:].mean(numeric_only=True)
    date_range = f"{df['Date'].min().strftime('%B %Y')} – {df['Date'].max().strftime('%B %Y')}"
    n_periods  = len(df)

    # ── Identify which KPIs are breaching thresholds
    los_breach      = avgs.get("LOS_Hours", 0)          > 7.0
    lwbs_breach     = avgs.get("LWBS_Rate", 0)          > 4.0
    staff_breach    = avgs.get("Staff_Gap", 0)           > 5.0
    boarding_breach = avgs.get("Boarding_Hours", 0)      > 15.0
    d2p_breach      = avgs.get("Door_to_Provider_Min", 0) > 35

    los_val      = avgs.get("LOS_Hours", 0)
    lwbs_val     = avgs.get("LWBS_Rate", 0)
    staff_val    = avgs.get("Staff_Gap", 0)
    boarding_val = avgs.get("Boarding_Hours", 0)
    d2p_val      = avgs.get("Door_to_Provider_Min", 0)
    ed_val       = avgs.get("ED_Visits", 0)
    admit_val    = avgs.get("Admission_Rate", 0)

    # ── Trend direction helpers
    def trend(col):
        if col not in first.index or col not in second.index:
            return "stable"
        d = second[col] - first[col]
        if d > 0.5:  return "worsening"
        if d < -0.5: return "improving"
        return "stable"

    los_trend      = trend("LOS_Hours")
    lwbs_trend     = trend("LWBS_Rate")
    staff_trend    = trend("Staff_Gap")
    boarding_trend = trend("Boarding_Hours")

    # ── Count breaches for severity framing
    breach_count = sum([los_breach, lwbs_breach, staff_breach, boarding_breach, d2p_breach])
    if breach_count >= 3:
        severity = "significant operational stress"
        severity_adj = "critical"
    elif breach_count == 2:
        severity = "moderate operational risk"
        severity_adj = "concerning"
    elif breach_count == 1:
        severity = "an isolated performance gap"
        severity_adj = "manageable"
    else:
        severity = "strong operational health"
        severity_adj = "positive"

    # ── Estimate financial impact (rule-based approximations)
    daily_admissions = ed_val * (admit_val / 100)
    los_excess_hrs   = max(0, los_val - 7.0)
    los_financial    = los_excess_hrs * 200 * daily_admissions * 30

    lwbs_excess      = max(0, lwbs_val - 2.0)
    avg_ed_rev_visit = 1200
    lwbs_financial   = (lwbs_excess / 100) * ed_val * avg_ed_rev_visit * 4

    staff_premium    = max(0, staff_val) * 85 * 21 * 8

    total_financial  = los_financial + lwbs_financial + staff_premium

    def fmt_dollar(val):
        if val >= 1_000_000: return f"${val/1_000_000:.1f}M"
        if val >= 1_000:     return f"${val/1_000:.0f}K"
        return f"${val:.0f}"

    # ══════════════════════════════════════════
    # BUILD THE REPORT MARKDOWN
    # ══════════════════════════════════════════
    report = []

    # ── 1. EXECUTIVE SUMMARY
    report.append("## 1. Executive Summary")
    report.append(
        f"This operational assessment covers **{n_periods} reporting periods** from **{date_range}**, "
        f"encompassing Emergency Department performance, throughput efficiency, staffing adequacy, "
        f"and patient flow metrics at this facility."
    )
    report.append(
        f"The data reveals **{severity}** across the monitored KPI portfolio. "
        f"Of the five primary benchmarks assessed, **{breach_count} exceed{'s' if breach_count==1 else ''} "
        f"established clinical thresholds**, presenting {'a ' + severity_adj + ' risk profile' if breach_count > 0 else 'a ' + severity_adj + ' outlook'} "
        f"for operational leadership."
    )
    if breach_count > 0:
        report.append(
            f"Left unaddressed, the combination of these performance gaps is estimated to generate "
            f"**{fmt_dollar(total_financial)} in excess monthly costs and foregone revenue**, "
            f"representing a material financial and quality-of-care concern that warrants immediate executive attention."
        )
    else:
        report.append(
            "The facility is performing within acceptable ranges across all monitored dimensions. "
            "Leadership should focus on sustaining current performance and setting stretch benchmarks "
            "to drive continuous improvement."
        )

    # ── 2. KEY PERFORMANCE ISSUES
    report.append("\n## 2. Key Performance Issues")

    if not any([los_breach, lwbs_breach, staff_breach, boarding_breach, d2p_breach]):
        report.append("No KPIs currently exceed defined thresholds. The facility is operating within benchmark ranges.")
    else:
        if los_breach:
            report.append(
                f"**Length of Stay ({los_val:.1f} hrs | Benchmark: ≤7.0 hrs)** — "
                f"LOS is running **{los_val - 7.0:.1f} hours above target** and is {los_trend}. "
                f"Prolonged stays reduce bed availability, increase infection exposure risk, "
                f"and compress downstream capacity for incoming admissions."
            )
        if lwbs_breach:
            report.append(
                f"**Left Without Being Seen Rate ({lwbs_val:.1f}% | Benchmark: ≤4.0%)** — "
                f"LWBS is {lwbs_trend} and exceeds threshold by **{lwbs_val - 4.0:.1f} percentage points**. "
                f"Each percentage point above baseline represents patients who left without care — "
                f"a direct patient safety signal and a revenue leakage indicator."
            )
        if boarding_breach:
            report.append(
                f"**ED Boarding Hours ({boarding_val:.1f} hrs | Benchmark: ≤15.0 hrs)** — "
                f"Boarding is {boarding_trend} and reflects a systemic inpatient throughput failure. "
                f"When admitted patients board in the ED for extended periods, it occupies beds needed "
                f"for incoming patients and is a primary driver of LWBS and LOS escalation."
            )
        if staff_breach:
            report.append(
                f"**Staffing Gap ({staff_val:.1f} FTEs | Benchmark: ≤5.0 FTEs)** — "
                f"The facility is carrying a persistent staffing deficit that is {staff_trend}. "
                f"Sustained gaps of this magnitude increase reliance on overtime and agency labor, "
                f"elevate burnout risk among permanent staff, and compromise care consistency."
            )
        if d2p_breach:
            report.append(
                f"**Door-to-Provider Time ({d2p_val:.0f} min | Benchmark: ≤35 min)** — "
                f"Patients are waiting an average of {d2p_val:.0f} minutes before first provider contact. "
                f"This metric is a leading indicator of patient dissatisfaction and early departure, "
                f"directly contributing to the elevated LWBS rate."
            )

    # ── 3. LIKELY ROOT CAUSES
    report.append("\n## 3. Likely Root Causes")

    causes = []
    if boarding_breach or los_breach:
        causes.append(
            "**Insufficient Inpatient Bed Availability:** The most common driver of both elevated LOS "
            "and prolonged boarding is inadequate inpatient capacity relative to ED admission demand. "
            f"With an average admission rate of {admit_val:.1f}%, the facility is converting a meaningful "
            "proportion of ED visits to inpatient stays, creating sustained downstream pressure."
        )
    if staff_breach or d2p_breach:
        causes.append(
            "**Staffing Model Misalignment:** A staffing gap of this scale suggests the current FTE model "
            "does not reflect actual demand patterns. This is often caused by scheduling that doesn't account "
            "for peak-hour surges, high turnover in key roles, or an over-reliance on PRN/agency coverage "
            "that introduces variability in team performance and handoff quality."
        )
    if lwbs_breach or d2p_breach:
        causes.append(
            "**Patient Flow Bottlenecks at Triage and Intake:** Elevated door-to-provider times and LWBS "
            "rates are consistent with an intake model that has not scaled with volume. "
            f"At {ed_val:.0f} average ED visits per period, the current triage and bedding processes "
            "are likely creating visible wait times that prompt patients to leave before assessment."
        )
    if los_breach and not boarding_breach:
        causes.append(
            "**Discharge Process Inefficiency:** When LOS is elevated in the absence of severe boarding, "
            "the root cause typically lies in discharge workflow — late physician order entry, "
            "delays in social work or case management engagement, medication reconciliation backlogs, "
            "or transportation coordination failures at the end of stay."
        )
    if not causes:
        causes.append(
            "No threshold breaches detected. Root cause analysis is not indicated at this time. "
            "Recommend quarterly review to confirm sustained performance."
        )
    for c in causes:
        report.append(c)

    # ── 4. OPERATIONAL IMPACT
    report.append("\n## 4. Operational Impact")

    impacts = []
    if lwbs_breach:
        impacts.append(
            f"A LWBS rate of {lwbs_val:.1f}% signals that patients are actively choosing to leave rather "
            "than wait for care. Beyond the immediate safety concern, this reflects a reputational risk: "
            "patients who leave without being seen rarely return and frequently share negative experiences. "
            "In competitive markets, sustained LWBS above 4% measurably erodes market share."
        )
    if boarding_breach:
        impacts.append(
            f"With average boarding at {boarding_val:.1f} hours, the ED is effectively operating as a "
            "holding unit for admitted patients. This compresses treatment capacity, delays ambulance "
            "offload, and creates a cascading effect on all downstream throughput metrics. "
            "Boarding is also the strongest predictor of nursing burnout in acute care settings."
        )
    if los_breach:
        impacts.append(
            f"An average LOS of {los_val:.1f} hours means each bed is turning over more slowly than "
            f"benchmarked. For a facility processing {ed_val:.0f} visits per period, this represents "
            "a compounding constraint on total throughput capacity — effectively reducing the number "
            "of patients the department can serve without physical expansion."
        )
    if staff_breach:
        impacts.append(
            f"A staffing gap of {staff_val:.1f} FTEs, if covered through overtime, generates premium "
            "labor costs and accelerates burnout. If left uncovered, it reduces care team capacity, "
            "lengthens task completion times, and introduces patient safety risk through workload compression."
        )
    if not impacts:
        impacts.append(
            "Current operational metrics do not indicate material negative impact on throughput, "
            "staffing stability, or patient experience. The facility should maintain current "
            "performance management cadence."
        )
    for i in impacts:
        report.append(i)

    # ── 5. ESTIMATED FINANCIAL IMPACT
    report.append("\n## 5. Estimated Financial Impact")
    report.append(
        "The following estimates are based on industry-standard cost benchmarks and the KPI variances "
        "observed in this dataset. These figures are directional and should be validated against "
        "facility-specific payer mix, cost structures, and volume data."
    )

    fin_lines = []
    if los_breach:
        fin_lines.append(
            f"- **Excess LOS Cost:** {fmt_dollar(los_financial)}/month — "
            f"Based on {los_excess_hrs:.1f} excess hours per stay × ~$200 loaded bed cost × "
            f"{daily_admissions:.0f} estimated daily admissions"
        )
    if lwbs_breach:
        fin_lines.append(
            f"- **LWBS Revenue Leakage:** {fmt_dollar(lwbs_financial)}/month — "
            f"Based on {lwbs_excess:.1f}% excess LWBS × {ed_val:.0f} visits × "
            f"~$1,200 average net ED revenue per visit"
        )
    if staff_breach:
        fin_lines.append(
            f"- **Excess Staffing Cost (Overtime/Agency Premium):** {fmt_dollar(staff_premium)}/month — "
            f"Based on {staff_val:.1f} FTE gap × ~$85/hr premium × estimated shift coverage"
        )
    if fin_lines:
        for fl in fin_lines:
            report.append(fl)
        report.append(f"\n**Estimated Total Monthly Financial Exposure: {fmt_dollar(total_financial)}**")
        report.append(
            f"On an annualized basis, this represents approximately **{fmt_dollar(total_financial * 12)} "
            f"in addressable cost and revenue opportunity** — a strong business case for targeted "
            "operational investment."
        )
    else:
        report.append(
            "No threshold breaches detected. Financial exposure from KPI variances is minimal. "
            "Recommend tracking cost-per-visit and net revenue per admission as forward-looking indicators."
        )

    # ── 6. 30-60-90 DAY ACTION PLAN
    report.append("\n## 6. 30-60-90 Day Action Plan")

    report.append("### 🔴 Days 1–30: Stabilize")
    day30 = []
    if staff_breach:
        day30.append("- **Staffing Emergency Protocol:** Activate float pool and issue agency contracts for immediate gap coverage. Freeze non-essential PTO approvals for 30 days while demand analysis is completed.")
    if d2p_breach or lwbs_breach:
        day30.append("- **Provider-in-Triage (PIT) Pilot:** Deploy one attending or advanced practice provider to triage during peak hours (10 AM – 10 PM) to initiate workups before a bed is assigned.")
    if boarding_breach:
        day30.append("- **Daily Bed Huddle:** Launch a 7 AM bed management huddle with ED charge, house supervisor, and inpatient unit leads to proactively identify and clear holds before the daily surge.")
    if los_breach:
        day30.append("- **Discharge Before Noon Initiative:** Identify and flag top 5 discharge-delay diagnoses. Assign case management to all anticipated next-day discharges by 3 PM the prior day.")
    if not day30:
        day30.append("- Conduct a baseline performance audit and establish stretch KPI targets for the next 90 days.")
    for item in day30:
        report.append(item)

    report.append("\n### 🟡 Days 31–60: Redesign")
    day60 = []
    if staff_breach:
        day60.append("- **Workforce Demand Modeling:** Complete a shift-by-shift demand analysis using 6 months of volume data. Redesign schedules to match staffing to actual arrival patterns rather than historical averages.")
    if lwbs_breach or d2p_breach:
        day60.append("- **Fast-Track / Split-Flow Implementation:** Design and pilot a low-acuity fast-track pathway for ESI 4/5 patients. Target 60-minute door-to-discharge for this cohort to free main ED capacity.")
    if los_breach:
        day60.append("- **Discharge Process Redesign:** Implement anticipated discharge date (ADD) documentation in the EMR at time of admission. Require pharmacy, social work, and PT/OT to complete discharge tasks by noon.")
    if boarding_breach:
        day60.append("- **Inpatient Pull System:** Pilot a 'pull-until-full' model on two inpatient units, where the charge nurse pulls admitted patients from the ED proactively rather than waiting for a formal bed request.")
    if not day60:
        day60.append("- Benchmark against top-quartile peer facilities and identify 2–3 best practices for adoption.")
    for item in day60:
        report.append(item)

    report.append("\n### 🟢 Days 61–90: Sustain")
    day90 = []
    day90.append("- **KPI Dashboard Governance:** Formalize a bi-weekly KPI review cadence with department directors and the CNO/CMO. Establish accountability metrics tied to operational scorecards.")
    if staff_breach:
        day90.append("- **Retention Program Launch:** Engage HR to conduct stay interviews with high-risk staff. Design a targeted retention incentive (schedule flexibility, career laddering, or differential pay) based on findings.")
    if los_breach or boarding_breach:
        day90.append("- **Throughput Steering Committee:** Establish a permanent cross-functional throughput committee with authority to make real-time capacity decisions. Include ED, hospitalist, nursing, and case management leadership.")
    day90.append("- **30-Day Outcome Review:** Quantify the impact of Day 1–60 interventions against baseline KPIs. Present findings to the COO and Board Quality Committee with updated financial projections.")
    for item in day90:
        report.append(item)

    return "\n\n".join(report)


# ─────────────────────────────────────────────
# PDF GENERATOR
# Builds a polished executive-grade PDF using
# ReportLab Platypus (no wrapOn calls).
# ─────────────────────────────────────────────
def generate_executive_pdf(df: pd.DataFrame, alerts: list[dict], report_text: str) -> bytes:
    """
    Convert the consultant report text into a formatted PDF.
    Returns raw PDF bytes for st.download_button.
    """
    buf = io.BytesIO()

    # ── Page setup
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=1.0 * inch,
        bottomMargin=0.9 * inch,
        title="Synora Executive Intelligence Report",
        author="Synora — Executive Intelligence for Healthcare Operations",
    )

    # ── Color palette
    NAVY      = colors.HexColor("#0B172A")
    MIDBLUE   = colors.HexColor("#1E293B")
    LIGHTBLUE = colors.HexColor("#E0F2FE")
    AMBER     = colors.HexColor("#F59E0B")
    RED       = colors.HexColor("#DC2626")
    GREEN     = colors.HexColor("#10B981")
    GRAY      = colors.HexColor("#6B7280")
    LIGHTGRAY = colors.HexColor("#F3F4F6")
    WHITE     = colors.white

    # ── Style definitions
    styles = getSampleStyleSheet()

    cover_tag = ParagraphStyle("cover_tag",
        fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#A8C8E8"),
        spaceAfter=6, leading=12, alignment=TA_CENTER)

    cover_title = ParagraphStyle("cover_title",
        fontName="Helvetica-Bold", fontSize=26, textColor=WHITE,
        spaceAfter=10, leading=32, alignment=TA_CENTER)

    cover_sub = ParagraphStyle("cover_sub",
        fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#A8C8E8"),
        spaceAfter=4, leading=14, alignment=TA_CENTER)

    section_heading = ParagraphStyle("section_heading",
        fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
        spaceBefore=18, spaceAfter=8, leading=18,
        borderPad=4)

    sub_heading = ParagraphStyle("sub_heading",
        fontName="Helvetica-Bold", fontSize=11, textColor=MIDBLUE,
        spaceBefore=12, spaceAfter=4, leading=14)

    body_style = ParagraphStyle("body_style",
        fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#1F2937"),
        spaceAfter=7, leading=14, alignment=TA_LEFT)

    bullet_style = ParagraphStyle("bullet_style",
        fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#1F2937"),
        spaceAfter=5, leading=14, leftIndent=16,
        bulletIndent=4, bulletFontName="Helvetica",
        bulletFontSize=9.5)

    label_style = ParagraphStyle("label_style",
        fontName="Helvetica-Bold", fontSize=8, textColor=WHITE,
        spaceAfter=0, leading=10, alignment=TA_CENTER)

    kpi_label = ParagraphStyle("kpi_label",
        fontName="Helvetica", fontSize=8.5, textColor=GRAY,
        spaceAfter=0, leading=11)

    kpi_value = ParagraphStyle("kpi_value",
        fontName="Helvetica-Bold", fontSize=14, textColor=NAVY,
        spaceAfter=0, leading=16)

    footer_style = ParagraphStyle("footer_style",
        fontName="Helvetica", fontSize=7.5, textColor=GRAY,
        alignment=TA_CENTER, leading=10)

    # ── Compute KPIs for the summary table
    avgs = df.mean(numeric_only=True)
    date_range = f"{df['Date'].min().strftime('%b %Y')} – {df['Date'].max().strftime('%b %Y')}"

    def get(col, fmt=".1f"):
        v = avgs.get(col, 0)
        return format(v, fmt)

    # ── Helper: draw a colored horizontal rule
    def hr(color=MIDBLUE, thickness=0.5):
        return HRFlowable(width="100%", thickness=thickness,
                          color=color, spaceAfter=6, spaceBefore=2)

    # ── Helper: strip markdown bold markers for PDF body text
    import re
    def clean(text):
        return re.sub(r"\*\*(.+?)\*\*", r"\1", text)

    def bold_inline(text):
        return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

    # ══════════════════════════════════════════
    # BUILD FLOWABLES
    # ══════════════════════════════════════════
    story = []

    # ── COVER PAGE ──────────────────────────
    cover_data = [[
        Paragraph("CONFIDENTIAL · FOR EXECUTIVE USE ONLY", cover_tag),
    ]]
    cover_table = Table(cover_data, colWidths=[6.3 * inch])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",   (0, 0), (-1, -1), 48),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("LEFTPADDING",  (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [6, 6, 0, 0]),
    ]))
    story.append(cover_table)

    title_data = [[Paragraph("Synora<br/>Executive Intelligence Report", cover_title)]]
    title_table = Table(title_data, colWidths=[6.3 * inch])
    title_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), MIDBLUE),
        ("TOPPADDING",   (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 18),
        ("LEFTPADDING",  (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
    ]))
    story.append(title_table)

    sub_data = [[
        Paragraph("Prepared by: Synora — Executive Intelligence for Healthcare Operations", cover_sub),
        Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", cover_sub),
        Paragraph(f"Data Period: {date_range}", cover_sub),
        Paragraph(f"Reporting Periods Analyzed: {len(df)}", cover_sub),
    ]]
    sub_table = Table(sub_data, colWidths=[6.3 * inch])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), colors.HexColor("#0F2847")),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 28),
        ("LEFTPADDING",  (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("ROUNDEDCORNERS", (0, 0), (-1, -1), [0, 0, 6, 6]),
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 0.35 * inch))

    # ── KPI SNAPSHOT TABLE ──────────────────
    story.append(Paragraph("Key Performance Snapshot", section_heading))
    story.append(hr())

    kpi_rows = [
        ["KPI", "Average", "Benchmark", "Status"],
        ["ED Visits",          f"{get('ED_Visits', '.0f')} visits",  "—",        "—"],
        ["Length of Stay",     f"{get('LOS_Hours')} hrs",              "≤ 7.0 hrs",
         "⚠ BREACH" if avgs.get("LOS_Hours", 0) > 7   else "✓ OK"],
        ["Door-to-Provider",   f"{get('Door_to_Provider_Min', '.0f')} min", "≤ 35 min",
         "⚠ BREACH" if avgs.get("Door_to_Provider_Min", 0) > 35 else "✓ OK"],
        ["LWBS Rate",          f"{get('LWBS_Rate')}%",                 "≤ 4.0%",
         "⚠ BREACH" if avgs.get("LWBS_Rate", 0) > 4   else "✓ OK"],
        ["Boarding Hours",     f"{get('Boarding_Hours')} hrs",         "≤ 15.0 hrs",
         "⚠ BREACH" if avgs.get("Boarding_Hours", 0) > 15 else "✓ OK"],
        ["Staff Gap",          f"{get('Staff_Gap')} FTEs",             "≤ 5.0 FTEs",
         "⚠ BREACH" if avgs.get("Staff_Gap", 0) > 5   else "✓ OK"],
        ["Admission Rate",     f"{get('Admission_Rate')}%",            "—",        "—"],
    ]

    kpi_col_w = [2.2*inch, 1.4*inch, 1.4*inch, 1.3*inch]
    kpi_table = Table(kpi_rows, colWidths=kpi_col_w, repeatRows=1)
    kpi_style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 8.5),
        ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
        ("TOPPADDING",    (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8.5),
        ("TOPPADDING",    (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("ALIGN",         (1, 1), (-1, -1), "CENTER"),
        ("ALIGN",         (0, 1), (0, -1), "LEFT"),
        ("LEFTPADDING",   (0, 0), (0, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHTGRAY]),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [4, 4, 4, 4]),
    ])
    for i, row in enumerate(kpi_rows[1:], start=1):
        status = row[3]
        if "BREACH" in status:
            kpi_style.add("TEXTCOLOR",  (3, i), (3, i), RED)
            kpi_style.add("FONTNAME",   (3, i), (3, i), "Helvetica-Bold")
            kpi_style.add("BACKGROUND", (3, i), (3, i), colors.HexColor("#FEF2F2"))
        elif "OK" in status:
            kpi_style.add("TEXTCOLOR",  (3, i), (3, i), GREEN)
            kpi_style.add("FONTNAME",   (3, i), (3, i), "Helvetica-Bold")

    kpi_table.setStyle(kpi_style)
    story.append(kpi_table)
    story.append(Spacer(1, 0.2 * inch))

    # ── PARSE REPORT TEXT INTO SECTIONS ─────
    import re as _re
    raw_sections = _re.split(r"\n\n## ", report_text)
    parsed = []
    for i, sec in enumerate(raw_sections):
        if i == 0:
            sec = sec.lstrip("## ")
        lines = sec.strip().split("\n")
        title_line = lines[0].strip()
        body_lines = lines[1:]
        parsed.append({"title": title_line, "body": body_lines})

    # ── RENDER EACH REPORT SECTION ──────────
    for sec in parsed:
        title = sec["title"]
        hdr_data = [[Paragraph(title, section_heading)]]
        hdr_table = Table(hdr_data, colWidths=[6.3 * inch])
        hdr_table.setStyle(TableStyle([
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",   (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
            ("LINEBEFORE",   (0, 0), (0, -1), 3, MIDBLUE),
        ]))
        story.append(KeepTogether([hdr_table, hr()]))

        for line in sec["body"]:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 4))
                continue

            if line.startswith("### "):
                text = line[4:].strip()
                if "1–30" in text or "30" in text:
                    color = RED
                elif "31–60" in text or "60" in text:
                    color = AMBER
                else:
                    color = GREEN
                day_style = ParagraphStyle("day_heading",
                    fontName="Helvetica-Bold", fontSize=10.5,
                    textColor=color, spaceBefore=10, spaceAfter=4, leading=13)
                story.append(Paragraph(bold_inline(text), day_style))

            elif line.startswith("- ") or line.startswith("* "):
                text = bold_inline(line[2:].strip())
                story.append(Paragraph(f"• {text}", bullet_style))

            elif line.startswith("**Estimated Total"):
                story.append(Spacer(1, 4))
                total_style = ParagraphStyle("total",
                    fontName="Helvetica-Bold", fontSize=10,
                    textColor=NAVY, spaceAfter=6,
                    leading=14, borderPad=6,
                    backColor=LIGHTBLUE)
                story.append(Paragraph(clean(line), total_style))

            else:
                story.append(Paragraph(bold_inline(line), body_style))

        story.append(Spacer(1, 0.1 * inch))

    # ── FOOTER NOTE ─────────────────────────
    story.append(Spacer(1, 0.3 * inch))
    story.append(hr(color=colors.HexColor("#D1D5DB"), thickness=0.3))
    story.append(Paragraph(
        f"Synora  ·  Confidential — For Executive Use Only  ·  "
        f"Generated {datetime.now().strftime('%B %d, %Y')}  ·  "
        "Financial estimates are directional and should be validated against facility-specific data.",
        footer_style
    ))

    # ── BUILD PDF ───────────────────────────
    def on_page(canvas, doc):
        """Add page numbers to every page."""
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GRAY)
        page_num = canvas.getPageNumber()
        canvas.drawRightString(
            doc.pagesize[0] - 0.85 * inch,
            0.55 * inch,
            f"Page {page_num}"
        )
        canvas.drawString(
            0.85 * inch, 0.55 * inch,
            "CONFIDENTIAL · Synora"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    buf.seek(0)
    return buf.read()


def _markdown_to_report_html(text: str) -> str:
    """Convert basic report markdown to HTML with explicit contrast-safe colors."""
    lines = text.strip().split("\n")
    parts = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            parts.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            parts.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("- "):
            content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped[2:])
            parts.append(f"<p>• {content}</p>")
        else:
            content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            parts.append(f"<p>{content}</p>")
    return "\n".join(parts)


def render_consultant_report(df: pd.DataFrame, alerts: list[dict]):
    """Render the AI Consultant Report section with a generate button."""

    st.markdown('<div class="page-header"><h2 class="page-title">Reports</h2>'
                '<p class="page-subtitle">Generate and download Synora executive intelligence reports</p></div>',
                unsafe_allow_html=True)

    with st.container(border=True):
        col_desc, col_btn = st.columns([3, 1])
        with col_desc:
            st.markdown("**Executive Intelligence Report Generator**")
            st.markdown(
                "Synora analyzes your KPI data and produces a structured executive intelligence report for COO "
                "or Board Quality Committee review — including root cause analysis, financial impact "
                "estimates, and a 30-60-90 day action plan."
            )
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            generate = st.button("Generate Executive Report", type="primary", use_container_width=True)

    if generate:
        with st.spinner("Synora is analyzing your KPI data..."):
            import time
            time.sleep(1.2)
            report_text = generate_consultant_report(df, alerts)
            st.session_state.report_text = report_text

    report_text = st.session_state.get("report_text")
    if report_text:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0A1020,#141C2E);
                    border-radius:16px; padding:1.75rem 2.25rem; margin-bottom:1.75rem;
                    border:1px solid rgba(34,211,238,0.2); box-shadow:0 16px 40px rgba(0,0,0,0.25);">
            <div style="font-size:0.65rem; font-weight:700; letter-spacing:2px;
                        text-transform:uppercase; color:#22D3EE; margin-bottom:0.5rem;">
                Confidential · Executive Brief
            </div>
            <div style="font-family:'DM Sans',sans-serif; font-size:1.6rem; font-weight:700;
                        color:#F1F5F9; margin-bottom:0.3rem; letter-spacing:-0.03em;">
                Synora Executive Intelligence Report
            </div>
            <div style="font-size:0.82rem; color:#94A3B8;">
                Executive Intelligence for Healthcare Operations &nbsp;·&nbsp; {datetime.now().strftime("%B %d, %Y")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Render each section of the report
        sections = report_text.split("\n\n## ")
        first_section = sections[0]
        rest_sections = ["## " + s for s in sections[1:]]

        st.markdown(
            f'<div class="report-section">{_markdown_to_report_html(first_section)}</div>',
            unsafe_allow_html=True,
        )

        for section in rest_sections:
            st.markdown(
                f'<div class="report-section">{_markdown_to_report_html(section)}</div>',
                unsafe_allow_html=True,
            )

        # Generate and offer PDF download
        st.markdown("<br>", unsafe_allow_html=True)
        with st.spinner("Generating PDF..."):
            pdf_bytes = generate_executive_pdf(df, alerts, report_text)
        st.download_button(
            label="Download Executive PDF",
            data=pdf_bytes,
            file_name=f"synora_executive_intelligence_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            type="primary",
        )


# ─────────────────────────────────────────────
# SECTION 8: Portfolio Demo Mode
# ─────────────────────────────────────────────
def render_portfolio_demo():
    """Product overview for healthcare leaders and recruiters."""

    st.markdown('<div class="section-header">Platform Capabilities</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="platform-banner">
        <div style="font-size:0.65rem; font-weight:700; letter-spacing:2px; text-transform:uppercase;
                    color:#22D3EE; margin-bottom:0.6rem;">Built for Healthcare Operations Leaders</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:2rem; font-weight:700;
                    color:#F1F5F9; line-height:1.2; margin-bottom:0.35rem; letter-spacing:-0.03em;">
            Synora
        </div>
        <div style="font-size:0.85rem; font-weight:600; color:#22D3EE; margin-bottom:0.75rem; letter-spacing:0.02em;">
            Executive Intelligence for Healthcare Operations
        </div>
        <div style="font-size:0.92rem; color:#94A3B8; max-width:680px; line-height:1.65;">
            Transform healthcare data into executive action through AI-powered operational intelligence,
            predictive analytics, and executive decision support.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Who it's built for | Problem it solves
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("#### 🎯 Who It's Built For")
            st.markdown("""
**Primary Users**
- Chief Operating Officers and Chief Medical Officers
- VP of Operations and Emergency Department Medical Directors
- Healthcare management consultants conducting performance reviews
- Hospital Board Quality & Safety Committees

**Secondary Users**
- Performance improvement analysts
- Graduate healthcare administration students
- Healthcare IT and data teams piloting executive reporting tools
""")

    with col2:
        with st.container(border=True):
            st.markdown("#### ⚡ Problem It Solves")
            st.markdown("""
Hospital operations data is often trapped in EMR exports, spreadsheets, and fragmented department reports. Leadership teams spend hours manually compiling KPIs before they can begin analysis.

**Synora eliminates that delay.** Upload a single CSV and within seconds receive:
- Threshold-based clinical alerts
- Trend direction analysis across all KPIs
- A prioritized recommendation set
- A full consulting-grade narrative report
- A downloadable executive PDF — ready for the board room

**No BI team. No data warehouse. No wait.**
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Key Features (3 columns)
    st.markdown("""
    <div style="font-size:0.68rem; font-weight:700; letter-spacing:2px; text-transform:uppercase;
                color:#22D3EE; margin-bottom:1.25rem;">
        Key Capabilities
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)

    with fc1:
        with st.container(border=True):
            st.markdown("**📊 Automated KPI Analysis**")
            st.markdown("""
- 7 Emergency Department KPIs monitored simultaneously
- Configurable clinical thresholds per metric
- First-half vs. second-half trend detection
- Visual Plotly trend charts with threshold reference lines
- 7-metric summary card dashboard
""")

    with fc2:
        with st.container(border=True):
            st.markdown("**🚨 Intelligent Alert Engine**")
            st.markdown("""
- Critical vs. warning severity classification
- Threshold breach detection with clinical context
- Plain-language alert messaging for non-technical audiences
- Green / amber / red visual hierarchy
- Zero configuration required after CSV upload
""")

    with fc3:
        with st.container(border=True):
            st.markdown("**📄 Executive Report Generator**")
            st.markdown("""
- Rule-based COO-grade consulting narrative
- 6 structured report sections with clinical framing
- Directional financial impact estimates (LOS, LWBS, staffing)
- 30-60-90 day phased action plan
- Polished PDF download with cover page, KPI table, page numbers
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 3: Business Value / ROI
    with st.container(border=True):
        st.markdown("#### 💼 Business Value & ROI")
        bv1, bv2, bv3, bv4 = st.columns(4)

        metrics = [
            ("< 60 sec", "Time to insight after CSV upload"),
            ("$0", "BI infrastructure required"),
            ("6 sections", "Of structured analysis generated automatically"),
            ("~$200K+", "Typical monthly cost exposure surfaced per flagged facility"),
        ]
        for col, (val, label) in zip([bv1, bv2, bv3, bv4], metrics):
            with col:
                st.markdown(f"""
                <div class="platform-metric">
                    <div class="platform-metric-value">{val}</div>
                    <div class="platform-metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
Traditional healthcare performance consulting engagements cost **$50,000–$250,000** and take 4–8 weeks to deliver a report of this structure.
Synora produces an equivalent first-pass analysis in under a minute, enabling leadership teams to:

- **Prioritize** which performance gaps require immediate intervention
- **Quantify** the financial exposure before engaging an external consulting firm
- **Accelerate** board reporting cycles from weekly to real-time
- **Democratize** operational intelligence across health systems of any size
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 4: Future Roadmap
    with st.container(border=True):
        st.markdown("#### 🗺️ Future Roadmap")
        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown("""
**🔵 Near-Term (v2)**
- Hospital name & facility branding on PDF cover
- Multi-facility comparison mode
- National benchmark overlays (ACEP / CMS percentiles)
- Date range filtering and cohort slicing
- Automated email delivery of PDF report
""")
        with r2:
            st.markdown("""
**🟡 Mid-Term (v3)**
- LLM-powered narrative generation (GPT-4 / Claude)
- Real-time EMR data connector (Epic, Cerner via FHIR)
- Custom threshold configuration per facility
- Role-based access (COO view vs. department director view)
- Historical trend persistence across sessions
""")
        with r3:
            st.markdown("""
**🟢 Long-Term (v4)**
- Predictive KPI forecasting (LSTM / time-series models)
- Staffing optimization recommendations with shift modeling
- Integration with hospital ERP and workforce platforms
- Multi-site health system portfolio dashboard
- Regulatory compliance reporting (CMS, Joint Commission)
""")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tech stack & contact footer
    st.markdown("""
    <div class="tech-stack-bar">
        <div>
            <div style="font-size:0.65rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
                        color:#64748B; margin-bottom:0.4rem;">Tech Stack</div>
            <div style="font-size:0.85rem; color:#F1F5F9; font-weight:500;">
                Python 3.11 &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Pandas &nbsp;·&nbsp;
                Plotly &nbsp;·&nbsp; NumPy &nbsp;·&nbsp; ReportLab
            </div>
        </div>
        <div style="margin-top:1rem;">
            <div style="font-size:0.65rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
                        color:#64748B; margin-bottom:0.4rem;">Product</div>
            <div style="font-size:0.85rem; color:#F1F5F9; font-weight:500;">
                Synora — Executive Intelligence for Healthcare Operations
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# NAVIGATION & PAGE LAYOUT
# ═══════════════════════════════════════════════
def init_session_state():
    if "df" not in st.session_state:
        st.session_state.df = None
    if "alerts" not in st.session_state:
        st.session_state.alerts = []
    if "report_text" not in st.session_state:
        st.session_state.report_text = None


def render_hero():
    df = st.session_state.df
    stats_html = ""
    if df is not None:
        avgs = df.mean(numeric_only=True)
        alerts = len(st.session_state.alerts)
        stats_html = f"""
        <div class="synora-hero-stats">
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">{len(df)}</div>
                <div class="synora-hero-stat-label">Reporting Periods</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">{avgs.get('ED_Visits', 0):.0f}</div>
                <div class="synora-hero-stat-label">Avg ED Visits</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">{alerts}</div>
                <div class="synora-hero-stat-label">Active Alerts</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">{avgs.get('Admission_Rate', 0):.1f}%</div>
                <div class="synora-hero-stat-label">Admission Rate</div>
            </div>
        </div>
        """
    else:
        stats_html = """
        <div class="synora-hero-stats">
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">7</div>
                <div class="synora-hero-stat-label">KPIs Monitored</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">&lt;60s</div>
                <div class="synora-hero-stat-label">Time to Insight</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">6</div>
                <div class="synora-hero-stat-label">Report Sections</div>
            </div>
            <div class="synora-hero-stat">
                <div class="synora-hero-stat-value">PDF</div>
                <div class="synora-hero-stat-label">Executive Export</div>
            </div>
        </div>
        """

    st.markdown(f"""
    <div class="synora-hero">
        <div class="synora-hero-inner">
            <div class="synora-hero-badge">◆ Executive Intelligence</div>
            <h1 class="synora-hero-title">Synora</h1>
            <p class="synora-hero-subtitle">Executive Intelligence for Healthcare Operations</p>
            <p class="synora-hero-desc">
                Transform healthcare data into executive action through AI-powered operational intelligence,
                predictive analytics, and executive decision support.
            </p>
            {stats_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div class="synora-sidebar-brand">
            <div class="synora-logo-mark">◆</div>
            <p class="synora-logo">Syn<span>ora</span></p>
            <p class="synora-sidebar-tag">Executive Intelligence for Healthcare Operations</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="synora-nav-label">Navigation</p>', unsafe_allow_html=True)
        page = st.radio(
            "Navigation",
            NAV_PAGES,
            format_func=lambda p: f"{NAV_ICONS.get(p, '·')}  {p}",
            label_visibility="collapsed",
        )

        st.markdown("---")
        if st.session_state.df is not None:
            periods = len(st.session_state.df)
            st.markdown(f"""
            <div class="synora-sidebar-status">
                <span class="status-dot status-dot-live"></span>
                <span style="font-size:0.82rem;color:#F1F5F9;font-weight:600;">Dataset Active</span>
                <div style="font-size:0.75rem;color:#64748B;margin-top:0.35rem;">{periods} reporting periods loaded</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="synora-sidebar-status">
                <span class="status-dot status-dot-idle"></span>
                <span style="font-size:0.82rem;color:#94A3B8;">Awaiting data upload</span>
                <div style="font-size:0.72rem;color:#64748B;margin-top:0.35rem;">Upload a CSV to begin</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:0.68rem;color:#475569;margin-top:2rem;letter-spacing:0.5px;">Synora v1.0 · Enterprise</p>',
            unsafe_allow_html=True,
        )
    return page


def parse_uploaded_csv(uploaded_file) -> Optional[pd.DataFrame]:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        return None
    if "Date" not in df.columns:
        st.error("The uploaded CSV must contain a 'Date' column.")
        return None
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    if df.empty:
        st.error("No valid date rows found in the uploaded file.")
        return None
    return df


def load_dataset(uploaded_file):
    df = parse_uploaded_csv(uploaded_file)
    if df is not None:
        st.session_state.df = df
        st.session_state.alerts = detect_problems(df)
        st.session_state.report_text = None


def render_empty_state(message: str = "Upload a KPI dataset to unlock this view."):
    st.markdown(f"""
    <div class="empty-state">
        <p style="font-size:2rem;margin-bottom:0.75rem;opacity:0.8;">◉</p>
        <p><strong>No data loaded</strong></p>
        <p style="margin-top:0.5rem;">{message}</p>
        <p style="margin-top:1.25rem;font-size:0.85rem;color:#64748B;">
            Go to <strong style="color:#22D3EE;">Upload Data</strong> in the sidebar to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_synora_footer():
    st.markdown(
        f'<div class="synora-footer">Synora · Executive Intelligence for Healthcare Operations · '
        f'{datetime.now().strftime("%B %d, %Y")}</div>',
        unsafe_allow_html=True,
    )


def render_kpi_metrics(df: pd.DataFrame):
    avgs = df.mean(numeric_only=True)
    metric_items = [
        ("ED Visits", "ED_Visits", f"{avgs.get('ED_Visits', 0):.0f}", "visits / period"),
        ("Length of Stay", "LOS_Hours", f"{avgs.get('LOS_Hours', 0):.1f}", "hours"),
        ("Door-to-Provider", "Door_to_Provider_Min", f"{avgs.get('Door_to_Provider_Min', 0):.0f}", "minutes"),
        ("LWBS Rate", "LWBS_Rate", f"{avgs.get('LWBS_Rate', 0):.1f}", "%"),
        ("Boarding Hours", "Boarding_Hours", f"{avgs.get('Boarding_Hours', 0):.1f}", "hours"),
        ("Staff Gap", "Staff_Gap", f"{avgs.get('Staff_Gap', 0):.1f}", "FTEs"),
        ("Admission Rate", "Admission_Rate", f"{avgs.get('Admission_Rate', 0):.1f}", "%"),
    ]
    row1 = st.columns(4)
    for i, (label, col, val, unit) in enumerate(metric_items[:4]):
        cfg = next((c for n, c in KPI_CONFIG.items() if c["col"] == col), {})
        status_class, status_label = kpi_status_for_display(col, avgs.get(col, 0), cfg)
        with row1[i]:
            metric_card(label, val, unit, status_class, status_label)
    st.markdown("<br>", unsafe_allow_html=True)
    row2 = st.columns(4)
    for i, (label, col, val, unit) in enumerate(metric_items[4:]):
        cfg = next((c for n, c in KPI_CONFIG.items() if c["col"] == col), {})
        status_class, status_label = kpi_status_for_display(col, avgs.get(col, 0), cfg)
        with row2[i]:
            metric_card(label, val, unit, status_class, status_label)


def render_kpi_charts(df: pd.DataFrame):
    chart_items = [(name, cfg) for name, cfg in KPI_CONFIG.items() if cfg["col"] in df.columns]
    for i in range(0, len(chart_items), 2):
        cols = st.columns(2)
        for j, (name, cfg) in enumerate(chart_items[i:i + 2]):
            with cols[j]:
                fig = build_line_chart(
                    df, cfg["col"], name, cfg["unit"],
                    CHART_COLORS[(i + j) % len(CHART_COLORS)], cfg["threshold"],
                )
                st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)


def render_alerts_panel(alerts: list[dict]):
    if not alerts:
        st.markdown("""
        <div class="alert-success">
            <div class="alert-title" style="color:#34D399;">All KPIs Within Acceptable Thresholds</div>
            <div class="alert-body">
                No threshold violations detected. Continue monitoring and consider tightening benchmarks.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for alert in alerts:
            css_class = "alert-critical" if alert["level"] == "critical" else "alert-warning"
            title_color = "#F87171" if alert["level"] == "critical" else "#FBBF24"
            st.markdown(f"""
            <div class="{css_class}">
                <div class="alert-title" style="color:{title_color};">{alert['title']}</div>
                <div class="alert-body">{alert['msg']}</div>
            </div>
            """, unsafe_allow_html=True)


def render_financial_impact(df: pd.DataFrame, alerts: list[dict]):
    report_text = generate_consultant_report(df, alerts)
    sections = report_text.split("\n\n## ")
    fin_section = None
    for sec in sections:
        if sec.strip().startswith("5. Estimated Financial Impact") or "## 5." in sec:
            fin_section = sec if sec.startswith("##") else "## " + sec
            break
    if not fin_section:
        for sec in sections:
            if "Estimated Financial Impact" in sec:
                fin_section = "## " + sec if not sec.startswith("##") else sec
                break

    st.markdown('<div class="section-header">Financial Exposure Analysis</div>', unsafe_allow_html=True)
    if fin_section:
        st.markdown(
            f'<div class="report-section">{_markdown_to_report_html(fin_section)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No financial exposure detected for the current dataset.")

    action_section = None
    for sec in sections:
        if "30-60-90" in sec or sec.strip().startswith("6."):
            action_section = sec if sec.startswith("##") else "## " + sec
            break
    if action_section:
        st.markdown('<div class="section-header">30-60-90 Day Action Plan</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="report-section">{_markdown_to_report_html(action_section)}</div>',
            unsafe_allow_html=True,
        )


def render_page_overview():
    render_hero()
    df = st.session_state.df
    if df is not None:
        alerts = st.session_state.alerts
        st.markdown('<div class="section-header">Executive Snapshot</div>', unsafe_allow_html=True)
        avgs = df.mean(numeric_only=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="fin-card"><div class="fin-value">{len(df)}</div>'
                        '<div class="fin-label">Reporting Periods</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="fin-card"><div class="fin-value">{avgs.get("ED_Visits", 0):.0f}</div>'
                        '<div class="fin-label">Avg ED Visits</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="fin-card"><div class="fin-value">{len(alerts)}</div>'
                        '<div class="fin-label">Active Alerts</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="fin-card"><div class="fin-value">{avgs.get("Admission_Rate", 0):.1f}%</div>'
                        '<div class="fin-label">Admission Rate</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Operational Status</div>', unsafe_allow_html=True)
        render_alerts_panel(alerts)
    render_portfolio_demo()


def render_page_upload():
    st.markdown('<div class="page-header"><h2 class="page-title">Upload Data</h2>'
                '<p class="page-subtitle">Import healthcare operations data to power Synora executive intelligence</p></div>',
                unsafe_allow_html=True)

    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)

    col_upload, col_sample = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload your hospital KPI CSV file",
            type=["csv"],
            help="CSV must include a 'Date' column plus one or more KPI columns.",
            label_visibility="collapsed",
        )
    with col_sample:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Sample CSV",
            data=generate_sample_csv(),
            file_name="sample_hospital_kpi.csv",
            mime="text/csv",
            help="Download a pre-filled sample to explore Synora.",
            use_container_width=True,
        )

    if uploaded_file is not None:
        load_dataset(uploaded_file)
        st.success(f"Dataset loaded — {len(st.session_state.df)} reporting periods ready for analysis.")
    elif st.session_state.df is None:
        st.markdown("""
        <div class="upload-zone">
            <div class="upload-icon">↑</div>
            <div class="upload-title">Drop your KPI CSV here or use the uploader above</div>
            <div class="upload-hint">
                Synora accepts weekly or monthly hospital operations data with a Date column
            </div>
            <div class="upload-columns">
                <span class="upload-col-tag">Date</span>
                <span class="upload-col-tag">ED_Visits</span>
                <span class="upload-col-tag">LOS_Hours</span>
                <span class="upload-col-tag">Door_to_Provider_Min</span>
                <span class="upload-col-tag">LWBS_Rate</span>
                <span class="upload-col-tag">Boarding_Hours</span>
                <span class="upload-col-tag">Staff_Gap</span>
                <span class="upload-col-tag">Admission_Rate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.df is not None:
        with st.expander("Preview raw data", expanded=False):
            st.dataframe(st.session_state.df, use_container_width=True)


def render_page_ed_operations(df: pd.DataFrame, alerts: list[dict]):
    st.markdown('<div class="page-header"><h2 class="page-title">ED Operations</h2>'
                '<p class="page-subtitle">Real-time KPI monitoring, trends, and clinical alerts</p></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    render_kpi_metrics(df)
    st.markdown('<div class="section-header">Trend Analysis</div>', unsafe_allow_html=True)
    render_kpi_charts(df)
    st.markdown('<div class="section-header">Clinical Alerts</div>', unsafe_allow_html=True)
    render_alerts_panel(alerts)


def render_page_ai_advisor(df: pd.DataFrame, alerts: list[dict]):
    st.markdown('<div class="page-header"><h2 class="page-title">AI Advisor</h2>'
                '<p class="page-subtitle">Synora executive intelligence summary and prioritized recommendations</p></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    render_executive_summary(df, alerts)
    st.markdown('<div class="section-header">Operational Recommendations</div>', unsafe_allow_html=True)
    render_recommendations(df, alerts)


def render_page_financial_impact(df: pd.DataFrame, alerts: list[dict]):
    st.markdown('<div class="page-header"><h2 class="page-title">Financial Impact</h2>'
                '<p class="page-subtitle">Directional cost exposure and revenue impact estimates</p></div>',
                unsafe_allow_html=True)
    render_financial_impact(df, alerts)


def render_page_reports(df: pd.DataFrame, alerts: list[dict]):
    render_consultant_report(df, alerts)


# ═══════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════
def main():
    init_session_state()
    page = render_sidebar()

    if page == "Overview":
        render_page_overview()
    elif page == "Upload Data":
        render_page_upload()
    else:
        if st.session_state.df is None:
            render_hero()
            render_empty_state()
        else:
            df = st.session_state.df
            alerts = st.session_state.alerts
            if page == "ED Operations":
                render_page_ed_operations(df, alerts)
            elif page == "Financial Impact":
                render_page_financial_impact(df, alerts)
            elif page == "AI Advisor":
                render_page_ai_advisor(df, alerts)
            elif page == "Reports":
                render_page_reports(df, alerts)

    render_synora_footer()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
