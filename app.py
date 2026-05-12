import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64, os

st.set_page_config(page_title="Meta Ads Dashboard", page_icon="📊", layout="wide")

# ── Logos ──────────────────────────────────────────────────────────────────────
def img_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

_ls = img_b64("lifesource_logo.png")
LIFESOURCE_IMG = (
    f'<img src="data:image/png;base64,{_ls}" height="24" style="object-fit:contain;vertical-align:middle">' 
    if _ls else '<span style="font-size:1rem;font-weight:700;color:#cc2200">LifeSource</span>'
)

META_LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" height="18" style="vertical-align:middle">
  <path d="M8 25C8 16.2 13.5 9 21 9c4 0 7.5 2.2 10.5 6.2C34.5 11.2 38 9 42 9
    c7.5 0 13 7.2 13 16 0 4.4-1.4 8.4-3.8 11.3-2.2 2.6-4.8 4-7.7 4
    -3.8 0-6.5-1.8-10.5-7.4-4 5.6-6.7 7.4-10.5 7.4-2.9 0-5.5-1.4-7.7-4
    C9.4 33.4 8 29.4 8 25zm13-10.2C15.2 14.8 11 19.4 11 25s4.2 10.2 10 10.2
    c2.8 0 5-1.5 8-6.3-3.1-5.2-5.2-7.9-8-7.9zm21 0c-2.8 0-4.9 2.7-8 7.9
    3 4.8 5.2 6.3 8 6.3 5.8 0 10-4.6 10-10.2s-4.2-10.2-10-10.2z" fill="white"/>
  <text x="62" y="36" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="white">Meta</text>
