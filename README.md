# AI Healthcare Performance Improvement Platform

A hospital executive intelligence dashboard that transforms Emergency Department (ED) KPI data into operational insights, threshold-based alerts, prioritized recommendations, and a boardroom-ready consulting report — in under 60 seconds.

Built with Python and Streamlit as a portfolio-grade demonstration of healthcare operations analytics and executive reporting.

---

## Project Overview

Hospital leadership teams routinely rely on fragmented spreadsheets, EMR exports, and manual reports to monitor performance. This platform provides a single, streamlined workflow: upload a CSV of hospital KPIs and receive an executive-grade analysis without requiring a BI team, data warehouse, or external consulting engagement.

The application monitors seven core ED and throughput metrics, detects clinical threshold breaches, summarizes trends, generates prioritized operational recommendations, and produces a structured consulting narrative with downloadable PDF export.

> **Note:** The "AI Consultant Report" uses rule-based analytics and templated clinical narratives derived from KPI thresholds and trend logic. It is designed to mirror the structure and language of healthcare operations consulting deliverables.

---

## Problem Statement

Healthcare operations leaders — COOs, CMOs, ED medical directors, and performance improvement teams — face recurring challenges:

- **Data fragmentation:** KPIs live across EMR exports, department spreadsheets, and ad hoc reports with no unified view.
- **Analysis delay:** Manual compilation of metrics can take hours or days before meaningful review can begin.
- **Threshold blind spots:** Critical breaches (e.g., elevated LWBS, prolonged boarding) may not surface until periodic reviews.
- **Reporting overhead:** Board-quality operational narratives and action plans typically require expensive, weeks-long consulting engagements.
- **Resource constraints:** Smaller health systems lack dedicated analytics infrastructure to support real-time executive decision-making.

This platform addresses these gaps by automating first-pass KPI analysis, alert generation, and executive reporting from a single CSV upload.

---

## Features

### Data Ingestion
- CSV upload with date validation and expandable raw data preview
- Downloadable sample dataset for immediate exploration
- Support for weekly or periodic reporting intervals

### KPI Dashboard
- Seven monitored metrics: ED Visits, Length of Stay, Door-to-Provider Time, LWBS Rate, Boarding Hours, Staff Gap, Admission Rate
- Executive metric cards with period averages
- Interactive Plotly trend charts with clinical threshold reference lines

### Intelligent Alert Engine
- Critical and warning severity classification based on configurable clinical thresholds
- Plain-language alert messaging suitable for non-technical executive audiences
- Visual red / amber / green hierarchy for at-a-glance risk assessment

### Executive Summary
- Narrative overview of reporting period performance
- First-half vs. second-half trend detection (improving vs. worsening KPIs)
- Operational risk inventory and areas performing within target

### Operational Recommendations
- Priority-tagged recommendation cards (High / Medium / Sustain)
- Evidence-based interventions mapped to specific KPI breaches (discharge planning, triage redesign, workforce optimization, throughput initiatives)

### AI Consultant Report
- Six-section consulting deliverable structured for COO and Board Quality Committee presentation:
  1. Executive Summary
  2. Key Performance Issues
  3. Likely Root Causes
  4. Operational Impact
  5. Estimated Financial Impact
  6. 30-60-90 Day Action Plan
- Downloadable executive PDF with cover page, KPI snapshot table, and page numbering

### Portfolio Demo Mode
- Product overview documenting target users, business value, tech stack, and roadmap for recruiters and healthcare stakeholders

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| PDF Generation | ReportLab |
| Deployment Config | Streamlit `config.toml` (headless, port 8000) |

### Expected CSV Schema

| Column | Description |
|--------|-------------|
| `Date` | Reporting period date (required) |
| `ED_Visits` | Emergency Department visit volume |
| `LOS_Hours` | Average length of stay (hours) |
| `Door_to_Provider_Min` | Door-to-provider time (minutes) |
| `LWBS_Rate` | Left-without-being-seen rate (%) |
| `Boarding_Hours` | ED boarding duration (hours) |
| `Staff_Gap` | Staffing deficit (FTEs) |
| `Admission_Rate` | ED admission rate (%) |

