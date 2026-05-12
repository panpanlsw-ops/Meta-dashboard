import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Meta Ads Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LS_B64 = "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"

META_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 24" height="18" style="vertical-align:middle">
<path d="M2 12C2 7.2 5.2 3 9.2 3c2.2 0 4.2 1.2 5.8 3.3C16.6 4.2 18.6 3 20.6 3
c4 0 7.2 4.2 7.2 9 0 2.5-.8 4.8-2.1 6.4-1.2 1.4-2.7 2.2-4.3 2.2
-2 0-3.6-1-5.6-3.9-2 2.9-3.6 3.9-5.6 3.9-1.6 0-3.1-.8-4.3-2.2
C2.8 16.8 2 14.5 2 12zm7.2-5.5C6 6.5 4 9 4 12s2 5.5 5.2 5.5
c1.4 0 2.6-.8 4.2-3.4-1.6-2.8-2.8-4.6-4.2-4.6zm11.4 0c-1.4 0-2.6 1.8-4.2 4.6
1.6 2.6 2.8 3.4 4.2 3.4 3.2 0 5.2-2.5 5.2-5.5s-2-5.5-5.2-5.5z" fill="white"/>
</svg>"""

st.markdown("""
<style>
#MainMenu, footer { display:none!important }
header[data-testid="stHeader"] { display:none!important }
section[data-testid="stSidebar"] { display:none!important }
button[data-testid="collapsedControl"] { display:none!important }
.block-container { padding:0!important; max-width:100%!important }

/* ── Top bar ── */
.topbar {
    background:#1877F2; padding:0 24px;
    display:flex; align-items:center; height:50px; gap:16px;
}
.topbar-brand { display:flex; align-items:center; gap:8px; }
.topbar-brand span { color:white; font-size:1rem; font-weight:700; }
.topbar-sep { width:1px; height:24px; background:rgba(255,255,255,0.3); }
.topbar-date { color:rgba(255,255,255,0.85); font-size:0.85rem; margin-left:auto; }
.topbar-ls { background:white; border-radius:5px; padding:3px 10px; display:flex; align-items:center; }

