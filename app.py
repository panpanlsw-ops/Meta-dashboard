import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64, os

st.set_page_config(page_title="Meta Ads Dashboard", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

# ── Inline logos ───────────────────────────────────────────────────────────────
LS_B64 = "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"

META_ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 24" height="20" style="vertical-align:middle;margin-right:2px">
  <path d="M2 12C2 7.2 5.2 3 9.2 3c2.2 0 4.2 1.2 5.8 3.3C16.6 4.2 18.6 3 20.6 3
    c4 0 7.2 4.2 7.2 9 0 2.5-.8 4.8-2.1 6.4-1.2 1.4-2.7 2.2-4.3 2.2
    -2 0-3.6-1-5.6-3.9-2 2.9-3.6 3.9-5.6 3.9-1.6 0-3.1-.8-4.3-2.2
    C2.8 16.8 2 14.5 2 12zm7.2-5.5C6 6.5 4 9 4 12s2 5.5 5.2 5.5
    c1.4 0 2.6-.8 4.2-3.4-1.6-2.8-2.8-4.6-4.2-4.6zm11.4 0c-1.4 0-2.6 1.8-4.2 4.6
    1.6 2.6 2.8 3.4 4.2 3.4 3.2 0 5.2-2.5 5.2-5.5s-2-5.5-5.2-5.5z" fill="white"/>
</svg>"""

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Hide Streamlit chrome */
  #MainMenu,footer,header[data-testid="stHeader"]{display:none!important}
  .block-container{padding:0!important;max-width:100%!important}
  section[data-testid="stSidebar"]{display:none}

  /* Full-page layout */
  .dashboard-wrap{display:flex;flex-direction:column;height:100vh;
    background:#f0f2f6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}

  /* Top nav bar */
  .topbar{background:#1877F2;padding:0 20px;display:flex;align-items:center;
    gap:0;height:48px;flex-shrink:0}
  .topbar-logo{display:flex;align-items:center;gap:8px;margin-right:20px}
  .topbar-divider{width:1px;height:24px;background:rgba(255,255,255,0.25);margin:0 16px}
  .topbar-tabs{display:flex;gap:2px;flex:1}
  .topbar-tab{padding:0 18px;height:48px;display:flex;align-items:center;
    font-size:0.82rem;font-weight:500;color:rgba(255,255,255,0.75);
    cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap}
  .topbar-tab.active{color:white;border-bottom:3px solid white}
  .topbar-right{display:flex;align-items:center;gap:10px;margin-left:auto}
  .topbar-date{font-size:0.75rem;color:rgba(255,255,255,0.75)}
  .ls-badge{background:white;border-radius:5px;padding:2px 8px;
    display:flex;align-items:center}

  /* Sub-filters bar */
  .filterbar{background:white;border-bottom:1px solid #e5e7eb;
    padding:6px 20px;display:flex;align-items:center;gap:10px;flex-shrink:0}
  .filter-label{font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
    letter-spacing:0.06em;margin-right:2px}
  .filter-select{font-size:0.78rem;border:1px solid #e5e7eb;border-radius:5px;
    padding:3px 8px;background:white;color:#374151;cursor:pointer}

  /* Page content */
  .page-content{padding:12px 20px;overflow-y:auto;flex:1}

  /* KPI strip */
  .kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0;
    background:white;border:1px solid #e5e7eb;border-radius:8px;
    overflow:hidden;margin-bottom:8px}
  .kpi-strip-3{display:grid;grid-template-columns:repeat(3,1fr);gap:0;
    background:white;border:1px solid #e5e7eb;border-radius:8px;
    overflow:hidden;margin-bottom:10px}
  .kpi-cell{padding:10px 16px 8px;border-right:1px solid #e5e7eb;position:relative}
  .kpi-cell:last-child{border-right:none}
  .kpi-cell::after{content:'';position:absolute;top:0;left:0;right:0;height:3px}
  .k1::after{background:#1877F2}.k2::after{background:#8b5cf6}
  .k3::after{background:#10b981}.k4::after{background:#f59e0b}
  .k5::after{background:#06b6d4}.k6::after{background:#ec4899}
  .k7::after{background:#22c55e}
  .kpi-lbl{font-size:0.62rem;color:#9ca3af;font-weight:600;
    text-transform:uppercase;letter-spacing:0.06em;margin-bottom:3px}
  .kpi-val{font-size:1.25rem;font-weight:700;color:#111827;
    line-height:1.1;margin-bottom:2px}
  .kpi-pos{font-size:0.68rem;color:#10b981;font-weight:600}
  .kpi-neg{font-size:0.68rem;color:#ef4444;font-weight:600}

  /* Territory KPI strip */
  .terr-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:0;
    background:white;border:1px solid #e5e7eb;border-radius:8px;
    overflow:hidden;margin-bottom:10px}
  .terr-cell{padding:10px 12px 8px;border-right:1px solid #e5e7eb;text-align:center}
  .terr-cell:last-child{border-right:none}
  .terr-top{display:block;height:3px;margin-bottom:6px;border-radius:0}
  .terr-lbl{font-size:0.62rem;color:#9ca3af;font-weight:600;
    text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px}
  .terr-val{font-size:1.2rem;font-weight:700;color:#111827}

  /* Section cards */
  .sec-hdr{background:#1877F2;color:white;padding:5px 12px;
    border-radius:6px 6px 0 0;font-weight:600;font-size:0.78rem;
    display:flex;align-items:center;gap:5px}
  .sec-body{background:white;border:1px solid #e5e7eb;border-top:none;
    border-radius:0 0 6px 6px;padding:10px;margin-bottom:10px}

  /* Campaign pills */
  div[data-testid="stHorizontalBlock"] .stButton button{
    border-radius:20px!important;font-size:0.75rem!important;
    padding:4px 14px!important;height:auto!important}

  /* Tighten default streamlit spacing */
  div[data-testid="stVerticalBlock"]{gap:0!important}
  .element-container{margin-bottom:0!important}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
COLORS = ["#1877F2","#10b981","#f59e0b","#8b5cf6","#ef4444",
          "#06b6d4","#f97316","#ec4899","#22c55e","#a78bfa","#fb923c","#34d399","#60a5fa"]

def fmt_num(n):
    if pd.isna(n): return "—"
    if abs(n)>=1_000_000: return f"{n/1_000_000:.1f}M"
    if abs(n)>=1_000: return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"

def fmt_cur(n):
    if pd.isna(n) or n==0: return "$0"
    if abs(n)>=1_000_000: return f"${n/1_000_000:.1f}M"
    if abs(n)>=1_000: return f"${n/1_000:.1f}K"
    return f"${n:,.0f}"

def delta_html(v, pos_good=True):
    if pd.isna(v): return ""
    arrow = "▲" if v>0 else "▼"
    cls = ("kpi-pos" if v>0 else "kpi-neg") if pos_good else ("kpi-neg" if v>0 else "kpi-pos")
    return f'<span class="{cls}">{arrow} {abs(v):.1f}%</span>'

@st.cache_data
def load(file):
    xls = pd.ExcelFile(file)
    return {n: pd.read_excel(xls, sheet_name=n) for n in xls.sheet_names}

def chart_base(h=220):
    return dict(height=h, margin=dict(t=8,b=35,l=55,r=15),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(showgrid=False, tickformat="%b %d"),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified")

# ── Load data ──────────────────────────────────────────────────────────────────
uploaded = None   # no sidebar

# Try sample data
try:
    data = load("meta_ads_data.xlsx")
except Exception:
    data = {}

# ── Tab state ──────────────────────────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "overview"

# ── TOP NAV BAR ───────────────────────────────────────────────────────────────
tab_defs = [
    ("overview",   "📊 MTD Overview"),
    ("trends",     "📈 Trends"),
    ("territory",  "🗺️ By Territory"),
]

t1_active = "active" if st.session_state.active_tab=="overview"  else ""
t2_active = "active" if st.session_state.active_tab=="trends"    else ""
t3_active = "active" if st.session_state.active_tab=="territory" else ""

st.markdown(f"""
<div class="topbar">
  <div class="topbar-logo">
    {META_ICON}
    <span style="color:white;font-weight:700;font-size:0.9rem">Meta</span>
  </div>
  <div class="topbar-divider"></div>
  <span style="color:rgba(255,255,255,0.85);font-size:0.85rem;font-weight:600;margin-right:20px">
    {"MTD Overview" if st.session_state.active_tab=="overview" else "Trends" if st.session_state.active_tab=="trends" else "By Territory"}
  </span>
  <div class="topbar-right">
    <span class="topbar-date">Dec 2024</span>
    <div class="ls-badge">
      <img src="data:image/png;base64,{LS_B64}" height="22" style="object-fit:contain">
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Tab buttons rendered as Streamlit buttons in a row
tc = st.columns([1,1,1,6])
with tc[0]:
    if st.button("📊 MTD Overview", use_container_width=True,
                 type="primary" if st.session_state.active_tab=="overview" else "secondary"):
        st.session_state.active_tab = "overview"
        st.rerun()
with tc[1]:
    if st.button("📈 Trends", use_container_width=True,
                 type="primary" if st.session_state.active_tab=="trends" else "secondary"):
        st.session_state.active_tab = "trends"
        st.rerun()
with tc[2]:
    if st.button("🗺️ By Territory", use_container_width=True,
                 type="primary" if st.session_state.active_tab=="territory" else "secondary"):
        st.session_state.active_tab = "territory"
        st.rerun()
with tc[3]:
    pass  # spacer

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ── Filters bar ────────────────────────────────────────────────────────────────
fc = st.columns([2,2,2,2,1])
with fc[0]:
    uploaded = st.file_uploader("", type=["xlsx","xls"], label_visibility="collapsed",
                                 help="Upload your Meta Ads Excel file")
    if uploaded:
        data = load(uploaded)

with fc[1]:
    camp_list = ["All Campaigns"]
    if "Campaign Performance" in data:
        camp_list += list(data["Campaign Performance"]["Campaign Objective"].unique())
    sel_camp = st.selectbox("Campaign", camp_list, label_visibility="visible")

with fc[2]:
    offices = ["All Offices"]
    if "Territory Performance" in data:
        offices += sorted(data["Territory Performance"]["Territory"].unique().tolist())
    sel_office = st.selectbox("Office", offices, label_visibility="visible")

with fc[3]:
    date_range = None
    if "Daily Performance" in data:
        daily_raw = data["Daily Performance"].copy()
        daily_raw["Date"] = pd.to_datetime(daily_raw["Date"])
        mn, mx = daily_raw["Date"].min().date(), daily_raw["Date"].max().date()
        date_range = st.date_input("Date range", value=(mn,mx), min_value=mn, max_value=mx,
                                   label_visibility="visible")

with fc[4]:
    st.markdown("<div style='padding-top:22px'>", unsafe_allow_html=True)
    if "Daily Performance" in data:
        csv = data["Daily Performance"].to_csv(index=False).encode()
        st.download_button("⬇ Export", csv, "meta_daily.csv", "text/csv",
                           use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MTD OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "overview":

    if "Overview" in data:
        ov = data["Overview"].set_index("Metric")

        def kc(metric, cls, is_cur=False, pos_good=True):
            if metric not in ov.index:
                return f'<div class="kpi-cell {cls}"><div class="kpi-lbl">{metric}</div><div class="kpi-val">—</div></div>'
            row = ov.loc[metric]
            fval = fmt_cur(row["Current Period"]) if is_cur else fmt_num(row["Current Period"])
            return (f'<div class="kpi-cell {cls}"><div class="kpi-lbl">{metric}</div>'
                    f'<div class="kpi-val">{fval}</div>{delta_html(row["Change %"], pos_good)}</div>')

        st.markdown(
            '<div class="kpi-strip">' +
            kc("Spend ($)",   "k1", True, False) +
            kc("Clicks",      "k2", False, True) +
            kc("Conversions", "k3", False, True) +
            kc("CRM Leads",   "k4", False, True) +
            '</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="kpi-strip-3">' +
            kc("Appointments",     "k5", False, True) +
            kc("Customers",        "k6", False, True) +
            kc("Sales Amount ($)", "k7", True,  True) +
            '</div>', unsafe_allow_html=True)

    if "Campaign Performance" in data:
        camp_df = data["Campaign Performance"].copy()

        if "t1_camp" not in st.session_state:
            st.session_state.t1_camp = "All Campaigns"

        all_camps = list(camp_df["Campaign Objective"].unique())
        camp_options = ["All Campaigns"] + all_camps
        bc = st.columns(len(camp_options))
        for i, label in enumerate(camp_options):
            if bc[i].button(label, key=f"cp_{i}", use_container_width=True,
                            type="primary" if st.session_state.t1_camp==label else "secondary"):
                st.session_state.t1_camp = label
                st.rerun()

        sel = st.session_state.t1_camp
        fcamp = camp_df if sel=="All Campaigns" else camp_df[camp_df["Campaign Objective"]==sel]

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="sec-hdr">💸 Spend by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            fig = px.pie(camp_df, values="Spend ($)", names="Campaign Objective",
                         hole=0.42, color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside", textinfo="percent",
                              hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
            fig.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=0),
                              paper_bgcolor="white", showlegend=True,
                              legend=dict(font=dict(size=9)))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="sec-hdr">👥 CRM Leads by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            ld = camp_df[camp_df["CRM Leads"]>0].sort_values("CRM Leads")
            fig2 = px.bar(ld, x="CRM Leads", y="Campaign Objective", orientation="h",
                          color="Campaign Objective", color_discrete_sequence=COLORS, text="CRM Leads")
            fig2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            fig2.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=50),
                               showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
                               xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            st.markdown('<div class="sec-hdr">💰 Sales by Campaign</div><div class="sec-body">', unsafe_allow_html=True)
            sd = camp_df[camp_df["Sales Amount ($)"]>0].sort_values("Sales Amount ($)")
            fig3 = px.bar(sd, x="Sales Amount ($)", y="Campaign Objective", orientation="h",
                          color="Campaign Objective", color_discrete_sequence=COLORS,
                          text="Sales Amount ($)")
            fig3.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig3.update_layout(height=220, margin=dict(t=0,b=0,l=0,r=70),
                               showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
                               xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f'<div class="sec-hdr">📋 Campaign Breakdown — {sel}</div><div class="sec-body">',
                    unsafe_allow_html=True)
        cols_show = ["Campaign Objective","Spend ($)","Impressions","Clicks",
                     "CRM Leads","Conversions","Appointments","Customers","Sales Amount ($)","ROAS"]
        tbl = fcamp[[c for c in cols_show if c in fcamp.columns]].copy()
        tbl["Spend ($)"]        = tbl["Spend ($)"].apply(fmt_cur)
        tbl["Impressions"]      = tbl["Impressions"].apply(fmt_num)
        tbl["Clicks"]           = tbl["Clicks"].apply(fmt_num)
        tbl["CRM Leads"]        = tbl["CRM Leads"].apply(lambda x: fmt_num(x) if x>0 else "—")
        tbl["Conversions"]      = tbl["Conversions"].apply(lambda x: fmt_num(x) if x>0 else "—")
        tbl["Appointments"]     = tbl["Appointments"].apply(fmt_num)
        tbl["Customers"]        = tbl["Customers"].apply(lambda x: fmt_num(x) if x>0 else "—")
        tbl["Sales Amount ($)"] = tbl["Sales Amount ($)"].apply(lambda x: fmt_cur(x) if x>0 else "—")
        tbl["ROAS"]             = tbl["ROAS"].apply(lambda x: f"{x:.1f}x" if x>0 else "—")
        st.dataframe(tbl, use_container_width=True, hide_index=True, height=180)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "trends":

    if "Daily Performance" not in data:
        st.warning("No 'Daily Performance' sheet found in your Excel file.")
        st.stop()

    daily = data["Daily Performance"].copy()
    daily["Date"] = pd.to_datetime(daily["Date"])

    if date_range and len(date_range)==2:
        daily = daily[(daily["Date"]>=pd.Timestamp(date_range[0])) &
                      (daily["Date"]<=pd.Timestamp(date_range[1]))]
    if sel_camp!="All Campaigns" and "Campaign" in daily.columns:
        daily = daily[daily["Campaign"]==sel_camp]

    agg = daily.groupby("Date").agg({
        "Spend ($)":"sum","Impressions":"sum","Reach":"sum","Clicks":"sum",
        "CRM Leads":"sum","Conversions":"sum","Appointments":"sum",
        "Customers":"sum","Sales Amount ($)":"sum","ROAS":"mean"
    }).reset_index()

    gc = st.columns([1,1,1,5])
    with gc[0]:
        if st.button("Daily",   type="primary" if st.session_state.get("gran","Daily")=="Daily"   else "secondary", use_container_width=True): st.session_state.gran="Daily";   st.rerun()
    with gc[1]:
        if st.button("Weekly",  type="primary" if st.session_state.get("gran","Daily")=="Weekly"  else "secondary", use_container_width=True): st.session_state.gran="Weekly";  st.rerun()
    with gc[2]:
        if st.button("Monthly", type="primary" if st.session_state.get("gran","Daily")=="Monthly" else "secondary", use_container_width=True): st.session_state.gran="Monthly"; st.rerun()
    with gc[3]: pass

    gran = st.session_state.get("gran","Daily")
    if gran=="Weekly":  agg = agg.resample("W",  on="Date").sum().reset_index()
    if gran=="Monthly": agg = agg.resample("ME", on="Date").sum().reset_index()

    metric_opts = ["Spend ($)","Sales Amount ($)","CRM Leads","Clicks","Conversions","Appointments","Customers","ROAS"]
    defaults    = [True,True,True,False,False,False,False,False]
    mc = st.columns(8)
    sel_metrics = [m for i,(m,d) in enumerate(zip(metric_opts,defaults))
                   if mc[i].checkbox(m.replace(" ($)",""), value=d, key=f"m{i}")]

    if sel_metrics:
        st.markdown('<div class="sec-hdr">📈 Metrics Over Time</div><div class="sec-body">', unsafe_allow_html=True)
        fig_main = go.Figure()
        for m, col in zip(sel_metrics, COLORS):
            if m not in agg.columns: continue
            fig_main.add_trace(go.Scatter(x=agg["Date"], y=agg[m], name=m,
                mode="lines+markers", line=dict(color=col,width=2), marker=dict(size=4),
                hovertemplate=f"<b>%{{x|%b %d}}</b><br>{m}: %{{y:,.1f}}<extra></extra>"))
        fig_main.update_layout(**chart_base(240))
        st.plotly_chart(fig_main, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    r1,r2 = st.columns(2)
    with r1:
        st.markdown('<div class="sec-hdr">💹 ROAS Trend</div><div class="sec-body">', unsafe_allow_html=True)
        fig_r = go.Figure(go.Scatter(x=agg["Date"],y=agg["ROAS"],mode="lines+markers",
            line=dict(color="#22c55e",width=2.5),fill="tozeroy",fillcolor="rgba(34,197,94,0.08)",
            hovertemplate="<b>%{x|%b %d}</b><br>ROAS: %{y:.2f}x<extra></extra>"))
        fig_r.update_layout(height=185,margin=dict(t=8,b=30,l=50,r=10),
            paper_bgcolor="white",plot_bgcolor="white",
            xaxis=dict(showgrid=False,tickformat="%b %d"),
            yaxis=dict(showgrid=True,gridcolor="#f3f4f6",ticksuffix="x"))
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="sec-hdr">💸 Spend vs Sales</div><div class="sec-body">', unsafe_allow_html=True)
        fig_sv = make_subplots(specs=[[{"secondary_y":True}]])
        fig_sv.add_trace(go.Bar(x=agg["Date"],y=agg["Spend ($)"],name="Spend",
            marker_color="rgba(24,119,242,0.7)",hovertemplate="Spend: $%{y:,.0f}<extra></extra>"),secondary_y=False)
        fig_sv.add_trace(go.Scatter(x=agg["Date"],y=agg["Sales Amount ($)"],name="Sales",
            line=dict(color="#22c55e",width=2.5),hovertemplate="Sales: $%{y:,.0f}<extra></extra>"),secondary_y=True)
        fig_sv.update_layout(height=185,margin=dict(t=8,b=30,l=50,r=50),
            paper_bgcolor="white",plot_bgcolor="white",
            legend=dict(orientation="h",y=1.08),hovermode="x unified",
            xaxis=dict(showgrid=False,tickformat="%b %d"))
        fig_sv.update_yaxes(showgrid=True,gridcolor="#f3f4f6",secondary_y=False)
        fig_sv.update_yaxes(showgrid=False,secondary_y=True)
        st.plotly_chart(fig_sv, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    a1,a2 = st.columns(2)
    with a1:
        st.markdown('<div class="sec-hdr">📡 Impressions & Reach</div><div class="sec-body">', unsafe_allow_html=True)
        fig_acq = go.Figure()
        fig_acq.add_trace(go.Scatter(x=agg["Date"],y=agg["Impressions"],name="Impressions",
            line=dict(color="#1877F2",width=2),hovertemplate="Impr: %{y:,.0f}<extra></extra>"))
        fig_acq.add_trace(go.Scatter(x=agg["Date"],y=agg["Reach"],name="Reach",
            line=dict(color="#8b5cf6",width=2,dash="dash"),hovertemplate="Reach: %{y:,.0f}<extra></extra>"))
        fig_acq.update_layout(**chart_base(185))
        st.plotly_chart(fig_acq, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with a2:
        st.markdown('<div class="sec-hdr">🎯 Conversion Funnel</div><div class="sec-body">', unsafe_allow_html=True)
        fig_cv = go.Figure()
        for m,col in [("Conversions","#10b981"),("Appointments","#06b6d4"),("Customers","#ec4899")]:
            fig_cv.add_trace(go.Scatter(x=agg["Date"],y=agg[m],name=m,
                line=dict(color=col,width=2),hovertemplate=f"{m}: %{{y:,.0f}}<extra></extra>"))
        fig_cv.update_layout(**chart_base(185))
        st.plotly_chart(fig_cv, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    b1,b2 = st.columns(2)
    with b1:
        st.markdown('<div class="sec-hdr">🖱️ Clicks</div><div class="sec-body">', unsafe_allow_html=True)
        fig_cl = go.Figure(go.Bar(x=agg["Date"],y=agg["Clicks"],marker_color="rgba(139,92,246,0.75)",
            hovertemplate="Clicks: %{y:,.0f}<extra></extra>"))
        fig_cl.update_layout(height=170,margin=dict(t=8,b=30,l=55,r=10),
            paper_bgcolor="white",plot_bgcolor="white",
            xaxis=dict(showgrid=False,tickformat="%b %d"),
            yaxis=dict(showgrid=True,gridcolor="#f3f4f6"))
        st.plotly_chart(fig_cl, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="sec-hdr">👥 CRM Leads</div><div class="sec-body">', unsafe_allow_html=True)
        fig_ld = go.Figure(go.Bar(x=agg["Date"],y=agg["CRM Leads"],marker_color="rgba(245,158,11,0.75)",
            hovertemplate="Leads: %{y:,.0f}<extra></extra>"))
        fig_ld.update_layout(height=170,margin=dict(t=8,b=30,l=55,r=10),
            paper_bgcolor="white",plot_bgcolor="white",
            xaxis=dict(showgrid=False,tickformat="%b %d"),
            yaxis=dict(showgrid=True,gridcolor="#f3f4f6"))
        st.plotly_chart(fig_ld, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BY TERRITORY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "territory":

    if "Territory Performance" not in data:
        st.warning("No 'Territory Performance' sheet found.")
        st.stop()

    terr_raw = data["Territory Performance"].copy()
    t3_camps = ["All Campaigns"] + sorted(terr_raw["Campaign"].unique().tolist())
    sel_t3   = st.selectbox("Filter by Campaign", t3_camps, key="t3camp")
    tdf      = terr_raw if sel_t3=="All Campaigns" else terr_raw[terr_raw["Campaign"]==sel_t3]

    terr = tdf.groupby("Territory").agg({
        "Unique Leads":"sum","New Leads":"sum","Appointments":"sum",
        "Quote":"sum","Customers":"sum","Sales Amount ($)":"sum",
        "NL Customers":"sum","NL Sales ($)":"sum","Spend ($)":"sum","ROAS":"mean"
    }).reset_index()

    total = terr.sum(numeric_only=True)
    terr["Leads %"]     = (terr["Unique Leads"]    /total["Unique Leads"]     *100).round(2)
    terr["Sales %"]     = (terr["Sales Amount ($)"]/total["Sales Amount ($)"] *100).round(2)
    terr["APT/Leads"]   = (terr["Appointments"]    /terr["Unique Leads"].replace(0,1)*100).round(2)
    terr["Order/APT"]   = (terr["Customers"]       /terr["Appointments"].replace(0,1)*100).round(2)
    terr["Order/Leads"] = (terr["Customers"]       /terr["Unique Leads"].replace(0,1)*100).round(2)
    terr = terr.sort_values("Sales Amount ($)", ascending=False)

    tot_ul  = int(total["Unique Leads"])
    tot_apt = int(total["Appointments"])
    tot_cu  = int(total["Customers"])
    tot_sal = total["Sales Amount ($)"]
    apt_pct = round(tot_apt/tot_ul*100) if tot_ul else 0

    st.markdown(f"""
    <div class="terr-strip">
      <div class="terr-cell"><span class="terr-top" style="background:#1877F2"></span>
        <div class="terr-lbl">Total Leads</div><div class="terr-val">{tot_ul:,}</div></div>
      <div class="terr-cell"><span class="terr-top" style="background:#10b981"></span>
        <div class="terr-lbl">Appointments</div><div class="terr-val">{tot_apt:,}</div></div>
      <div class="terr-cell"><span class="terr-top" style="background:#8b5cf6"></span>
        <div class="terr-lbl">Customers</div><div class="terr-val">{tot_cu:,}</div></div>
      <div class="terr-cell"><span class="terr-top" style="background:#22c55e"></span>
        <div class="terr-lbl">Total Sales</div><div class="terr-val">{fmt_cur(tot_sal)}</div></div>
      <div class="terr-cell"><span class="terr-top" style="background:#f59e0b"></span>
        <div class="terr-lbl">APT / Leads</div><div class="terr-val">{apt_pct}%</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">🥧 Distribution by Territory</div><div class="sec-body">', unsafe_allow_html=True)
    d1,d2 = st.columns(2)
    with d1:
        fig_dl = px.pie(terr, values="Unique Leads", names="Territory",
                        title="LEADS % OF TOTAL", hole=0.42, color_discrete_sequence=COLORS)
        fig_dl.update_traces(textposition="inside", textinfo="percent",
                             hovertemplate="<b>%{label}</b><br>%{value:,} leads<br>%{percent}<extra></extra>")
        fig_dl.update_layout(height=300,margin=dict(t=35,b=5,l=0,r=0),
                             paper_bgcolor="white",legend=dict(font=dict(size=10)),
                             title_font=dict(size=10,color="#6b7280"))
        st.plotly_chart(fig_dl, use_container_width=True)
    with d2:
        sal_df = terr[terr["Sales Amount ($)"]>0]
        fig_ds = px.pie(sal_df, values="Sales Amount ($)", names="Territory",
                        title="SALES AMOUNT % OF TOTAL", hole=0.42, color_discrete_sequence=COLORS)
        fig_ds.update_traces(textposition="inside", textinfo="percent",
                             hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>")
        fig_ds.update_layout(height=300,margin=dict(t=35,b=5,l=0,r=0),
                             paper_bgcolor="white",legend=dict(font=dict(size=10)),
                             title_font=dict(size=10,color="#6b7280"))
        st.plotly_chart(fig_ds, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">🏢 Regional Office Performance</div><div class="sec-body">', unsafe_allow_html=True)
    disp = terr[["Territory","Unique Leads","New Leads","Appointments","Quote",
                 "Customers","Sales Amount ($)","NL Customers","NL Sales ($)",
                 "Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]].copy()
    tot_row = pd.DataFrame([{"Territory":"Total","Unique Leads":int(total["Unique Leads"]),
        "New Leads":int(total["New Leads"]),"Appointments":int(total["Appointments"]),
        "Quote":int(total["Quote"]),"Customers":int(total["Customers"]),
        "Sales Amount ($)":total["Sales Amount ($)"],"NL Customers":int(total["NL Customers"]),
        "NL Sales ($)":total["NL Sales ($)"],"Leads %":100.0,"Sales %":100.0,
        "APT/Leads":round(total["Appointments"]/total["Unique Leads"]*100,2) if total["Unique Leads"] else 0,
        "Order/APT":round(total["Customers"]/total["Appointments"]*100,2) if total["Appointments"] else 0,
        "Order/Leads":round(total["Customers"]/total["Unique Leads"]*100,2) if total["Unique Leads"] else 0}])
    disp = pd.concat([disp,tot_row],ignore_index=True)
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
    st.dataframe(disp, use_container_width=True, hide_index=True, height=400)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">📊 Campaign Breakdown by Territory</div><div class="sec-body">', unsafe_allow_html=True)
    tcamp = terr_raw.copy()
    if sel_office!="All Offices":
        tcamp = tcamp[tcamp["Territory"]==sel_office]
    pv_metric = st.selectbox("Metric",["Sales Amount ($)","Unique Leads","Appointments","Customers","Spend ($)"],key="pvm")
    fig_grp = px.bar(tcamp.sort_values("Territory"),x="Territory",y=pv_metric,color="Campaign",
                     barmode="group",color_discrete_sequence=COLORS,text_auto=".2s")
    fig_grp.update_layout(height=300,margin=dict(t=8,b=80,l=60,r=10),
                          paper_bgcolor="white",plot_bgcolor="white",
                          xaxis=dict(showgrid=False,tickangle=-30),
                          yaxis=dict(showgrid=True,gridcolor="#f3f4f6"),
                          legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    st.plotly_chart(fig_grp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
