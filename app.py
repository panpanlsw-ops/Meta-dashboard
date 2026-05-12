import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meta Ads Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    .main { background-color: #f0f2f6; }
    .block-container { padding: 1.5rem 2rem; }

    /* Header bar */
    .meta-header {
        background: linear-gradient(90deg, #1877F2, #0d5bd1);
        padding: 14px 24px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(24,119,242,0.3);
    }
    .meta-header h1 { color: white; margin: 0; font-size: 1.6rem; font-weight: 700; }
    .meta-header span { color: #bfdbfe; font-size: 0.9rem; margin-left: 16px; }

    /* Section titles */
    .section-title {
        background: #1877F2;
        color: white;
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0;
        display: inline-block;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #1877F2;
        height: 100%;
        transition: box-shadow 0.2s;
    }
    .kpi-card:hover { box-shadow: 0 4px 16px rgba(24,119,242,0.15); }
    .kpi-label { color: #6b7280; font-size: 0.78rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { color: #111827; font-size: 1.6rem; font-weight: 800; margin: 4px 0; }
    .kpi-delta-pos { color: #10b981; font-size: 0.82rem; font-weight: 600; }
    .kpi-delta-neg { color: #ef4444; font-size: 0.82rem; font-weight: 600; }
    .kpi-delta-neu { color: #6b7280; font-size: 0.82rem; }

    /* Chart containers */
    .chart-container {
        background: white;
        border-radius: 0 12px 12px 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }

    /* Table */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1a1a2e;
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stFileUploader label { color: #94a3b8 !important; font-size: 0.8rem; }

    /* Upload area */
    .upload-box {
        border: 2px dashed #1877F2;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        background: #eff6ff;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

META_BLUE    = "#1877F2"
CHART_COLORS = ["#1877F2","#10b981","#f59e0b","#8b5cf6","#ef4444","#06b6d4","#f97316"]

@st.cache_data
def load_excel(file) -> dict:
    xls = pd.ExcelFile(file)
    sheets = {}
    for name in xls.sheet_names:
        sheets[name] = pd.read_excel(xls, sheet_name=name)
    return sheets

def fmt_number(n):
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.1f}"

def delta_html(val, positive_is_good=True):
    if pd.isna(val): return ""
    arrow = "▲" if val > 0 else "▼"
    if positive_is_good:
        cls = "kpi-delta-pos" if val > 0 else "kpi-delta-neg"
    else:
        cls = "kpi-delta-neg" if val > 0 else "kpi-delta-pos"
    return f'<span class="{cls}">{arrow} {abs(val):.1f}%</span>'

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📊 Meta Ads Dashboard")
    st.markdown("---")

    st.markdown("### 📁 Data Source")
    uploaded = st.file_uploader(
        "Upload your Excel file",
        type=["xlsx", "xls"],
        help="Upload a .xlsx file with your Meta Ads data"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Filters")

    # Load data
    if uploaded:
        data = load_excel(uploaded)
        st.success(f"✅ Loaded: {uploaded.name}")
    else:
        try:
            data = load_excel("meta_ads_data.xlsx")
            st.info("📋 Using sample data")
        except Exception as e:
            st.error("No data found. Please upload an Excel file.")
            st.stop()

    # Sheet selector
    sheet_names = list(data.keys())

    # Date filter (for Daily Performance)
    if "Daily Performance" in data:
        daily_df = data["Daily Performance"].copy()
        daily_df["Date"] = pd.to_datetime(daily_df["Date"])
        min_d, max_d = daily_df["Date"].min(), daily_df["Date"].max()
        date_range = st.date_input(
            "Date Range",
            value=(min_d.date(), max_d.date()),
            min_value=min_d.date(),
            max_value=max_d.date(),
        )
    else:
        date_range = None

    # Campaign filter
    if "Campaign Performance" in data:
        camp_df = data["Campaign Performance"]
        objectives = ["All"] + list(camp_df["Campaign Objective"].unique())
        selected_obj = st.selectbox("Campaign Objective", objectives)
    else:
        selected_obj = "All"

    st.markdown("---")
    st.markdown("### 📥 Download")
    if "Daily Performance" in data:
        csv = data["Daily Performance"].to_csv(index=False).encode()
        st.download_button("Download Daily Data (CSV)", csv, "meta_daily.csv", "text/csv")

    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="meta-header">
    <span style="font-size:2rem;margin-right:12px;">🔵</span>
    <div>
        <h1>Meta Ads Dashboard</h1>
    </div>
    <span style="margin-left:auto; color:#bfdbfe; font-size:0.9rem;">Overview &nbsp;|&nbsp; Dec 2024</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS (Overview sheet)
# ─────────────────────────────────────────────────────────────────────────────

if "Overview" in data:
    overview = data["Overview"].set_index("Metric")

    st.markdown('<span class="section-title">📈 Performances</span>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container" style="border-radius:0 12px 12px 12px;">', unsafe_allow_html=True)

    # icon, metric key, format, positive_is_good
    KPI_CONFIG = [
        ("💸", "Spend ($)",        "currency", False),
        ("🖱️", "Clicks",           "number",   True),
        ("🔄", "Conversions",      "number",   True),
        ("👥", "CRM Leads",        "number",   True),
        ("📅", "Appointments",     "number",   True),
        ("🤝", "Customers",        "number",   True),
        ("💰", "Sales Amount ($)", "currency", True),
    ]

    def fmt_value(val, fmt):
        if fmt == "currency":
            if abs(val) >= 1_000_000: return f"${val/1_000_000:.1f}M"
            if abs(val) >= 1_000:     return f"${val/1_000:.1f}K"
            return f"${val:,.0f}"
        else:
            return fmt_number(val)

    cols = st.columns(len(KPI_CONFIG))
    for col, (icon, metric, fmt, pg) in zip(cols, KPI_CONFIG):
        if metric not in overview.index:
            with col:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">{icon} {metric}</div>
                    <div class="kpi-value" style="color:#9ca3af;">—</div>
                    <span class="kpi-delta-neu">No data</span>
                </div>
                """, unsafe_allow_html=True)
            continue
        row   = overview.loc[metric]
        cur   = row["Current Period"]
        chg   = row["Change %"]
        d_html = delta_html(chg, pg)
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{icon} {metric}</div>
                <div class="kpi-value">{fmt_value(cur, fmt)}</div>
                {d_html}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BUDGET DISTRIBUTION PIE + CAMPAIGN TABLE
# ─────────────────────────────────────────────────────────────────────────────

if "Campaign Performance" in data:
    camp_df = data["Campaign Performance"].copy()
    if selected_obj != "All":
        filtered_camp = camp_df[camp_df["Campaign Objective"] == selected_obj]
    else:
        filtered_camp = camp_df

    col_pie, col_table = st.columns([1, 2])

    with col_pie:
        st.markdown('<span class="section-title">💰 Budget Distribution</span>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        pie_fig = px.pie(
            camp_df,
            values="Spend ($)",
            names="Campaign Objective",
            color_discrete_sequence=CHART_COLORS,
            hole=0.35,
        )
        pie_fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>Spend: $%{value:,.0f}<br>Share: %{percent}<extra></extra>"
        )
        pie_fig.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            legend=dict(font=dict(size=11), orientation="v"),
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_table:
        st.markdown('<span class="section-title">📋 Performances by Campaign Objectives</span>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        display_cols = ["Campaign Objective", "Spend ($)", "Impressions", "CPM ($)",
                        "Clicks", "CPC ($)", "Leads", "Purchases", "ROAS"]
        tbl = filtered_camp[display_cols].copy()
        tbl["Spend ($)"] = tbl["Spend ($)"].apply(lambda x: f"${x:,.0f}")
        tbl["Impressions"] = tbl["Impressions"].apply(lambda x: fmt_number(x))
        tbl["CPM ($)"] = tbl["CPM ($)"].apply(lambda x: f"${x:.2f}")
        tbl["Clicks"] = tbl["Clicks"].apply(lambda x: fmt_number(x))
        tbl["CPC ($)"] = tbl["CPC ($)"].apply(lambda x: f"${x:.2f}")
        tbl["ROAS"] = tbl["ROAS"].apply(lambda x: f"{x:.1f}" if x > 0 else "-")
        tbl["Leads"] = tbl["Leads"].apply(lambda x: fmt_number(x) if x > 0 else "-")
        tbl["Purchases"] = tbl["Purchases"].apply(lambda x: fmt_number(x) if x > 0 else "-")

        st.dataframe(tbl, use_container_width=True, hide_index=True, height=280)
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DAILY TREND CHARTS
# ─────────────────────────────────────────────────────────────────────────────

if "Daily Performance" in data:
    daily = data["Daily Performance"].copy()
    daily["Date"] = pd.to_datetime(daily["Date"])

    if date_range and len(date_range) == 2:
        start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        daily = daily[(daily["Date"] >= start) & (daily["Date"] <= end)]

    st.markdown('<span class="section-title">📅 Daily Performance Trends</span>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    metric_choice = st.selectbox(
        "Select Metric",
        ["Spend ($)", "Impressions", "Clicks", "Leads", "Purchases", "ROAS", "Reach"],
        key="trend_metric"
    )

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily[metric_choice],
        mode="lines+markers",
        name=metric_choice,
        line=dict(color=META_BLUE, width=2.5),
        marker=dict(size=5, color=META_BLUE),
        fill="tozeroy",
        fillcolor="rgba(24,119,242,0.08)",
        hovertemplate=f"<b>%{{x|%b %d}}</b><br>{metric_choice}: %{{y:,.1f}}<extra></extra>"
    ))

    # 7-day rolling avg
    daily_sorted = daily.sort_values("Date")
    rolling = daily_sorted[metric_choice].rolling(7, min_periods=1).mean()
    fig_trend.add_trace(go.Scatter(
        x=daily_sorted["Date"],
        y=rolling,
        mode="lines",
        name="7-day avg",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        hovertemplate="<b>7d avg</b>: %{y:,.1f}<extra></extra>"
    ))

    fig_trend.update_layout(
        height=320,
        margin=dict(t=10, b=40, l=60, r=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=False, tickformat="%b %d"),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Spend vs ROAS dual axis
    st.markdown('<span class="section-title">💹 Spend vs ROAS</span>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(
        x=daily["Date"], y=daily["Spend ($)"],
        name="Spend ($)", marker_color="rgba(24,119,242,0.7)",
        hovertemplate="Spend: $%{y:,.0f}<extra></extra>"
    ), secondary_y=False)
    fig2.add_trace(go.Scatter(
        x=daily["Date"], y=daily["ROAS"],
        name="ROAS", line=dict(color="#10b981", width=2.5),
        marker=dict(size=4),
        hovertemplate="ROAS: %{y:.2f}<extra></extra>"
    ), secondary_y=True)

    fig2.update_layout(
        height=300,
        margin=dict(t=10, b=40, l=60, r=60),
        plot_bgcolor="white",
        paper_bgcolor="white",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
    )
    fig2.update_yaxes(title_text="Spend ($)", secondary_y=False, showgrid=True, gridcolor="#f3f4f6")
    fig2.update_yaxes(title_text="ROAS", secondary_y=True, showgrid=False)
    fig2.update_xaxes(showgrid=False, tickformat="%b %d")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# AD SET PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────

if "Ad Set Performance" in data:
    adset_df = data["Ad Set Performance"].copy()

    col_bar, col_scatter = st.columns(2)

    with col_bar:
        st.markdown('<span class="section-title">🎯 Top Ad Sets by Spend</span>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        top10 = adset_df.nlargest(8, "Spend ($)")
        fig_bar = px.bar(
            top10.sort_values("Spend ($)"),
            x="Spend ($)", y="Ad Set Name",
            orientation="h",
            color="ROAS",
            color_continuous_scale=[[0, "#ef4444"],[0.5, "#f59e0b"],[1, "#10b981"]],
            text="Spend ($)",
        )
        fig_bar.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Spend: $%{x:,.0f}<extra></extra>"
        )
        fig_bar.update_layout(
            height=320, margin=dict(t=10, b=10, l=10, r=60),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
            yaxis=dict(showgrid=False),
            coloraxis_colorbar=dict(title="ROAS", thickness=12),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_scatter:
        st.markdown('<span class="section-title">🔍 Clicks vs Leads by Ad Set</span>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        scatter_df = adset_df[adset_df["Leads"] > 0].copy()
        fig_sc = px.scatter(
            scatter_df,
            x="Clicks", y="Leads",
            size="Spend ($)",
            color="Campaign",
            hover_name="Ad Set Name",
            color_discrete_sequence=CHART_COLORS,
            size_max=40,
        )
        fig_sc.update_layout(
            height=320, margin=dict(t=10, b=40, l=60, r=20),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
            yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
            legend=dict(font=dict(size=10)),
        )
        st.plotly_chart(fig_sc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Full table
    st.markdown('<span class="section-title">📊 Ad Set Full Report</span>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    display_adset = adset_df.copy()
    display_adset["Spend ($)"] = display_adset["Spend ($)"].apply(lambda x: f"${x:,.0f}")
    display_adset["Impressions"] = display_adset["Impressions"].apply(lambda x: fmt_number(x))
    display_adset["CTR (%)"] = display_adset["CTR (%)"].apply(lambda x: f"{x:.2f}%")
    display_adset["CPC ($)"] = display_adset["CPC ($)"].apply(lambda x: f"${x:.2f}")
    display_adset["ROAS"] = display_adset["ROAS"].apply(lambda x: f"{x:.1f}" if x > 0 else "-")
    display_adset["Leads"] = display_adset["Leads"].apply(lambda x: f"{x:,.0f}" if x > 0 else "-")
    display_adset["Purchases"] = display_adset["Purchases"].apply(lambda x: f"{x:,.0f}" if x > 0 else "-")

    st.dataframe(display_adset, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption("📊 Meta Ads Dashboard")
with col_f2:
    st.caption("Data refreshed from Excel upload")
with col_f3:
    st.caption("Built with Streamlit + Plotly")