</svg>"""

META_LOGO_BLUE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" height="24" style="vertical-align:middle">
  <path d="M8 25C8 16.2 13.5 9 21 9c4 0 7.5 2.2 10.5 6.2C34.5 11.2 38 9 42 9
    c7.5 0 13 7.2 13 16 0 4.4-1.4 8.4-3.8 11.3-2.2 2.6-4.8 4-7.7 4
    -3.8 0-6.5-1.8-10.5-7.4-4 5.6-6.7 7.4-10.5 7.4-2.9 0-5.5-1.4-7.7-4
    C9.4 33.4 8 29.4 8 25zm13-10.2C15.2 14.8 11 19.4 11 25s4.2 10.2 10 10.2
    c2.8 0 5-1.5 8-6.3-3.1-5.2-5.2-7.9-8-7.9zm21 0c-2.8 0-4.9 2.7-8 7.9
    3 4.8 5.2 6.3 8 6.3 5.8 0 10-4.6 10-10.2s-4.2-10.2-10-10.2z" fill="#0082FB"/>
  <text x="62" y="36" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="#0082FB">Meta</text>
</svg>"""

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main{background:#f4f6fb}
  .block-container{padding:0.5rem 1.2rem}
  header[data-testid="stHeader"]{display:none}
  #MainMenu{visibility:hidden}
  footer{visibility:hidden}
  section[data-testid="stSidebar"]{background:#1a1e3c}
  section[data-testid="stSidebar"] *{color:#e2e8f0!important}
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stDateInput label{color:#7c8ab0!important;font-size:0.78rem!important}
  section[data-testid="stSidebar"] .stMarkdown p{color:#7c8ab0!important;font-size:0.72rem!important;
    text-transform:uppercase;letter-spacing:0.06em}

  .sec-hdr{background:#1877F2;color:white;padding:5px 12px;border-radius:6px 6px 0 0;
    font-weight:600;font-size:0.78rem;display:flex;align-items:center;gap:5px}
  .sec-body{background:white;border:1px solid #e5e7eb;border-top:none;
    border-radius:0 0 6px 6px;padding:10px;margin-bottom:10px}

  .kpi-strip{display:flex;gap:0;background:white;border:1px solid #e5e7eb;
    border-radius:8px;overflow:hidden;margin-bottom:5px}
  .kpi-cell{flex:1;padding:8px 12px 7px;border-right:1px solid #e5e7eb;position:relative}
  .kpi-cell:last-child{border-right:none}
  .kpi-cell::after{content:'';position:absolute;top:0;left:0;right:0;height:3px}
  .kpi-c1::after{background:#1877F2}.kpi-c2::after{background:#8b5cf6}
  .kpi-c3::after{background:#10b981}.kpi-c4::after{background:#f59e0b}
  .kpi-c5::after{background:#06b6d4}.kpi-c6::after{background:#ec4899}
  .kpi-c7::after{background:#22c55e}
  .kpi-lbl{font-size:0.62rem;color:#9ca3af;font-weight:600;text-transform:uppercase;
    letter-spacing:0.07em;margin-bottom:2px}
  .kpi-val{font-size:1.1rem;font-weight:700;color:#111827;margin-bottom:1px;line-height:1.1}
  .kpi-pos{font-size:0.68rem;color:#10b981;font-weight:600}
  .kpi-neg{font-size:0.68rem;color:#ef4444;font-weight:600}

  .terr-strip{display:flex;gap:0;background:white;border:1px solid #e5e7eb;
    border-radius:8px;overflow:hidden;margin-bottom:10px}
  .terr-cell{flex:1;padding:10px 10px 8px;border-right:1px solid #e5e7eb;text-align:center}
  .terr-cell:last-child{border-right:none}
  .terr-top{display:block;height:3px;border-radius:2px;margin-bottom:6px}
  .terr-lbl{font-size:0.62rem;color:#9ca3af;font-weight:600;text-transform:uppercase;
    letter-spacing:0.07em;margin-bottom:3px}
  .terr-val{font-size:1.2rem;font-weight:700;color:#111827}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
META   = "#1877F2"
COLORS = ["#1877F2","#10b981","#f59e0b","#8b5cf6","#ef4444",
          "#06b6d4","#f97316","#ec4899","#22c55e","#a78bfa",
          "#fb923c","#34d399","#60a5fa"]

def fmt_num(n):
    if pd.isna(n): return "—"
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"

def fmt_cur(n):
    if pd.isna(n) or n == 0: return "$0"
    if abs(n) >= 1_000_000: return f"${n/1_000_000:.1f}M"
    if abs(n) >= 1_000:     return f"${n/1_000:.1f}K"
    return f"${n:,.0f}"

def delta_html(v, pos_good=True):
    if pd.isna(v): return ""
    arrow = "▲" if v > 0 else "▼"
    cls = ("kpi-pos" if v > 0 else "kpi-neg") if pos_good else ("kpi-neg" if v > 0 else "kpi-pos")
    return f'<span class="{cls}">{arrow} {abs(v):.1f}%</span>'

@st.cache_data
def load(file):
    xls = pd.ExcelFile(file)
    return {n: pd.read_excel(xls, sheet_name=n) for n in xls.sheet_names}

def chart_layout(fig, h=260):
    fig.update_layout(height=h, margin=dict(t=10, b=40, l=60, r=20),
                      paper_bgcolor="white", plot_bgcolor="white",
                      xaxis=dict(showgrid=False, tickformat="%b %d"),
                      yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1),
                      hovermode="x unified")
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:10px 8px 8px;border-bottom:1px solid rgba(255,255,255,0.08);
                display:flex;flex-direction:column;align-items:center;gap:5px">
      <div style="display:flex;align-items:center;justify-content:center">
        {LIFESOURCE_IMG}
      </div>
      <div style="display:flex;align-items:center;gap:6px;padding:5px 10px;
                  background:rgba(255,255,255,0.06);border-radius:6px">
        {META_LOGO_SVG}
      </div>
      <div style="font-size:0.72rem;color:#6b7db0;letter-spacing:0.06em;text-transform:uppercase">
        Ads Dashboard
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    uploaded = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

    try:
        data = load(uploaded) if uploaded else load("meta_ads_data.xlsx")
        st.success(f"✅ {uploaded.name}") if uploaded else st.info("📋 Sample data")
    except Exception:
        st.error("Upload an Excel file to begin.")
        st.stop()

    st.markdown("---")
    st.markdown("**NAVIGATION**")
    tab_sel = st.radio("", ["📊 MTD Overview", "📈 Trends", "🗺️ By Territory"],
                       label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**FILTERS**")

    camp_list = ["All Campaigns"]
    if "Campaign Performance" in data:
        camp_list += list(data["Campaign Performance"]["Campaign Objective"].unique())
    sel_camp = st.selectbox("Campaign", camp_list)

    offices = ["All"]
    if "Territory Performance" in data:
        offices += sorted(data["Territory Performance"]["Territory"].unique().tolist())
    sel_office = st.selectbox("Office / Territory", offices)

    date_range = None
    if "Daily Performance" in data:
        daily_raw = data["Daily Performance"].copy()
        daily_raw["Date"] = pd.to_datetime(daily_raw["Date"])
        mn, mx = daily_raw["Date"].min().date(), daily_raw["Date"].max().date()
        date_range = st.date_input("Date range (Trends)", value=(mn, mx),
                                   min_value=mn, max_value=mx)

    st.markdown("---")
    if "Daily Performance" in data:
        csv = data["Daily Performance"].to_csv(index=False).encode()
        st.download_button("⬇ Export Daily CSV", csv, "meta_daily.csv", "text/csv")

# ── Page header ───────────────────────────────────────────────────────────────
titles = {
    "📊 MTD Overview": "MTD Overview",
    "📈 Trends":       "Metric Trends",
    "🗺️ By Territory": "Performance by Territory",
}
st.markdown(f"""
<div style="background:#1877F2;padding:8px 16px;border-radius:8px;margin-bottom:10px;
            display:flex;align-items:center;justify-content:space-between">
  <div style="display:flex;align-items:center;gap:14px">
    {META_LOGO_BLUE_SVG.replace("fill=\"#0082FB\"","fill=\"white\"").replace("fill=\"#0082FB\"","fill=\"white\"")}
    <div style="width:1px;height:28px;background:rgba(255,255,255,0.3)"></div>
    <span style="color:white;font-size:1.1rem;font-weight:700">
      {titles[tab_sel]}</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <span style="color:#bfdbfe;font-size:0.8rem">Dec 2024</span>
    <div style="background:white;border-radius:6px;padding:3px 10px;display:flex;align-items:center">
      {LIFESOURCE_IMG.replace('height="24"','height="24"')}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MTD OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if tab_sel == "📊 MTD Overview":

    # KPI rows: Row1 = Spend · Clicks · Conversions · CRM Leads
    #           Row2 = Appointments · Customers · Sales Amount
    if "Overview" in data:
        ov = data["Overview"].set_index("Metric")

        def kpi_cell(metric, cls, is_cur=False, pos_good=True):
            if metric not in ov.index:
                return (f'<div class="kpi-cell {cls}">'
                        f'<div class="kpi-lbl">{metric}</div>'
                        f'<div class="kpi-val">—</div></div>')
            row  = ov.loc[metric]
            cur  = row["Current Period"]
            chg  = row["Change %"]
            fval = fmt_cur(cur) if is_cur else fmt_num(cur)
            return (f'<div class="kpi-cell {cls}">'
                    f'<div class="kpi-lbl">{metric}</div>'
                    f'<div class="kpi-val">{fval}</div>'
                    f'{delta_html(chg, pos_good)}</div>')

        st.markdown(
            '<div class="kpi-strip">'
            + kpi_cell("Spend ($)",    "kpi-c1", True,  False)
            + kpi_cell("Clicks",       "kpi-c2", False, True)
            + kpi_cell("Conversions",  "kpi-c3", False, True)
            + kpi_cell("CRM Leads",    "kpi-c4", False, True)
            + '</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="kpi-strip">'
            + kpi_cell("Appointments",     "kpi-c5", False, True)
            + kpi_cell("Customers",        "kpi-c6", False, True)
            + kpi_cell("Sales Amount ($)", "kpi-c7", True,  True)
            + '</div>', unsafe_allow_html=True)

    # Campaign pill selector
    if "Campaign Performance" in data:
        camp_df = data["Campaign Performance"].copy()
        all_camps = list(camp_df["Campaign Objective"].unique())

        if "t1_camp" not in st.session_state:
            st.session_state.t1_camp = "All Campaigns"

        btn_cols = st.columns(len(all_camps) + 1)
        for i, label in enumerate(["All Campaigns"] + all_camps):
            if btn_cols[i].button(label, key=f"t1_{i}", use_container_width=True,
                                  type="primary" if st.session_state.t1_camp == label else "secondary"):
                st.session_state.t1_camp = label

        sel = st.session_state.t1_camp
        fcamp = camp_df if sel == "All Campaigns" else camp_df[camp_df["Campaign Objective"] == sel]

        # Distribution charts
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="sec-hdr">💸 Spend by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            fig = px.pie(camp_df, values="Spend ($)", names="Campaign Objective",
                         hole=0.42, color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside", textinfo="percent",
                              hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
            fig.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=0),
                              paper_bgcolor="white", showlegend=True,
                              legend=dict(font=dict(size=9), orientation="v"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="sec-hdr">👥 CRM Leads by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            ld = camp_df[camp_df["CRM Leads"] > 0].sort_values("CRM Leads")
            fig2 = px.bar(ld, x="CRM Leads", y="Campaign Objective", orientation="h",
                          color="Campaign Objective", color_discrete_sequence=COLORS, text="CRM Leads")
            fig2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            fig2.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=50),
                               showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
                               xaxis=dict(showgrid=False, visible=False),
                               yaxis=dict(showgrid=False))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="sec-hdr">💰 Sales by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            sd = camp_df[camp_df["Sales Amount ($)"] > 0].sort_values("Sales Amount ($)")
            fig3 = px.bar(sd, x="Sales Amount ($)", y="Campaign Objective", orientation="h",
                          color="Campaign Objective", color_discrete_sequence=COLORS,
                          text="Sales Amount ($)")
            fig3.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig3.update_layout(height=180, margin=dict(t=0, b=0, l=0, r=70),
                               showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
                               xaxis=dict(showgrid=False, visible=False),
                               yaxis=dict(showgrid=False))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Campaign breakdown table
        st.markdown(f'<div class="sec-hdr">📋 Campaign Breakdown — {sel}</div>'
                    '<div class="sec-body">', unsafe_allow_html=True)

        cols_show = ["Campaign Objective", "Spend ($)", "Impressions", "Clicks",
                     "CRM Leads", "Conversions", "Appointments", "Customers",
                     "Sales Amount ($)", "ROAS"]
        tbl = fcamp[[c for c in cols_show if c in fcamp.columns]].copy()
        tbl["Spend ($)"]        = tbl["Spend ($)"].apply(fmt_cur)
        tbl["Impressions"]      = tbl["Impressions"].apply(fmt_num)
        tbl["Clicks"]           = tbl["Clicks"].apply(fmt_num)
        tbl["CRM Leads"]        = tbl["CRM Leads"].apply(lambda x: fmt_num(x) if x > 0 else "—")
        tbl["Conversions"]      = tbl["Conversions"].apply(lambda x: fmt_num(x) if x > 0 else "—")
        tbl["Appointments"]     = tbl["Appointments"].apply(fmt_num)
        tbl["Customers"]        = tbl["Customers"].apply(lambda x: fmt_num(x) if x > 0 else "—")
        tbl["Sales Amount ($)"] = tbl["Sales Amount ($)"].apply(lambda x: fmt_cur(x) if x > 0 else "—")
        tbl["ROAS"]             = tbl["ROAS"].apply(lambda x: f"{x:.1f}x" if x > 0 else "—")
        st.dataframe(tbl, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif tab_sel == "📈 Trends":

    if "Daily Performance" not in data:
        st.warning("No 'Daily Performance' sheet found.")
        st.stop()

    daily = data["Daily Performance"].copy()
    daily["Date"] = pd.to_datetime(daily["Date"])

    if date_range and len(date_range) == 2:
        daily = daily[(daily["Date"] >= pd.Timestamp(date_range[0])) &
                      (daily["Date"] <= pd.Timestamp(date_range[1]))]
    if sel_camp != "All Campaigns" and "Campaign" in daily.columns:
        daily = daily[daily["Campaign"] == sel_camp]

    agg = daily.groupby("Date").agg({
        "Spend ($)": "sum", "Impressions": "sum", "Reach": "sum",
        "Clicks": "sum", "CRM Leads": "sum", "Conversions": "sum",
        "Appointments": "sum", "Customers": "sum",
        "Sales Amount ($)": "sum", "ROAS": "mean"
    }).reset_index()

    gran = st.radio("Granularity", ["Daily", "Weekly", "Monthly"], horizontal=True)
    if gran == "Weekly":
        agg = agg.resample("W", on="Date").sum().reset_index()
    elif gran == "Monthly":
        agg = agg.resample("ME", on="Date").sum().reset_index()

    # Metric toggles
    st.markdown("**Select metrics to overlay:**")
    metric_opts = ["Spend ($)", "Sales Amount ($)", "CRM Leads", "Clicks",
                   "Conversions", "Appointments", "Customers", "ROAS"]
    defaults    = [True, True, True, False, False, False, False, False]
    mc = st.columns(8)
    sel_metrics = [m for i, (m, d) in enumerate(zip(metric_opts, defaults))
                   if mc[i].checkbox(m.replace(" ($)", ""), value=d, key=f"m{i}")]

    if sel_metrics:
        st.markdown('<div class="sec-hdr">📈 Selected Metrics Over Time</div>'
                    '<div class="sec-body">', unsafe_allow_html=True)
        fig_main = go.Figure()
        for m, col in zip(sel_metrics, COLORS):
            if m not in agg.columns: continue
            fig_main.add_trace(go.Scatter(
                x=agg["Date"], y=agg[m], name=m, mode="lines+markers",
                line=dict(color=col, width=2), marker=dict(size=4),
                hovertemplate=f"<b>%{{x|%b %d}}</b><br>{m}: %{{y:,.1f}}<extra></extra>"))
        chart_layout(fig_main, 300)
        st.plotly_chart(fig_main, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Select at least one metric above.")

    # ROAS + Spend vs Sales
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="sec-hdr">💹 ROAS / ROI Trend</div><div class="sec-body">', unsafe_allow_html=True)
        fig_r = go.Figure(go.Scatter(
            x=agg["Date"], y=agg["ROAS"], mode="lines+markers",
            line=dict(color="#22c55e", width=2.5),
            fill="tozeroy", fillcolor="rgba(34,197,94,0.08)",
            hovertemplate="<b>%{x|%b %d}</b><br>ROAS: %{y:.2f}x<extra></extra>"))
        fig_r.update_layout(height=180, margin=dict(t=10, b=30, l=50, r=10),
                            paper_bgcolor="white", plot_bgcolor="white",
                            xaxis=dict(showgrid=False, tickformat="%b %d"),
                            yaxis=dict(showgrid=True, gridcolor="#f3f4f6", ticksuffix="x"))
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="sec-hdr">💸 Spend vs Sales Amount</div><div class="sec-body">', unsafe_allow_html=True)
        fig_sv = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sv.add_trace(go.Bar(x=agg["Date"], y=agg["Spend ($)"], name="Spend",
                                marker_color="rgba(24,119,242,0.7)",
                                hovertemplate="Spend: $%{y:,.0f}<extra></extra>"), secondary_y=False)
        fig_sv.add_trace(go.Scatter(x=agg["Date"], y=agg["Sales Amount ($)"], name="Sales",
                                    line=dict(color="#22c55e", width=2.5),
                                    hovertemplate="Sales: $%{y:,.0f}<extra></extra>"), secondary_y=True)
        fig_sv.update_layout(height=180, margin=dict(t=10, b=30, l=50, r=50),
                             paper_bgcolor="white", plot_bgcolor="white",
                             legend=dict(orientation="h", y=1.08),
                             hovermode="x unified",
                             xaxis=dict(showgrid=False, tickformat="%b %d"))
        fig_sv.update_yaxes(showgrid=True, gridcolor="#f3f4f6", secondary_y=False)
        fig_sv.update_yaxes(showgrid=False, secondary_y=True)
        st.plotly_chart(fig_sv, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Acquisition + Funnel
    a1, a2 = st.columns(2)
    with a1:
        st.markdown('<div class="sec-hdr">📡 Acquisition — Impressions & Reach</div>'
                    '<div class="sec-body">', unsafe_allow_html=True)
        fig_acq = go.Figure()
        fig_acq.add_trace(go.Scatter(x=agg["Date"], y=agg["Impressions"], name="Impressions",
                                     line=dict(color=META, width=2),
                                     hovertemplate="Impr: %{y:,.0f}<extra></extra>"))
        fig_acq.add_trace(go.Scatter(x=agg["Date"], y=agg["Reach"], name="Reach",
                                     line=dict(color="#8b5cf6", width=2, dash="dash"),
                                     hovertemplate="Reach: %{y:,.0f}<extra></extra>"))
        chart_layout(fig_acq, 200)
        st.plotly_chart(fig_acq, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown('<div class="sec-hdr">🎯 Conversion Funnel Trend</div><div class="sec-body">', unsafe_allow_html=True)
        fig_cv = go.Figure()
        for m, col in [("Conversions","#10b981"),("Appointments","#06b6d4"),("Customers","#ec4899")]:
            fig_cv.add_trace(go.Scatter(x=agg["Date"], y=agg[m], name=m,
                                        line=dict(color=col, width=2),
                                        hovertemplate=f"{m}: %{{y:,.0f}}<extra></extra>"))
        chart_layout(fig_cv, 200)
        st.plotly_chart(fig_cv, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Clicks + Leads bars
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="sec-hdr">🖱️ Clicks Over Time</div><div class="sec-body">', unsafe_allow_html=True)
        fig_cl = go.Figure(go.Bar(x=agg["Date"], y=agg["Clicks"],
                                  marker_color="rgba(139,92,246,0.75)",
                                  hovertemplate="Clicks: %{y:,.0f}<extra></extra>"))
        fig_cl.update_layout(height=170, margin=dict(t=10, b=30, l=60, r=10),
                             paper_bgcolor="white", plot_bgcolor="white",
                             xaxis=dict(showgrid=False, tickformat="%b %d"),
                             yaxis=dict(showgrid=True, gridcolor="#f3f4f6"))
        st.plotly_chart(fig_cl, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="sec-hdr">👥 CRM Leads Over Time</div><div class="sec-body">', unsafe_allow_html=True)
        fig_ld = go.Figure(go.Bar(x=agg["Date"], y=agg["CRM Leads"],
                                  marker_color="rgba(245,158,11,0.75)",
                                  hovertemplate="Leads: %{y:,.0f}<extra></extra>"))
        fig_ld.update_layout(height=170, margin=dict(t=10, b=30, l=60, r=10),
                             paper_bgcolor="white", plot_bgcolor="white",
                             xaxis=dict(showgrid=False, tickformat="%b %d"),
                             yaxis=dict(showgrid=True, gridcolor="#f3f4f6"))
        st.plotly_chart(fig_ld, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BY TERRITORY
# ══════════════════════════════════════════════════════════════════════════════
elif tab_sel == "🗺️ By Territory":

    if "Territory Performance" not in data:
        st.warning("No 'Territory Performance' sheet found.")
        st.stop()

    terr_raw = data["Territory Performance"].copy()

    # Campaign filter specific to this tab
    t3_camps = ["All Campaigns"] + sorted(terr_raw["Campaign"].unique().tolist())
    sel_t3   = st.selectbox("Filter by Campaign", t3_camps, key="t3camp")
    tdf      = terr_raw if sel_t3 == "All Campaigns" else terr_raw[terr_raw["Campaign"] == sel_t3]

    # Aggregate by territory
    terr = tdf.groupby("Territory").agg({
        "Unique Leads": "sum", "New Leads": "sum", "Appointments": "sum",
        "Quote": "sum", "Customers": "sum", "Sales Amount ($)": "sum",
        "NL Customers": "sum", "NL Sales ($)": "sum", "Spend ($)": "sum",
        "ROAS": "mean",
    }).reset_index()

    total = terr.sum(numeric_only=True)
    terr["Leads %"]     = (terr["Unique Leads"]    / total["Unique Leads"]      * 100).round(2)
    terr["Sales %"]     = (terr["Sales Amount ($)"] / total["Sales Amount ($)"]  * 100).round(2)
    terr["APT/Leads"]   = (terr["Appointments"]     / terr["Unique Leads"].replace(0, 1) * 100).round(2)
    terr["Order/APT"]   = (terr["Customers"]        / terr["Appointments"].replace(0, 1) * 100).round(2)
    terr["Order/Leads"] = (terr["Customers"]        / terr["Unique Leads"].replace(0, 1) * 100).round(2)
    terr = terr.sort_values("Sales Amount ($)", ascending=False)

    # ── KPI strip (5 cells, matching screenshot style) ─────────────────────
    tot_ul  = int(total["Unique Leads"])
    tot_apt = int(total["Appointments"])
    tot_cu  = int(total["Customers"])
    tot_sal = total["Sales Amount ($)"]
    apt_pct = round(tot_apt / tot_ul * 100) if tot_ul else 0

    st.markdown(f"""
    <div class="terr-strip">
      <div class="terr-cell">
        <span class="terr-top" style="background:#1877F2"></span>
        <div class="terr-lbl">Total Leads</div>
        <div class="terr-val">{tot_ul:,}</div>
      </div>
      <div class="terr-cell">
        <span class="terr-top" style="background:#10b981"></span>
        <div class="terr-lbl">Appointments</div>
        <div class="terr-val">{tot_apt:,}</div>
      </div>
      <div class="terr-cell">
        <span class="terr-top" style="background:#8b5cf6"></span>
        <div class="terr-lbl">Customers</div>
        <div class="terr-val">{tot_cu:,}</div>
      </div>
      <div class="terr-cell">
        <span class="terr-top" style="background:#22c55e"></span>
        <div class="terr-lbl">Total Sales</div>
        <div class="terr-val">{fmt_cur(tot_sal)}</div>
      </div>
      <div class="terr-cell">
        <span class="terr-top" style="background:#f59e0b"></span>
        <div class="terr-lbl">APT / Leads</div>
        <div class="terr-val">{apt_pct}%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Donut charts: Leads % + Sales % (matching screenshot layout) ────────
    st.markdown('<div class="sec-hdr">🥧 Distribution by Territory</div><div class="sec-body">', unsafe_allow_html=True)
    d1, d2 = st.columns(2)

    with d1:
        fig_dl = px.pie(terr, values="Unique Leads", names="Territory",
                        title="LEADS % OF TOTAL", hole=0.42,
                        color_discrete_sequence=COLORS)
        fig_dl.update_traces(textposition="inside", textinfo="percent",
                              hovertemplate="<b>%{label}</b><br>%{value:,} leads<br>%{percent}<extra></extra>")
        fig_dl.update_layout(height=260, margin=dict(t=40, b=10, l=0, r=0),
                             paper_bgcolor="white",
                             legend=dict(font=dict(size=10), orientation="v"),
                             title_font=dict(size=11, color="#6b7280"))
        st.plotly_chart(fig_dl, use_container_width=True)

    with d2:
        sal_df = terr[terr["Sales Amount ($)"] > 0]
        fig_ds = px.pie(sal_df, values="Sales Amount ($)", names="Territory",
                        title="SALES AMOUNT % OF TOTAL", hole=0.42,
                        color_discrete_sequence=COLORS)
        fig_ds.update_traces(textposition="inside", textinfo="percent",
                              hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>")
        fig_ds.update_layout(height=260, margin=dict(t=40, b=10, l=0, r=0),
                             paper_bgcolor="white",
                             legend=dict(font=dict(size=10), orientation="v"),
                             title_font=dict(size=11, color="#6b7280"))
        st.plotly_chart(fig_ds, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Regional Office Performance table (matches screenshot columns) ───────
    st.markdown('<div class="sec-hdr">🏢 Regional Office Performance</div><div class="sec-body">', unsafe_allow_html=True)

    disp = terr[["Territory","Unique Leads","New Leads","Appointments","Quote",
                 "Customers","Sales Amount ($)","NL Customers","NL Sales ($)",
                 "Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]].copy()

    # Append total row
    tot_row = pd.DataFrame([{
        "Territory": "Total",
        "Unique Leads": int(total["Unique Leads"]),
        "New Leads":    int(total["New Leads"]),
        "Appointments": int(total["Appointments"]),
        "Quote":        int(total["Quote"]),
        "Customers":    int(total["Customers"]),
        "Sales Amount ($)": total["Sales Amount ($)"],
        "NL Customers": int(total["NL Customers"]),
        "NL Sales ($)": total["NL Sales ($)"],
        "Leads %": 100.0, "Sales %": 100.0,
        "APT/Leads":   round(total["Appointments"] / total["Unique Leads"] * 100, 2) if total["Unique Leads"] else 0,
        "Order/APT":   round(total["Customers"] / total["Appointments"] * 100, 2) if total["Appointments"] else 0,
        "Order/Leads": round(total["Customers"] / total["Unique Leads"] * 100, 2) if total["Unique Leads"] else 0,
    }])
    disp = pd.concat([disp, tot_row], ignore_index=True)

    # Format
    disp["Sales Amount ($)"] = disp["Sales Amount ($)"].apply(lambda x: f"${x:,.2f}")
    disp["NL Sales ($)"]     = disp["NL Sales ($)"].apply(lambda x: f"${x:,.2f}")
    disp["Leads %"]          = disp["Leads %"].apply(lambda x: f"{x:.2f}")
    disp["Sales %"]          = disp["Sales %"].apply(lambda x: f"{x:.2f}")
    disp["APT/Leads"]        = disp["APT/Leads"].apply(lambda x: f"{x:.2f}")
    disp["Order/APT"]        = disp["Order/APT"].apply(lambda x: f"{x:.0f}%")
    disp["Order/Leads"]      = disp["Order/Leads"].apply(lambda x: f"{x:.2f}")
    disp.columns = ["Regional Office","Unique Leads","New Leads","APT","Quote",
                    "Customers","Sales Amount","NL Customers","NL Sales",
                    "Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]

    st.dataframe(disp, use_container_width=True, hide_index=True, height=430)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Campaign breakdown by territory ──────────────────────────────────────
    st.markdown('<div class="sec-hdr">📊 Campaign Breakdown by Territory</div><div class="sec-body">', unsafe_allow_html=True)

    tcamp = terr_raw.copy()
    if sel_office != "All":
        tcamp = tcamp[tcamp["Territory"] == sel_office]

    pv_metric = st.selectbox(
        "Metric to compare",
        ["Sales Amount ($)", "Unique Leads", "Appointments", "Customers", "Spend ($)"],
        key="pvm")

    fig_grp = px.bar(
        tcamp.sort_values("Territory"),
        x="Territory", y=pv_metric, color="Campaign",
        barmode="group", color_discrete_sequence=COLORS,
        text_auto=".2s",
        labels={"Territory": "Office", pv_metric: pv_metric.replace(" ($)", "")},
    )
    fig_grp.update_layout(
        height=260, margin=dict(t=10, b=90, l=60, r=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_grp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Meta Ads Dashboard · Streamlit + Plotly · Upload your Excel to replace sample data")
