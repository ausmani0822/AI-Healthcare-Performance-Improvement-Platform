"""
AI Healthcare Performance Improvement Platform
A hospital executive dashboard for KPI analysis and AI-driven insights.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import io

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Healthcare Performance Improvement Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Clean hospital executive styling
# Deep navy + clinical white + alert amber/red
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & Typography ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background-color: #F0F4F8;
}

/* ── Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, #0A2342 0%, #1B4F8A 60%, #1A6BAE 100%);
    padding: 2.5rem 3rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.header-subtitle {
    font-size: 0.95rem;
    color: #A8C8E8;
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.2px;
}
.header-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #D0E8FF;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.9rem;
}

/* ── Section Headers ── */
.section-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #1B4F8A;
    border-left: 3px solid #1B4F8A;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* ── Metric Cards ── */
.metric-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.4rem 1.2rem;
    border: 1px solid #E2EAF4;
    box-shadow: 0 1px 4px rgba(10,35,66,0.06);
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1B4F8A, #1A6BAE);
    border-radius: 10px 10px 0 0;
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #6B88A8;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0A2342;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.metric-unit {
    font-size: 0.78rem;
    color: #8BA8C0;
    font-weight: 400;
}

/* ── Alert Cards ── */
.alert-critical {
    background: #FFF5F5;
    border: 1px solid #FECACA;
    border-left: 4px solid #DC2626;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.alert-warning {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid #D97706;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.alert-success {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 4px solid #16A34A;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.alert-title {
    font-weight: 600;
    font-size: 0.88rem;
    margin-bottom: 0.2rem;
}
.alert-body {
    font-size: 0.82rem;
    color: #4B5563;
}

/* ── Summary & Recommendation Cards ── */
.summary-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    border: 1px solid #E2EAF4;
    box-shadow: 0 1px 4px rgba(10,35,66,0.06);
    margin-bottom: 1rem;
}
.rec-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #E2EAF4;
    border-left: 4px solid #1B4F8A;
    box-shadow: 0 1px 4px rgba(10,35,66,0.06);
    margin-bottom: 0.85rem;
}
.rec-priority-high {
    border-left-color: #DC2626;
}
.rec-priority-med {
    border-left-color: #D97706;
}
.rec-priority-low {
    border-left-color: #16A34A;
}
.rec-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #0A2342;
    margin-bottom: 0.3rem;
}
.rec-body {
    font-size: 0.82rem;
    color: #4B5563;
    line-height: 1.5;
}
.priority-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 20px;
    margin-bottom: 0.5rem;
}
.badge-high { background: #FEE2E2; color: #DC2626; }
.badge-med  { background: #FEF3C7; color: #D97706; }
.badge-low  { background: #DCFCE7; color: #16A34A; }

/* ── Upload Zone ── */
.upload-zone {
    background: #FFFFFF;
    border: 2px dashed #C5D8EE;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: border-color 0.2s;
}
.upload-hint {
    font-size: 0.8rem;
    color: #6B88A8;
    margin-top: 0.5rem;
}

/* ── Sample Data Button ── */
.stDownloadButton > button {
    background: #0A2342 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.25rem !important;
}

/* ── Chart Container ── */
.chart-container {
    background: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #E2EAF4;
    box-shadow: 0 1px 4px rgba(10,35,66,0.06);
    padding: 1rem;
    margin-bottom: 1rem;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, #1B4F8A22, #1B4F8A44, #1B4F8A22);
    margin: 1.5rem 0;
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

# Chart accent colors (clinical palette)
CHART_COLORS = [
    "#1B4F8A", "#1A6BAE", "#2E8BC0", "#D97706",
    "#DC2626", "#16A34A", "#7C3AED"
]


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
def metric_card(label: str, value: str, unit: str):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPER: Build a styled Plotly line chart
# ─────────────────────────────────────────────
def build_line_chart(df: pd.DataFrame, col: str, label: str, unit: str,
                     color: str, threshold: float | None) -> go.Figure:
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
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=11, color="#4B5563"),
        title=dict(text=label, font=dict(size=13, color="#0A2342", family="Inter"), x=0.02),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F4F8",
            tickfont=dict(size=9),
            title=unit,
            titlefont=dict(size=9),
        ),
        legend=dict(orientation="h", y=-0.25, font=dict(size=9)),
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

    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.markdown("**Overview**")
    st.markdown(
        f"Analysis of the uploaded KPI dataset covering **{len(df)} reporting periods** "
        f"identified **{risk_label}** against established clinical thresholds. "
        f"The ED processed an average of **{avgs.get('ED_Visits', 0):.0f} visits per period** "
        f"with a mean admission rate of **{avgs.get('Admission_Rate', 0):.1f}%**."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown("**Major Trends**")
        if worsening:
            st.markdown(f"📈 **Worsening:** {', '.join(worsening)} trended higher in the latter portion of the reporting period.")
        if improving:
            st.markdown(f"📉 **Improving:** {', '.join(improving)} showed measurable improvement over time.")
        if not worsening and not improving:
            st.markdown("Metrics remained relatively stable across the reporting period with no pronounced directional trends.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown("**Operational Risks**")
        if alerts:
            for a in alerts:
                icon = "🔴" if a["level"] == "critical" else "🟡"
                st.markdown(f"{icon} {a['title'].replace('⚠ ', '')}")
        else:
            st.markdown("✅ No KPIs exceeded defined thresholds during this period.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Areas performing well
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.markdown("**Areas Performing Well**")
    well = []
    if "LOS_Hours" in avgs and avgs["LOS_Hours"] <= 7.0:
        well.append(f"Length of Stay ({avgs['LOS_Hours']:.1f} hrs) is within target")
    if "LWBS_Rate" in avgs and avgs["LWBS_Rate"] <= 4.0:
        well.append(f"LWBS Rate ({avgs['LWBS_Rate']:.1f}%) is within acceptable range")
    if "Staff_Gap" in avgs and avgs["Staff_Gap"] <= 5.0:
        well.append(f"Staffing Gap ({avgs['Staff_Gap']:.1f} FTEs) is manageable")
    if "Boarding_Hours" in avgs and avgs["Boarding_Hours"] <= 15.0:
        well.append(f"Boarding Hours ({avgs['Boarding_Hours']:.1f} hrs) remain below threshold")
    if well:
        for w in well:
            st.markdown(f"✅ {w}")
    else:
        st.markdown("All monitored KPIs require attention in the current period.")
    st.markdown("</div>", unsafe_allow_html=True)


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


# ═══════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════
def main():

    # ── Header Banner ──────────────────────────
    st.markdown("""
    <div class="header-banner">
        <div class="header-tag">Executive Dashboard · AI-Powered</div>
        <div class="header-title">AI Healthcare Performance<br>Improvement Platform</div>
        <div class="header-subtitle">
            Upload hospital KPI data and receive AI-driven operational insights and recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 1: File Upload
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 1 — Data Upload</div>', unsafe_allow_html=True)

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
            label="⬇ Download Sample CSV",
            data=generate_sample_csv(),
            file_name="sample_hospital_kpi.csv",
            mime="text/csv",
            help="Download a pre-filled sample to explore the dashboard.",
        )

    # ── Upload hint when no file present
    if uploaded_file is None:
        st.markdown("""
        <div class="upload-zone">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📂</div>
            <div style="font-weight:600; color:#1B4F8A; font-size:0.9rem;">
                Drag and drop your CSV file above, or click to browse
            </div>
            <div class="upload-hint">
                Expected columns: Date, ED_Visits, LOS_Hours, Door_to_Provider_Min,
                LWBS_Rate, Boarding_Hours, Staff_Gap, Admission_Rate
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()  # Nothing to display until a file is uploaded

    # ── Parse the uploaded file
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

    # Validate the Date column
    if "Date" not in df.columns:
        st.error("The uploaded CSV must contain a 'Date' column.")
        st.stop()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    if df.empty:
        st.error("No valid date rows found in the uploaded file.")
        st.stop()

    # ── Data preview (collapsed)
    with st.expander("🔍 Preview raw data", expanded=False):
        st.dataframe(df, use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 2: Key Metric Cards
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 2 — Key Performance Indicators</div>', unsafe_allow_html=True)

    avgs = df.mean(numeric_only=True)

    # Display 4 cards per row
    metric_items = [
        ("Avg ED Visits",         f"{avgs.get('ED_Visits', 0):.0f}",            "visits / period"),
        ("Avg Length of Stay",    f"{avgs.get('LOS_Hours', 0):.1f}",             "hours"),
        ("Avg Door-to-Provider",  f"{avgs.get('Door_to_Provider_Min', 0):.0f}",  "minutes"),
        ("Avg LWBS Rate",         f"{avgs.get('LWBS_Rate', 0):.1f}",             "%"),
        ("Avg Boarding Hours",    f"{avgs.get('Boarding_Hours', 0):.1f}",         "hours"),
        ("Avg Staff Gap",         f"{avgs.get('Staff_Gap', 0):.1f}",             "FTEs"),
        ("Avg Admission Rate",    f"{avgs.get('Admission_Rate', 0):.1f}",         "%"),
    ]

    # Row 1: 4 cards
    row1 = st.columns(4)
    for i, (label, val, unit) in enumerate(metric_items[:4]):
        with row1[i]:
            metric_card(label, val, unit)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: 3 cards (left-aligned)
    row2 = st.columns(4)
    for i, (label, val, unit) in enumerate(metric_items[4:]):
        with row2[i]:
            metric_card(label, val, unit)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 3: KPI Trend Charts
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 3 — KPI Trends Over Time</div>', unsafe_allow_html=True)

    # Render charts in 2-column grid
    chart_items = [(name, cfg) for name, cfg in KPI_CONFIG.items() if cfg["col"] in df.columns]

    for i in range(0, len(chart_items), 2):
        cols = st.columns(2)
        for j, (name, cfg) in enumerate(chart_items[i:i+2]):
            with cols[j]:
                fig = build_line_chart(
                    df, cfg["col"], name, cfg["unit"],
                    CHART_COLORS[i + j], cfg["threshold"]
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 4: Problem Area Detection
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 4 — Problem Area Detection</div>', unsafe_allow_html=True)

    alerts = detect_problems(df)

    if not alerts:
        st.markdown("""
        <div class="alert-success">
            <div class="alert-title" style="color:#15803D;">✅ All KPIs Within Acceptable Thresholds</div>
            <div class="alert-body">
                No threshold violations detected in the uploaded dataset.
                Continue monitoring and consider tightening benchmarks.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for alert in alerts:
            css_class = "alert-critical" if alert["level"] == "critical" else "alert-warning"
            title_color = "#991B1B" if alert["level"] == "critical" else "#92400E"
            st.markdown(f"""
            <div class="{css_class}">
                <div class="alert-title" style="color:{title_color};">{alert['title']}</div>
                <div class="alert-body">{alert['msg']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 5: Executive Summary
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 5 — Executive Summary</div>', unsafe_allow_html=True)
    render_executive_summary(df, alerts)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SECTION 6: Recommendations
    # ─────────────────────────────────────────
    st.markdown('<div class="section-header">Section 6 — Operational Recommendations</div>', unsafe_allow_html=True)
    render_recommendations(df, alerts)

    # ── Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center; font-size:0.72rem; color:#9EB3C8; padding-bottom:1.5rem;'>"
        "AI Healthcare Performance Improvement Platform · For executive use only · "
        f"Report generated {datetime.now().strftime('%B %d, %Y')}"
        "</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