### Clinical Thresholds (Default)

| KPI | Benchmark |
|-----|-----------|
| Length of Stay | ≤ 7.0 hours |
| LWBS Rate | ≤ 4.0% |
| Boarding Hours | ≤ 15.0 hours |
| Staff Gap | ≤ 5.0 FTEs |
| Door-to-Provider | ≤ 35 minutes (reporting only) |

---

## How to Run Locally

### Prerequisites

- Python 3.11 or later
- pip

### Installation

```bash
# Clone or navigate to the project directory
cd "PI Project"

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
pip install reportlab           # Required for PDF export (used by app.py)
```

### Start the Application

```bash
streamlit run app.py
```

The app opens in your default browser. With the included `config.toml`, the server listens on **port 8000** at `http://localhost:8501` (Streamlit default) or `http://localhost:8000` depending on configuration.

To specify port explicitly:

```bash
streamlit run app.py --server.port=8000
```

### Quick Start

1. Launch the app with `streamlit run app.py`
2. Click **Download Sample CSV** to obtain test data, or upload your own KPI file
3. Review Sections 2–6 for dashboard metrics, alerts, summary, and recommendations
4. Click **Generate AI Consultant Report** for the full narrative and PDF download

### Project Files

| File | Description |
|------|-------------|
| `app.py` | Primary application entry point (full feature set) |
| `healthcare_dashboard.py` | Earlier version with core dashboard features (Sections 1–6) |
| `config.toml` | Streamlit server and theme configuration |
| `requirements.txt` | Core Python dependencies |

---

## Future Roadmap

### Near-Term (v2)
- Hospital name and facility branding on PDF cover page
- Multi-facility comparison mode
- National benchmark overlays (ACEP / CMS percentiles)
- Date range filtering and cohort slicing
- Automated email delivery of PDF reports

### Mid-Term (v3)
- LLM-powered narrative generation (GPT-4 / Claude) with rule-based fallback
- Real-time EMR data connector (Epic, Cerner via FHIR)
- Custom threshold configuration per facility
- Role-based access (COO view vs. department director view)
- Historical trend persistence across sessions

### Long-Term (v4)
- Predictive KPI forecasting (time-series models)
- Staffing optimization recommendations with shift modeling
- Integration with hospital ERP and workforce platforms
- Multi-site health system portfolio dashboard
- Regulatory compliance reporting (CMS, Joint Commission)

---

## Potential Healthcare Use Cases

### Hospital Executive Leadership
- **COO / VP Operations:** Weekly ED throughput review with financial impact estimates before board meetings
- **CMO / CNO:** Cross-functional performance briefings with prioritized intervention plans
- **ED Medical Director:** Trend monitoring for LWBS, door-to-provider, and boarding metrics

### Performance Improvement & Quality
- **PI Analysts:** Rapid first-pass analysis of exported EMR KPI data without building custom dashboards
- **Quality & Safety Committees:** Structured reporting aligned with clinical threshold benchmarks
- **Lean / Six Sigma teams:** Baseline assessment before process redesign initiatives

### Healthcare Consulting & Administration
- **Management consultants:** Accelerate engagement kickoff with automated KPI triage and draft report generation
- **Graduate healthcare administration programs:** Teaching tool for operations analytics and executive communication
- **Regional health systems:** Portfolio-level comparison across facilities (planned v2 feature)

### Financial & Strategic Planning
- **Revenue cycle teams:** Quantify LWBS-related revenue leakage and LOS-driven capacity constraints
- **Workforce planning:** Surface staffing gap trends to inform float pool and agency contract decisions
- **Board reporting:** Produce confidential executive PDFs for Quality Committee presentations

---

## Disclaimer

This platform is intended for **operational analytics and demonstration purposes**. Financial impact estimates are directional and based on industry-standard benchmarks — they should be validated against facility-specific payer mix, cost structures, and volume data before use in formal decision-making. This tool does not constitute medical advice and is not a substitute for licensed clinical or financial consulting.

---

## License

Portfolio project — contact the author for usage terms.