/* ── Left nav + content layout ── */
.dash-layout {
    display:flex; min-height:calc(100vh - 50px);
}
.left-nav {
    width:220px; min-width:220px; background:#1a1e3c;
    display:flex; flex-direction:column; padding:0;
}
.nav-logo {
    padding:18px 16px 14px;
    border-bottom:1px solid rgba(255,255,255,0.1);
    text-align:center;
}
.nav-section {
    font-size:0.65rem; color:#4a5a80; font-weight:700;
    text-transform:uppercase; letter-spacing:0.1em;
    padding:14px 16px 6px;
}
.nav-item {
    display:flex; align-items:center; gap:10px;
    padding:10px 16px; margin:1px 8px; border-radius:7px;
    font-size:0.85rem; font-weight:500; color:#8a9bc0;
    cursor:pointer; text-decoration:none;
}
.nav-item:hover { background:rgba(255,255,255,0.07); color:#c8d0e8; }
.nav-item.active { background:#1877F2; color:white; }
.nav-icon { font-size:1rem; width:20px; text-align:center; }
.nav-filter-label {
    font-size:0.65rem; color:#4a5a80; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em;
    padding:2px 16px 4px;
}
.nav-hr { border:none; border-top:1px solid rgba(255,255,255,0.1); margin:10px 0; }
.main-content { flex:1; padding:20px 24px; background:#f4f6fb; overflow-y:auto; }

/* ── KPI cards — one row of 7, longer cards ── */
.krow { display:grid; grid-template-columns:repeat(7,1fr); gap:10px; margin-bottom:24px; }
.kcell {
    background:white; border:1px solid #e5e7eb; border-radius:10px;
    padding:16px 16px 12px; position:relative;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
}
.kcell::before {
    content:""; position:absolute; top:0; left:0; right:0;
    height:4px; border-radius:10px 10px 0 0;
}
.c1::before{background:#1877F2} .c2::before{background:#22c55e}
.c3::before{background:#8b5cf6} .c4::before{background:#10b981}
.c5::before{background:#f59e0b} .c6::before{background:#ec4899}
.c7::before{background:#06b6d4}
.kl { font-size:0.68rem; color:#9ca3af; font-weight:600;
      text-transform:uppercase; letter-spacing:.07em; margin-bottom:6px; }
.kv { font-size:1.35rem; font-weight:700; color:#111827; line-height:1.1; margin-bottom:4px; }
.kp { font-size:0.72rem; color:#10b981; font-weight:600; }
.kn { font-size:0.72rem; color:#ef4444; font-weight:600; }

/* ── Section cards ── */
.sh { background:#1877F2; color:white; padding:8px 14px;
      border-radius:8px 8px 0 0; font-weight:600; font-size:0.82rem;
      display:flex; align-items:center; gap:6px; }
.sb { background:white; border:1px solid #e5e7eb; border-top:none;
      border-radius:0 0 8px 8px; padding:12px; margin-bottom:20px; }

/* ── Territory strip ── */
.tstrip { display:grid; grid-template-columns:repeat(5,1fr); gap:10px; margin-bottom:20px; }
.tcell  { background:white; border:1px solid #e5e7eb; border-radius:10px;
          padding:14px 14px 12px; text-align:center;
          box-shadow:0 1px 4px rgba(0,0,0,0.05); }
.ttop   { display:block; height:4px; border-radius:3px; margin-bottom:8px; }
.tl     { font-size:0.68rem; color:#9ca3af; font-weight:600;
          text-transform:uppercase; letter-spacing:.06em; margin-bottom:5px; }
.tv     { font-size:1.2rem; font-weight:700; color:#111827; }

div[data-testid="stVerticalBlock"]>div { gap:0!important }
.element-container { margin-bottom:0!important }
.stPlotlyChart { margin:0!important; padding:0!important }
div[data-testid="column"] { padding:0 4px!important }
</style>
""", unsafe_allow_html=True)

COLORS = ["#1877F2","#10b981","#f59e0b","#8b5cf6","#ef4444",
          "#06b6d4","#f97316","#ec4899","#22c55e","#a78bfa","#fb923c","#34d399"]

def fn(n):
    if pd.isna(n): return "—"
    if abs(n)>=1_000_000: return f"{n/1e6:.1f}M"
    if abs(n)>=1_000: return f"{n/1e3:.1f}K"
    return f"{n:,.0f}"
def fc(n):
    if pd.isna(n) or n==0: return "$0"
    if abs(n)>=1_000_000: return f"${n/1e6:.1f}M"
    if abs(n)>=1_000: return f"${n/1e3:.1f}K"
    return f"${n:,.0f}"
def dlt(v, pg=True):
    if pd.isna(v): return ""
    a = "▲" if v>0 else "▼"
    c = ("kp" if v>0 else "kn") if pg else ("kn" if v>0 else "kp")
    return f'<span class="{c}">{a} {abs(v):.1f}%</span>'

@st.cache_data
def load_data(f):
    xls = pd.ExcelFile(f)
    return {n: pd.read_excel(xls, sheet_name=n) for n in xls.sheet_names}

def ch(h=200):
    return dict(height=h, margin=dict(t=6,b=30,l=48,r=8),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(showgrid=False, tickformat="%b %d"),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified")

if "page"  not in st.session_state: st.session_state.page  = "overview"
if "t1c"   not in st.session_state: st.session_state.t1c   = "All Campaigns"
if "gran"  not in st.session_state: st.session_state.gran  = "Daily"

try:    data = load_data("meta_ads_data.xlsx")
except: data = {}

# ── TOP BAR ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">{META_SVG}<span>Meta Ads</span></div>
  <div class="topbar-sep"></div>
  <span style="color:rgba(255,255,255,0.9);font-size:0.9rem;font-weight:500">
    {"MTD Overview" if st.session_state.page=="overview" else "Trends" if st.session_state.page=="trends" else "By Territory"}
  </span>
  <span class="topbar-date">Dec 2024</span>
  <div class="topbar-ls">
    <img src="data:image/png;base64,{LS_B64}" height="22" style="object-fit:contain">
  </div>
</div>
""", unsafe_allow_html=True)

# ── LEFT NAV + MAIN CONTENT side by side using columns ───────────────────────
nav_col, main_col = st.columns([1, 5.5])

# ── LEFT NAV ─────────────────────────────────────────────────────────────────
with nav_col:
    st.markdown(f"""
    <div class="left-nav">
      <div class="nav-logo">
        <img src="data:image/png;base64,{LS_B64}" height="36"
             style="object-fit:contain;display:block;margin:0 auto 8px">
        <div style="display:inline-flex;align-items:center;gap:6px;
                    background:rgba(255,255,255,0.08);border-radius:6px;padding:4px 12px">
          {META_SVG}
          <span style="color:white;font-size:0.82rem;font-weight:600">Meta Ads</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Nav buttons
    pages = [
        ("overview",  "📊", "MTD Overview"),
        ("trends",    "📈", "Trends"),
        ("territory", "🗺️", "By Territory"),
    ]
    for key, icon, label in pages:
        is_active = st.session_state.page == key
        btn_style = (
            "background:#1877F2;color:white;border:none;"
            if is_active else
            "background:rgba(255,255,255,0.05);color:#8a9bc0;border:none;"
        )
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:12px 0'>",
                unsafe_allow_html=True)

    # Filters
    st.markdown("<p style='color:#4a5a80;font-size:0.65rem;font-weight:700;"
                "text-transform:uppercase;letter-spacing:0.1em;"
                "padding:0 4px;margin-bottom:4px'>Filters</p>",
                unsafe_allow_html=True)

    camp_list = ["All Campaigns"]
    if "Campaign Performance" in data:
        camp_list += list(data["Campaign Performance"]["Campaign Objective"].unique())
    sel_camp = st.selectbox("Campaign", camp_list, label_visibility="collapsed")

    off_list = ["All"]
    if "Territory Performance" in data:
        off_list += sorted(data["Territory Performance"]["Territory"].unique().tolist())
    sel_off = st.selectbox("Office", off_list, label_visibility="collapsed")

    date_range = None
    if "Daily Performance" in data:
        dr = data["Daily Performance"].copy()
        dr["Date"] = pd.to_datetime(dr["Date"])
        mn, mx = dr["Date"].min().date(), dr["Date"].max().date()
        date_range = st.date_input("Dates", value=(mn,mx),
                                   min_value=mn, max_value=mx,
                                   label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:10px 0'>",
                unsafe_allow_html=True)

    up = st.file_uploader("Upload", type=["xlsx","xls"], label_visibility="collapsed")
    if up:
        data = load_data(up); st.rerun()
    if "Daily Performance" in data:
        csv = data["Daily Performance"].to_csv(index=False).encode()
        st.download_button("⬇ Export", csv, "meta.csv", "text/csv",
                           use_container_width=True)

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────
with main_col:

    # ══ PAGE 1 — MTD OVERVIEW ══════════════════════════════════════════════════
    if st.session_state.page == "overview":

        if "Overview" in data:
            ov = data["Overview"].set_index("Metric")
            def kc(m, cls, cur=False, pg=True):
                if m not in ov.index:
                    return f'<div class="kcell {cls}"><div class="kl">{m}</div><div class="kv">—</div></div>'
                r = ov.loc[m]
                v = fc(r["Current Period"]) if cur else fn(r["Current Period"])
                return (f'<div class="kcell {cls}"><div class="kl">{m}</div>'
                        f'<div class="kv">{v}</div>{dlt(r["Change %"],pg)}</div>')

            st.markdown(
                '<div class="krow">' +
                kc("Spend ($)",        "c1", True,  False) +
                kc("Sales Amount ($)", "c2", True,  True)  +
                kc("Clicks",           "c3", False, True)  +
                kc("Conversions",      "c4", False, True)  +
                kc("CRM Leads",        "c5", False, True)  +
                kc("Appointments",     "c6", False, True)  +
                kc("Customers",        "c7", False, True)  +
                '</div>', unsafe_allow_html=True)

        if "Campaign Performance" in data:
            camp_df = data["Campaign Performance"].copy()
            opts = ["All Campaigns"] + list(camp_df["Campaign Objective"].unique())
            st.caption("Select campaign to drill down:")
            bc = st.columns(len(opts))
            for i, lb in enumerate(opts):
                if bc[i].button(lb, key=f"cp{i}", use_container_width=True,
                                type="primary" if st.session_state.t1c==lb else "secondary"):
                    st.session_state.t1c = lb; st.rerun()

            sel = st.session_state.t1c
            fd  = camp_df if sel=="All Campaigns" else camp_df[camp_df["Campaign Objective"]==sel]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown('<div class="sh">💸 Spend by Campaign</div><div class="sb">', unsafe_allow_html=True)
                fig = px.pie(camp_df, values="Spend ($)", names="Campaign Objective",
                             hole=0.42, color_discrete_sequence=COLORS)
                fig.update_traces(textposition="inside", textinfo="percent",
                                  hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
                fig.update_layout(height=210, margin=dict(t=0,b=0,l=0,r=0),
                                  paper_bgcolor="white", legend=dict(font=dict(size=9)))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="sh">👥 CRM Leads by Campaign</div><div class="sb">', unsafe_allow_html=True)
                ld = camp_df[camp_df["CRM Leads"]>0].sort_values("CRM Leads")
                f2 = px.bar(ld, x="CRM Leads", y="Campaign Objective", orientation="h",
                            color="Campaign Objective", color_discrete_sequence=COLORS, text="CRM Leads")
                f2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                f2.update_layout(height=210, margin=dict(t=0,b=0,l=0,r=45), showlegend=False,
                                 paper_bgcolor="white", plot_bgcolor="white",
                                 xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False))
                st.plotly_chart(f2, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with c3:
                st.markdown('<div class="sh">💰 Sales by Campaign</div><div class="sb">', unsafe_allow_html=True)
                sd = camp_df[camp_df["Sales Amount ($)"]>0].sort_values("Sales Amount ($)")
                f3 = px.bar(sd, x="Sales Amount ($)", y="Campaign Objective", orientation="h",
                            color="Campaign Objective", color_discrete_sequence=COLORS, text="Sales Amount ($)")
                f3.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
                f3.update_layout(height=210, margin=dict(t=0,b=0,l=0,r=65), showlegend=False,
                                 paper_bgcolor="white", plot_bgcolor="white",
                                 xaxis=dict(showgrid=False,visible=False), yaxis=dict(showgrid=False))
                st.plotly_chart(f3, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f'<div class="sh">📋 Campaign Breakdown — {sel}</div><div class="sb">', unsafe_allow_html=True)
            show = ["Campaign Objective","Spend ($)","Impressions","Clicks","CRM Leads",
                    "Conversions","Appointments","Customers","Sales Amount ($)","ROAS"]
            tb = fd[[c for c in show if c in fd.columns]].copy()
            tb["Spend ($)"]        = tb["Spend ($)"].apply(fc)
            tb["Impressions"]      = tb["Impressions"].apply(fn)
            tb["Clicks"]           = tb["Clicks"].apply(fn)
            tb["CRM Leads"]        = tb["CRM Leads"].apply(lambda x: fn(x) if x>0 else "—")
            tb["Conversions"]      = tb["Conversions"].apply(lambda x: fn(x) if x>0 else "—")
            tb["Appointments"]     = tb["Appointments"].apply(fn)
            tb["Customers"]        = tb["Customers"].apply(lambda x: fn(x) if x>0 else "—")
            tb["Sales Amount ($)"] = tb["Sales Amount ($)"].apply(lambda x: fc(x) if x>0 else "—")
            tb["ROAS"]             = tb["ROAS"].apply(lambda x: f"{x:.1f}x" if x>0 else "—")
            st.dataframe(tb, use_container_width=True, hide_index=True, height=180)
            st.markdown("</div>", unsafe_allow_html=True)

    # ══ PAGE 2 — TRENDS ════════════════════════════════════════════════════════
    elif st.session_state.page == "trends":

        if "Daily Performance" not in data:
            st.warning("No Daily Performance sheet found."); st.stop()

        daily = data["Daily Performance"].copy()
        daily["Date"] = pd.to_datetime(daily["Date"])
        if date_range and len(date_range)==2:
            daily = daily[(daily["Date"]>=pd.Timestamp(date_range[0])) &
                          (daily["Date"]<=pd.Timestamp(date_range[1]))]
        if sel_camp != "All Campaigns" and "Campaign" in daily.columns:
            daily = daily[daily["Campaign"]==sel_camp]

        agg = daily.groupby("Date").agg({
            "Spend ($)":"sum","Impressions":"sum","Reach":"sum","Clicks":"sum",
            "CRM Leads":"sum","Conversions":"sum","Appointments":"sum",
            "Customers":"sum","Sales Amount ($)":"sum","ROAS":"mean"
        }).reset_index()

        gc = st.columns([1,1,1,5])
        for label, key in [("Daily","Daily"),("Weekly","Weekly"),("Monthly","Monthly")]:
            if gc[["Daily","Weekly","Monthly"].index(label)].button(
                label, key=f"g{label[0].lower()}", use_container_width=True,
                type="primary" if st.session_state.gran==label else "secondary"):
                st.session_state.gran=label; st.rerun()

        if st.session_state.gran=="Weekly":  agg = agg.resample("W", on="Date").sum().reset_index()
        if st.session_state.gran=="Monthly": agg = agg.resample("ME",on="Date").sum().reset_index()

        mopts  = ["Spend ($)","Sales Amount ($)","CRM Leads","Clicks","Conversions","Appointments","Customers","ROAS"]
        mshort = ["Spend","Sales","Leads","Clicks","Conv.","Appt.","Cust.","ROAS"]
        mdefs  = [True,True,True,False,False,False,False,False]
        mc = st.columns(8)
        sel_m = [m for i,(m,s,d) in enumerate(zip(mopts,mshort,mdefs))
                 if mc[i].checkbox(s, value=d, key=f"mx{i}")]

        if sel_m:
            st.markdown('<div class="sh">📈 Metrics Over Time</div><div class="sb">', unsafe_allow_html=True)
            fm = go.Figure()
            for m,col in zip(sel_m,COLORS):
                if m not in agg.columns: continue
                fm.add_trace(go.Scatter(x=agg["Date"],y=agg[m],name=m,mode="lines+markers",
                    line=dict(color=col,width=2),marker=dict(size=3),
                    hovertemplate=f"<b>%{{x|%b %d}}</b><br>{m}: %{{y:,.1f}}<extra></extra>"))
            fm.update_layout(**ch(230))
            st.plotly_chart(fm, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        r1,r2 = st.columns(2)
        with r1:
            st.markdown('<div class="sh">💹 ROAS Trend</div><div class="sb">', unsafe_allow_html=True)
            fr = go.Figure(go.Scatter(x=agg["Date"],y=agg["ROAS"],mode="lines+markers",
                line=dict(color="#22c55e",width=2),fill="tozeroy",fillcolor="rgba(34,197,94,0.07)",
                hovertemplate="ROAS: %{y:.2f}x<extra></extra>"))
            fr.update_layout(height=190,margin=dict(t=6,b=28,l=42,r=8),
                paper_bgcolor="white",plot_bgcolor="white",
                xaxis=dict(showgrid=False,tickformat="%b %d"),
                yaxis=dict(showgrid=True,gridcolor="#f3f4f6",ticksuffix="x"))
            st.plotly_chart(fr, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="sh">💸 Spend vs Sales</div><div class="sb">', unsafe_allow_html=True)
            fsv = make_subplots(specs=[[{"secondary_y":True}]])
            fsv.add_trace(go.Bar(x=agg["Date"],y=agg["Spend ($)"],name="Spend",
                marker_color="rgba(24,119,242,0.65)",hovertemplate="$%{y:,.0f}<extra></extra>"),secondary_y=False)
            fsv.add_trace(go.Scatter(x=agg["Date"],y=agg["Sales Amount ($)"],name="Sales",
                line=dict(color="#22c55e",width=2),hovertemplate="$%{y:,.0f}<extra></extra>"),secondary_y=True)
            fsv.update_layout(height=190,margin=dict(t=6,b=28,l=42,r=42),
                paper_bgcolor="white",plot_bgcolor="white",
                legend=dict(orientation="h",y=1.1),hovermode="x unified",
                xaxis=dict(showgrid=False,tickformat="%b %d"))
            fsv.update_yaxes(showgrid=True,gridcolor="#f3f4f6",secondary_y=False)
            fsv.update_yaxes(showgrid=False,secondary_y=True)
            st.plotly_chart(fsv, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        r3,r4 = st.columns(2)
        with r3:
            st.markdown('<div class="sh">📡 Impressions & Reach</div><div class="sb">', unsafe_allow_html=True)
            fa = go.Figure()
            fa.add_trace(go.Scatter(x=agg["Date"],y=agg["Impressions"],name="Impressions",line=dict(color="#1877F2",width=2)))
            fa.add_trace(go.Scatter(x=agg["Date"],y=agg["Reach"],name="Reach",line=dict(color="#8b5cf6",width=2,dash="dash")))
            fa.update_layout(**ch(185))
            st.plotly_chart(fa, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with r4:
            st.markdown('<div class="sh">🎯 Conversion Funnel</div><div class="sb">', unsafe_allow_html=True)
            fcv = go.Figure()
            for m,col in [("Conversions","#10b981"),("Appointments","#06b6d4"),("Customers","#ec4899")]:
                fcv.add_trace(go.Scatter(x=agg["Date"],y=agg[m],name=m,line=dict(color=col,width=2)))
            fcv.update_layout(**ch(185))
            st.plotly_chart(fcv, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ══ PAGE 3 — BY TERRITORY ══════════════════════════════════════════════════
    elif st.session_state.page == "territory":

        if "Territory Performance" not in data:
            st.warning("No Territory Performance sheet found."); st.stop()

        raw = data["Territory Performance"].copy()
        t3c = ["All Campaigns"]+sorted(raw["Campaign"].unique().tolist())
        s3  = st.selectbox("Campaign", t3c, key="t3c", label_visibility="collapsed")
        tdf = raw if s3=="All Campaigns" else raw[raw["Campaign"]==s3]

        terr = tdf.groupby("Territory").agg({
            "Unique Leads":"sum","New Leads":"sum","Appointments":"sum","Quote":"sum",
            "Customers":"sum","Sales Amount ($)":"sum","NL Customers":"sum",
            "NL Sales ($)":"sum","Spend ($)":"sum","ROAS":"mean"
        }).reset_index()
        tot = terr.sum(numeric_only=True)
        terr["Leads %"]     = (terr["Unique Leads"]    /tot["Unique Leads"]     *100).round(2)
        terr["Sales %"]     = (terr["Sales Amount ($)"]/tot["Sales Amount ($)"] *100).round(2)
        terr["APT/Leads"]   = (terr["Appointments"]    /terr["Unique Leads"].replace(0,1)*100).round(2)
        terr["Order/APT"]   = (terr["Customers"]       /terr["Appointments"].replace(0,1)*100).round(2)
        terr["Order/Leads"] = (terr["Customers"]       /terr["Unique Leads"].replace(0,1)*100).round(2)
        terr = terr.sort_values("Sales Amount ($)",ascending=False)

        ul=int(tot["Unique Leads"]); apt=int(tot["Appointments"])
        cu=int(tot["Customers"]);    sal=tot["Sales Amount ($)"]
        ap=round(apt/ul*100) if ul else 0

        st.markdown(f"""
        <div class="tstrip">
          <div class="tcell"><span class="ttop" style="background:#1877F2"></span>
            <div class="tl">Total Leads</div><div class="tv">{ul:,}</div></div>
          <div class="tcell"><span class="ttop" style="background:#10b981"></span>
            <div class="tl">Appointments</div><div class="tv">{apt:,}</div></div>
          <div class="tcell"><span class="ttop" style="background:#8b5cf6"></span>
            <div class="tl">Customers</div><div class="tv">{cu:,}</div></div>
          <div class="tcell"><span class="ttop" style="background:#22c55e"></span>
            <div class="tl">Total Sales</div><div class="tv">{fc(sal)}</div></div>
          <div class="tcell"><span class="ttop" style="background:#f59e0b"></span>
            <div class="tl">APT / Leads</div><div class="tv">{ap}%</div></div>
        </div>""", unsafe_allow_html=True)

        d1,d2 = st.columns(2)
        with d1:
            st.markdown('<div class="sh">🥧 Leads % of Total</div><div class="sb">', unsafe_allow_html=True)
            fl = px.pie(terr,values="Unique Leads",names="Territory",hole=0.42,color_discrete_sequence=COLORS)
            fl.update_traces(textposition="inside",textinfo="percent",
                             hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>")
            fl.update_layout(height=280,margin=dict(t=5,b=5,l=0,r=0),
                             paper_bgcolor="white",legend=dict(font=dict(size=9)))
            st.plotly_chart(fl, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with d2:
            st.markdown('<div class="sh">💰 Sales % of Total</div><div class="sb">', unsafe_allow_html=True)
            fs = px.pie(terr[terr["Sales Amount ($)"]>0],values="Sales Amount ($)",
                        names="Territory",hole=0.42,color_discrete_sequence=COLORS)
            fs.update_traces(textposition="inside",textinfo="percent",
                             hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>")
            fs.update_layout(height=280,margin=dict(t=5,b=5,l=0,r=0),
                             paper_bgcolor="white",legend=dict(font=dict(size=9)))
            st.plotly_chart(fs, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sh">🏢 Regional Office Performance</div><div class="sb">', unsafe_allow_html=True)
        disp = terr[["Territory","Unique Leads","New Leads","Appointments","Quote",
                     "Customers","Sales Amount ($)","NL Customers","NL Sales ($)",
                     "Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]].copy()
        tr_r = pd.DataFrame([{
            "Territory":"Total","Unique Leads":int(tot["Unique Leads"]),
            "New Leads":int(tot["New Leads"]),"Appointments":int(tot["Appointments"]),
            "Quote":int(tot["Quote"]),"Customers":int(tot["Customers"]),
            "Sales Amount ($)":tot["Sales Amount ($)"],"NL Customers":int(tot["NL Customers"]),
            "NL Sales ($)":tot["NL Sales ($)"],"Leads %":100.0,"Sales %":100.0,
            "APT/Leads":round(tot["Appointments"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0,
            "Order/APT":round(tot["Customers"]/tot["Appointments"]*100,2) if tot["Appointments"] else 0,
            "Order/Leads":round(tot["Customers"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0}])
        disp = pd.concat([disp,tr_r],ignore_index=True)
        for c in ["Sales Amount ($)","NL Sales ($)"]: disp[c]=disp[c].apply(lambda x:f"${x:,.2f}")
        for c in ["Leads %","Sales %","APT/Leads","Order/Leads"]: disp[c]=disp[c].apply(lambda x:f"{x:.2f}")
        disp["Order/APT"]=disp["Order/APT"].apply(lambda x:f"{x:.0f}%")
        disp.columns=["Regional Office","Unique Leads","New Leads","APT","Quote","Customers",
                      "Sales Amount","NL Customers","NL Sales","Leads %","Sales %",
                      "APT/Leads","Order/APT","Order/Leads"]
        st.dataframe(disp,use_container_width=True,hide_index=True,height=380)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sh">📊 Campaign Breakdown by Territory</div><div class="sb">', unsafe_allow_html=True)
        tc = raw.copy()
        if sel_off!="All": tc=tc[tc["Territory"]==sel_off]
        pm = st.selectbox("Metric",["Sales Amount ($)","Unique Leads","Appointments","Customers","Spend ($)"],
                          key="pm",label_visibility="collapsed")
        fg = px.bar(tc.sort_values("Territory"),x="Territory",y=pm,color="Campaign",
                    barmode="group",color_discrete_sequence=COLORS,text_auto=".2s")
        fg.update_layout(height=280,margin=dict(t=6,b=70,l=50,r=8),
                         paper_bgcolor="white",plot_bgcolor="white",
                         xaxis=dict(showgrid=False,tickangle=-30),
                         yaxis=dict(showgrid=True,gridcolor="#f3f4f6"),
                         legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        st.plotly_chart(fg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
