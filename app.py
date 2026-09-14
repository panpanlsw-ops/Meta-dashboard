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

st.markdown("""
<style>
#MainMenu, footer { display:none!important }
[data-testid="stSidebar"] { display:none!important }
[data-testid="collapsedControl"] { display:none!important }
header[data-testid="stHeader"] { display:none!important }
[data-testid="collapsedControl"] { display:none!important }

/* ── Black sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background-color: #111111 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #777777 !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stSidebar"] label { color: #cccccc !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1e1e1e !important;
    border-color: #333 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div { color: white !important; }
[data-testid="stSidebar"] input { background: #1e1e1e !important; color: white !important; }
[data-testid="stSidebar"] hr { border-color: #333 !important; }

/* ── Nav buttons ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #aaaaaa !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #1877F2 !important;
    color: white !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

LS_B64 = "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"

COLORS = ["#1877F2","#10b981","#f59e0b","#8b5cf6","#ef4444",
          "#06b6d4","#f97316","#ec4899","#22c55e","#a78bfa"]

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
    a="▲" if v>0 else "▼"
    good=(pg and v>0) or (not pg and v<0)
    col="#10b981" if good else "#ef4444"
    return f'<span style="font-size:0.72rem;font-weight:600;color:{col}">{a} {abs(v):.1f}%</span>'
def sh(t):
    return ('<div style="background:#1877F2;color:white;padding:8px 14px;' +
            f'border-radius:8px 8px 0 0;font-weight:600;font-size:0.82rem">{t}</div>')
def sb_o():
    return '<div style="background:white;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;padding:14px;margin-bottom:24px">'
def sb_c(): return "</div>"

@st.cache_data(ttl=1800)
def load_data():
    import gspread
    from google.oauth2.service_account import Credentials

    # Try Streamlit secrets first (for deployment)
    # Fall back to local JSON file (for local development)
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]
        )
    except Exception:
        creds = Credentials.from_service_account_file(
            "lsw-marketing-b9a13bd21034.json",
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]
        )

    gc = gspread.authorize(creds)
    sh = gc.open_by_key("1ZcB9ZiNuZ0a8CwCnqtxmg2pO_0OGk_Nu5icUhmPGF7s")

    def read_tab(name):
        records = sh.worksheet(name).get_all_records()
        return pd.DataFrame(records)

    return {
        "Campaign Performance":  read_tab("Campaign Performance"),
        "Territory Summary":     read_tab("Territory Summary"),
        "Territory Detail":      read_tab("Territory Detail"),
        "Overview":              read_tab("Overview"),
    }

def ch(h=210):
    return dict(height=h, margin=dict(t=8,b=32,l=50,r=12),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(showgrid=False, tickformat="%b %d"),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified")

for k,v in [("page","overview"),("t1c","All Campaigns"),("gran","Daily")]:
    if k not in st.session_state: st.session_state[k]=v

try:
    data = load_data()
    # Rename columns to match dashboard expectations
    def clean_numeric(df, cols):
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].astype(str)
                    .str.replace("[$,%]","",regex=True)
                    .str.strip(), errors="coerce").fillna(0)
        return df

    if "Campaign Performance" in data:
        data["Campaign Performance"] = data["Campaign Performance"].rename(columns={
            "Campaign":      "Campaign Objective",
            "Cost":          "Spend ($)",
            "unique_leads":  "CRM Leads",
            "new_leads":     "New Leads",
            "apt":           "Appointments",
            "sales_amount":  "Sales Amount ($)",
            "apt/lead":      "APT/Lead",
        })
        data["Campaign Performance"] = clean_numeric(
            data["Campaign Performance"],
            ["Spend ($)","CRM Leads","New Leads","Appointments",
             "Customers","Sales Amount ($)","Year","Month"])

    if "Territory Summary" in data:
        data["Territory Summary"] = data["Territory Summary"].rename(columns={
            "Region_Clean":  "Territory",
            "unique_leads":  "Unique Leads",
            "new_leads":     "New Leads",
            "apt":           "Appointments",
            "quote":         "Quote",
            "customers":     "Customers",
            "sales_amount":  "Sales Amount ($)",
            "leads_%":       "Leads %",
            "sales_%":       "Sales %",
            "apt/lead":      "APT/Leads",
            "order/lead":    "Order/Leads",
        })
        data["Territory Summary"] = clean_numeric(
            data["Territory Summary"],
            ["Unique Leads","New Leads","Appointments","Quote",
             "Customers","Sales Amount ($)","Year","Month"])

    if "Territory Detail" in data:
        data["Territory Detail"] = data["Territory Detail"].rename(columns={
            "Region_Clean":  "Territory",
            "unique_leads":  "Unique Leads",
            "new_leads":     "New Leads",
            "apt":           "Appointments",
            "quote":         "Quote",
            "customers":     "Customers",
            "sales_amount":  "Sales Amount ($)",
        })
        data["Territory Detail"] = clean_numeric(
            data["Territory Detail"],
            ["Unique Leads","New Leads","Appointments","Quote",
             "Customers","Sales Amount ($)","Year","Month"])

    if "Overview" in data:
        data["Overview"] = clean_numeric(
            data["Overview"],
            ["CRM Leads","Appointments","Customers",
             "Sales Amount ($)","Spend ($)","Year","Month"])

except Exception as e:
    data={}
    st.error(f"❌ Error loading data: {e}")
    st.stop()

camp_list = ["All"]
if "Campaign Performance" in data:
    camp_list += list(data["Campaign Performance"]["Campaign Objective"].unique())
off_list = ["All"]
if "Territory Performance" in data:
    off_list += sorted(data["Territory Summary"]["Territory"].unique().tolist())

# ════════════════════════════════════════════════════════════
# NAVIGATION & SHARED VARIABLES
# ════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "overview"

# Shared date variables (used by overview and trends)
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
all_years = []
if "Campaign Performance" in data:
    cp = data["Campaign Performance"]
    if "Year" in cp.columns:
        all_years = sorted([int(y) for y in cp["Year"].dropna().unique().tolist()])
if not all_years:
    all_years = [2024, 2025, 2026]

from_month = MONTHS[0]
from_year  = all_years[0]
to_month   = MONTHS[-1]
to_year    = all_years[-1]
from_m     = 1
to_m       = 12
sel_camp   = "All"
sel_off    = "All"

# ── Top Header ────────────────────────────────────────────
from datetime import date as _dt
_today_str = _dt.today().strftime("%a, %b %d %Y")

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:12px 0;margin-bottom:0;border-bottom:1px solid #e5e7eb">
  <div style="display:flex;align-items:center;gap:10px">
    <div style="background:#1877F2;border-radius:8px;width:36px;height:36px;
                display:flex;align-items:center;justify-content:center;flex-shrink:0">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 24" height="16">
        <path d="M2 12C2 7.2 5.2 3 9.2 3c2.2 0 4.2 1.2 5.8 3.3C16.6 4.2 18.6 3 20.6 3
        c4 0 7.2 4.2 7.2 9 0 2.5-.8 4.8-2.1 6.4-1.2 1.4-2.7 2.2-4.3 2.2
        -2 0-3.6-1-5.6-3.9-2 2.9-3.6 3.9-5.6 3.9-1.6 0-3.1-.8-4.3-2.2
        C2.8 16.8 2 14.5 2 12z" fill="white"/>
      </svg>
    </div>
    <div>
      <div style="font-size:1rem;font-weight:700;color:#111827">Meta Ads Dashboard</div>
      <div style="font-size:0.75rem;color:#6b7280">LifeSource Water</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:0.82rem;color:#6b7280">{_today_str}</span>
    {'<button onclick="window.location.reload()" style="background:#f3f4f6;border:1px solid #e5e7eb;border-radius:6px;padding:5px 12px;font-size:0.78rem;cursor:pointer;color:#374151">🔄 Refresh</button>' if False else ''}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Hidden refresh (cache auto-refreshes every 30 min) ────
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ── Tab navigation ────────────────────────────────────────
tabs_def = [("overview","📊 MTD Overview"),("territory","🗺️ By Territory"),("trends","📈 Trends")]
t1,t2,t3 = st.tabs([label for _,label in tabs_def])

# ════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════
with t1:

    if "Overview" in data:
        ov_all = data["Overview"].copy()
        ov_all["Year"]  = pd.to_numeric(ov_all["Year"],  errors="coerce").fillna(0).astype(int)
        ov_all["Month"] = pd.to_numeric(ov_all["Month"], errors="coerce").fillna(0).astype(int)
        for col in ["CRM Leads","Appointments","Customers","Sales Amount ($)","Spend ($)"]:
            if col in ov_all.columns:
                ov_all[col] = pd.to_numeric(ov_all[col], errors="coerce").fillna(0)
        # MTD Overview always shows current month only
        from datetime import date as _date_ov
        _now = _date_ov.today()
        ov = ov_all[(ov_all["Year"] == _now.year) & (ov_all["Month"] == _now.month)]
        if len(ov) == 0:  # fallback to latest available month
            ov = ov_all[ov_all["Year"] == ov_all["Year"].max()]
            ov = ov[ov["Month"] == ov["Month"].max()]
        ov_sum = ov[["CRM Leads","Appointments","Customers","Sales Amount ($)","Spend ($)"]].sum()

        import calendar
        from datetime import date as _date
        _today = _date.today()
        # Only show pace bar if selected range includes current month
        # Only show pace when BOTH from and to are current month
        _is_current_month = (
            to_year == _today.year and to_m == _today.month and
            from_year == _today.year and from_m == _today.month
        )
        _days_in_month = calendar.monthrange(_today.year, _today.month)[1]
        _days_elapsed = max(_today.day - 1, 1)
        _pct = round(_days_elapsed / _days_in_month * 100)

        def kp(m, color, cur=False):
            if m not in ov_sum.index:
                return (f'<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;padding:14px 14px 12px;position:relative;overflow:hidden">' +
                        f'<div style="position:absolute;top:0;left:0;right:0;height:4px;border-radius:10px 10px 0 0;background:{color}"></div>' +
                        f'<div style="font-size:0.58rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">{m}</div>' +
                        '<div style="font-size:1.3rem;font-weight:500;color:#111827;margin-bottom:8px">—</div></div>')
            raw = ov_sum[m]
            v = fc(raw) if cur else fn(raw)
            if _is_current_month:
                paced = raw / _days_elapsed * _days_in_month
                pv = fc(paced) if cur else fn(paced)
                pace_html = (f'<div style="font-size:0.72rem;font-weight:600;color:#374151;margin-bottom:4px">{pv} pace</div>' +
                             f'<div style="height:4px;background:#f3f4f6;border-radius:3px;overflow:hidden">' +
                             f'<div style="height:100%;width:{_pct}%;background:{color};border-radius:3px"></div></div>')
            else:
                pace_html = ""
            return (f'<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;padding:14px 14px 12px;position:relative;overflow:hidden">' +
                    f'<div style="position:absolute;top:0;left:0;right:0;height:4px;border-radius:10px 10px 0 0;background:{color}"></div>' +
                    f'<div style="font-size:0.58rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">{m}</div>' +
                    f'<div style="font-size:1.3rem;font-weight:500;color:#111827;margin-bottom:8px">{v}</div>' +
                    pace_html + '</div>')

        st.markdown(
            '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:26px">'+
            kp("CRM Leads","#1877F2")+kp("Appointments","#f59e0b")+
            kp("Customers","#06b6d4")+kp("Spend ($)","#ec4899",True)+
            kp("Sales Amount ($)","#22c55e",True)+
            '</div>', unsafe_allow_html=True)


    if "Campaign Performance" in data:
        camp_df=data["Campaign Performance"].copy()
        # Filter to current month only for MTD Overview
        from datetime import date as _dt_c
        _now_c = _dt_c.today()
        if "Year" in camp_df.columns and "Month" in camp_df.columns:
            camp_df["Year"]  = pd.to_numeric(camp_df["Year"],  errors="coerce").fillna(0).astype(int)
            camp_df["Month"] = pd.to_numeric(camp_df["Month"], errors="coerce").fillna(0).astype(int)
            _filtered = camp_df[(camp_df["Year"]==_now_c.year) & (camp_df["Month"]==_now_c.month)]
            if len(_filtered) > 0:
                camp_df = _filtered
            else:
                max_yr = camp_df["Year"].max()
                max_mo = camp_df[camp_df["Year"]==max_yr]["Month"].max()
                camp_df = camp_df[(camp_df["Year"]==max_yr)&(camp_df["Month"]==max_mo)]
        camp_df = camp_df.groupby("Campaign Objective").agg({
            "Spend ($)":"sum","CRM Leads":"sum",
            "Appointments":"sum","Customers":"sum","Sales Amount ($)":"sum"
        }).reset_index()
        opts=["All Campaigns"]+list(camp_df["Campaign Objective"].unique())
        sel = "All Campaigns"
        fd  = camp_df
        c1,c2,c3=st.columns(3,gap="medium")
        with c1:
            st.markdown(sh("💸 Spend by Campaign")+sb_o(),unsafe_allow_html=True)
            fig=px.pie(camp_df,values="Spend ($)",names="Campaign Objective",hole=0.42,color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside",textinfo="percent",hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
            fig.update_layout(height=280,margin=dict(t=0,b=0,l=0,r=0),paper_bgcolor="white",legend=dict(font=dict(size=9)))
            st.plotly_chart(fig,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        with c2:
            st.markdown(sh("👥 CRM Leads by Campaign")+sb_o(),unsafe_allow_html=True)
            ld=camp_df[camp_df["CRM Leads"]>0].sort_values("CRM Leads")
            f2=px.bar(ld,x="CRM Leads",y="Campaign Objective",orientation="h",color="Campaign Objective",color_discrete_sequence=COLORS,text="CRM Leads")
            f2.update_traces(texttemplate="%{text:,.0f}",textposition="outside")
            f2.update_layout(height=280,margin=dict(t=0,b=0,l=0,r=45),showlegend=False,paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,visible=False),yaxis=dict(showgrid=False))
            st.plotly_chart(f2,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        with c3:
            st.markdown(sh("💰 Sales by Campaign")+sb_o(),unsafe_allow_html=True)
            sd=camp_df[camp_df["Sales Amount ($)"]>0].sort_values("Sales Amount ($)")
            f3=px.bar(sd,x="Sales Amount ($)",y="Campaign Objective",orientation="h",color="Campaign Objective",color_discrete_sequence=COLORS,text="Sales Amount ($)")
            f3.update_traces(texttemplate="$%{text:,.0f}",textposition="outside")
            f3.update_layout(height=280,margin=dict(t=0,b=0,l=0,r=65),showlegend=False,paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,visible=False),yaxis=dict(showgrid=False))
            st.plotly_chart(f3,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        st.markdown(sh(f"📋 Campaign Breakdown — {sel}")+sb_o(),unsafe_allow_html=True)
        show=["Campaign Objective","Spend ($)","CRM Leads","Appointments","Customers","Sales Amount ($)","ROI","APT/Lead"]
        tb=fd[[c for c in show if c in fd.columns]].copy()
        # Compute Cost/APT and APT/Leads before formatting
        raw = fd.copy()
        tb["Cost/APT"] = raw.apply(lambda r: fc(r["Spend ($)"]/r["Appointments"]) if pd.notna(r.get("Appointments")) and r["Appointments"]>0 else "—", axis=1)
        tb["APT/Leads"] = raw.apply(lambda r: f'{r["Appointments"]/r["CRM Leads"]*100:.1f}%' if pd.notna(r.get("CRM Leads")) and r["CRM Leads"]>0 and pd.notna(r.get("Appointments")) and r["Appointments"]>0 else "—", axis=1)
        tb["Spend ($)"]=tb["Spend ($)"].apply(fc)
        for col in ["CRM Leads","Customers"]:
            if col in tb.columns:
                tb[col]=tb[col].apply(lambda x:fn(x) if x>0 else "—")
        if "Appointments" in tb.columns:
            tb["Appointments"]=tb["Appointments"].apply(fn)
        if "Sales Amount ($)" in tb.columns:
            tb["Sales Amount ($)"]=tb["Sales Amount ($)"].apply(lambda x:fc(x) if x>0 else "—")
        st.dataframe(tb,use_container_width=True,hide_index=True,height=min(600,(len(tb)+1)*35+50)); st.markdown(sb_c(),unsafe_allow_html=True)

with t2:

    if "Territory Summary" not in data:
        st.warning("No Territory Summary sheet found."); st.stop()

    raw = data["Territory Summary"].copy()

    # ── Date filters on top ───────────────────────────────────────
    st.markdown("<style>.stSelectbox>div>div{background:white!important;color:#111827!important}</style>", unsafe_allow_html=True)
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    all_years = sorted(raw["Year"].dropna().unique().tolist()) if "Year" in raw.columns else [2026]
    all_years = [int(y) for y in all_years if str(y).strip() not in ["","nan"]]

    dc1,dc2,dc3,dc4,dc5 = st.columns([2,2,0.3,2,2])
    with dc1:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>From Month</p>", unsafe_allow_html=True)
        t_from_month = st.selectbox("FM", MONTHS, index=0, label_visibility="collapsed", key="t_from_month")
    with dc2:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>From Year</p>", unsafe_allow_html=True)
        t_from_year = st.selectbox("FY", all_years, index=0, label_visibility="collapsed", key="t_from_year")
    with dc3:
        st.markdown("<p style='margin-top:22px;color:#6b7280;font-size:13px'>to</p>", unsafe_allow_html=True)
    with dc4:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>To Month</p>", unsafe_allow_html=True)
        t_to_month = st.selectbox("TM", MONTHS, index=len(MONTHS)-1, label_visibility="collapsed", key="t_to_month")
    with dc5:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>To Year</p>", unsafe_allow_html=True)
        t_to_year = st.selectbox("TY", all_years, index=len(all_years)-1, label_visibility="collapsed", key="t_to_year")

    t_from_m = MONTHS.index(t_from_month) + 1
    t_to_m   = MONTHS.index(t_to_month) + 1
    t_from_year = int(t_from_year)
    t_to_year   = int(t_to_year)

    dr_label = f"{t_from_month} {t_from_year} – {t_to_month} {t_to_year}"
    st.markdown(f"<p style='font-size:0.78rem;color:#6b7280;margin-bottom:14px'>Showing: {dr_label}</p>", unsafe_allow_html=True)

    # ── Filter data ───────────────────────────────────────────────
    tdf = raw.copy()
    tdf["Year"]  = pd.to_numeric(tdf["Year"],  errors="coerce").fillna(0).astype(int)
    tdf["Month"] = pd.to_numeric(tdf["Month"], errors="coerce").fillna(0).astype(int)
    tdf = tdf[
        ((tdf["Year"] > t_from_year) |
         ((tdf["Year"] == t_from_year) & (tdf["Month"] >= t_from_m))) &
        ((tdf["Year"] < t_to_year) |
         ((tdf["Year"] == t_to_year) & (tdf["Month"] <= t_to_m)))
    ]

    # Aggregate by territory
    terr = tdf.groupby("Territory").agg({
        "Unique Leads":"sum","New Leads":"sum","Appointments":"sum","Quote":"sum",
        "Customers":"sum","Sales Amount ($)":"sum",
    }).reset_index()
    tot = terr.sum(numeric_only=True)

    # Calculate % from raw numbers
    total_leads = tot["Unique Leads"]     if tot["Unique Leads"]     else 1
    total_sales = tot["Sales Amount ($)"] if tot["Sales Amount ($)"] else 1
    terr["Leads %"]     = (terr["Unique Leads"]     / total_leads * 100).round(2)
    terr["Sales %"]     = (terr["Sales Amount ($)"] / total_sales * 100).round(2)
    terr["APT/Leads"]   = (terr["Appointments"]     / terr["Unique Leads"].replace(0,1)   * 100).round(2)
    terr["Order/APT"]   = (terr["Customers"]        / terr["Appointments"].replace(0,1)   * 100).round(2)
    terr["Order/Leads"] = (terr["Customers"]        / terr["Unique Leads"].replace(0,1)   * 100).round(2)
    terr = terr.sort_values(["Unique Leads","Sales Amount ($)"], ascending=[False,False])

    ul  = int(tot["Unique Leads"])
    apt = int(tot["Appointments"])
    cu  = int(tot["Customers"])
    sal = tot["Sales Amount ($)"]
    ap  = round(apt/ul*100) if ul else 0

    # ── KPI strip ─────────────────────────────────────────────────
    def tcell(color, label, value):
        return (f'<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;padding:14px;position:relative">' +
                f'<div style="height:3px;border-radius:3px;background:{color};margin-bottom:8px"></div>' +
                f'<div style="font-size:0.62rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:5px">{label}</div>' +
                f'<div style="font-size:1.3rem;font-weight:700;color:#111827">{value}</div></div>')

    st.markdown(
        '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:20px">' +
        tcell("#1877F2","Total Leads",  fn(ul))  +
        tcell("#06b6d4","Appointments", fn(apt)) +
        tcell("#ec4899","Customers",    fn(cu))  +
        tcell("#22c55e","Total Sales",  fc(sal)) +
        tcell("#f59e0b","APT / Leads",  f"{ap}%") +
        '</div>', unsafe_allow_html=True)

    # ── Table header ──────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">' +
        f'<span style="font-size:0.9rem;font-weight:600;color:#111827">Regional Office Performance</span>' +
        f'<span style="font-size:0.72rem;color:#6b7280;background:#f3f4f6;padding:3px 10px;border-radius:20px">{dr_label}</span>' +
        f'</div>', unsafe_allow_html=True)

    # ── HTML table with progress bars ─────────────────────────────
    import streamlit.components.v1 as components

    def bar(pct, color):
        w = min(float(pct), 100)
        return (f'<div style="display:flex;align-items:center;gap:4px">' +
                f'<div style="width:50px;height:3px;background:#e5e7eb;border-radius:3px;flex-shrink:0">' +
                f'<div style="width:{w}%;height:100%;background:{color};border-radius:3px"></div></div>' +
                f'<span style="font-size:10.5px;color:#374151">{pct:.1f}%</span></div>')

    al_tot = round(tot["Appointments"]/tot["Unique Leads"]*100,1) if tot["Unique Leads"] else 0
    oa_tot = round(tot["Customers"]/tot["Appointments"]*100,1)   if tot["Appointments"] else 0
    ol_tot = round(tot["Customers"]/tot["Unique Leads"]*100,1)   if tot["Unique Leads"] else 0

    html = """<style>
    body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    table{width:100%;border-collapse:collapse;font-size:11.5px;background:white;
          border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
    thead tr{background:#111827}
    thead th{color:white;padding:9px 7px;text-align:left;font-weight:500;
             font-size:10px;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
    tbody tr{border-bottom:1px solid #f3f4f6;cursor:pointer}
    tbody tr:hover td{background:#f0f7ff}
    tbody td{padding:8px 7px;color:#111827;white-space:nowrap}
    tbody tr.tot td{background:#EBF3FF;color:#1e3a5f;font-weight:600;border-bottom:2px solid #bfdbfe}
    tbody tr.open{background:#EBF3FF}
    tbody tr.camp{background:#f5f8ff;border-bottom:1px solid #eff0f6}
    tbody tr.camp td{font-size:11px;color:#374151}
    tbody tr.camp td:first-child{padding-left:28px;color:#111827}
    .arrow{display:inline-block;font-size:9px;color:#9ca3af;margin-right:4px;transition:transform 0.15s}
    .arrow.open{transform:rotate(90deg)}
    </style>
    <table><thead><tr>
      <th>Regional Office</th>
      <th>Unique Leads</th><th>New Leads</th><th>APT</th><th>Quote</th>
      <th>Customers</th><th>Sales Amount</th>
      <th>Leads %</th><th>Sales %</th>
      <th>APT/Leads</th><th>Order/APT</th><th>Order/Leads</th>
    </tr></thead><tbody>"""

    # Total row
    html += (f'<tr class="tot"><td><b>Total</b></td>' +
             f'<td>{fn(tot["Unique Leads"])}</td><td>{fn(tot["New Leads"])}</td>' +
             f'<td>{fn(tot["Appointments"])}</td><td>{fn(tot.get("Quote",0))}</td>' +
             f'<td>{fn(tot["Customers"])}</td><td>{fc(tot["Sales Amount ($)"])}</td>' +
             f'<td>{bar(100,"#1877F2")}</td><td>{bar(100,"#22c55e")}</td>' +
             f'<td>{al_tot:.1f}%</td><td>{oa_tot:.1f}%</td><td>{ol_tot:.1f}%</td></tr>')

    # Territory rows with campaign breakdown
    t_detail = data.get("Territory Detail", pd.DataFrame())
    if not t_detail.empty and "Year" in t_detail.columns:
        t_detail["Year"]  = pd.to_numeric(t_detail["Year"],  errors="coerce").fillna(0).astype(int)
        t_detail["Month"] = pd.to_numeric(t_detail["Month"], errors="coerce").fillna(0).astype(int)
        t_detail = t_detail[
            ((t_detail["Year"] > t_from_year) |
             ((t_detail["Year"] == t_from_year) & (t_detail["Month"] >= t_from_m))) &
            ((t_detail["Year"] < t_to_year) |
             ((t_detail["Year"] == t_to_year) & (t_detail["Month"] <= t_to_m)))
        ]

    for idx, r in terr.iterrows():
        tid   = f"t{idx}"
        lp    = float(r.get("Leads %", 0))
        sp    = float(r.get("Sales %", 0))
        al    = float(r.get("APT/Leads", 0))
        oa    = float(r.get("Order/APT", 0))
        ol    = float(r.get("Order/Leads", 0))

        html += (f'<tr onclick="tog(\'{tid}\')" style="cursor:pointer">' +
                 f'<td><span class="arrow" id="{tid}-a">▶</span><b>{r["Territory"]}</b></td>' +
                 f'<td>{int(r["Unique Leads"])}</td><td>{int(r["New Leads"])}</td>' +
                 f'<td>{int(r["Appointments"])}</td><td>{int(r.get("Quote",0))}</td>' +
                 f'<td>{int(r["Customers"])}</td><td>{fc(r["Sales Amount ($)"])}</td>' +
                 f'<td>{bar(lp,"#1877F2")}</td><td>{bar(sp,"#22c55e")}</td>' +
                 f'<td>{al:.1f}%</td><td>{oa:.1f}%</td><td>{ol:.1f}%</td></tr>')

        # Campaign breakdown
        if not t_detail.empty and "Territory" in t_detail.columns:
            cd = t_detail[t_detail["Territory"]==r["Territory"]].groupby("Campaign").agg({
                "Unique Leads":"sum","New Leads":"sum","Appointments":"sum",
                "Quote":"sum","Customers":"sum","Sales Amount ($)":"sum"
            }).reset_index().sort_values("Unique Leads", ascending=False)

            t_ul = r["Unique Leads"] if r["Unique Leads"] else 1
            t_sa = r["Sales Amount ($)"] if r["Sales Amount ($)"] else 1

            for _, cr in cd.iterrows():
                c_lp = min(100, cr["Unique Leads"]     / t_ul * 100)
                c_sp = min(100, cr["Sales Amount ($)"] / t_sa * 100)
                c_al = cr["Appointments"]/cr["Unique Leads"]*100 if cr["Unique Leads"] else 0
                c_oa = cr["Customers"]/cr["Appointments"]*100    if cr["Appointments"] else 0
                c_ol = cr["Customers"]/cr["Unique Leads"]*100    if cr["Unique Leads"] else 0
                html += (f'<tr class="{tid}-camp" style="display:none">' +
                         f'<td style="padding-left:28px">{str(cr["Campaign"])}</td>' +
                         f'<td>{int(cr["Unique Leads"])}</td><td>{int(cr["New Leads"])}</td>' +
                         f'<td>{int(cr["Appointments"])}</td><td>{int(cr.get("Quote",0))}</td>' +
                         f'<td>{int(cr["Customers"])}</td><td>{fc(cr["Sales Amount ($)"])}</td>' +
                         f'<td>{bar(c_lp,"#1877F2")}</td><td>{bar(c_sp,"#22c55e")}</td>' +
                         f'<td>{c_al:.1f}%</td><td>{c_oa:.1f}%</td><td>{c_ol:.1f}%</td></tr>')

    html += """</tbody></table>
    <script>
    function tog(id){
      var rows=document.querySelectorAll('.'+id+'-camp');
      var arrow=document.getElementById(id+'-a');
      var open=rows[0]&&rows[0].style.display!=='none'&&rows[0].style.display!=='';
      rows.forEach(function(r){r.style.display=open?'none':'table-row';});
      if(arrow){arrow.classList.toggle('open',!open);}
    }
    </script>"""

    n_terr = len(terr)
    n_camp = sum(len(t_detail[t_detail["Territory"]==r["Territory"]]["Campaign"].unique())
                 for _,r in terr.iterrows()) if not t_detail.empty and "Territory" in t_detail.columns else 0
    tbl_height = max(400, (n_terr+2)*38 + n_camp*34)
    components.html(html, height=tbl_height, scrolling=True)

with t3:
    import json

    if "Campaign Performance" not in data:
        st.warning("No Campaign Performance data found."); st.stop()

    # ── Date filters ──────────────────────────────────────────────
    st.markdown("<style>.stSelectbox>div>div{background:white!important;color:#111827!important}</style>", unsafe_allow_html=True)
    MONTHS_T3 = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    all_years_t3 = sorted([int(y) for y in data["Campaign Performance"]["Year"].dropna().unique().tolist()])
    if not all_years_t3: all_years_t3 = [2026]

    tc1,tc2,tc3,tc4,tc5 = st.columns([2,2,0.3,2,2])
    with tc1:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>From Month</p>", unsafe_allow_html=True)
        t3_fm = st.selectbox("t3fm", MONTHS_T3, index=0, label_visibility="collapsed", key="t3_fm")
    with tc2:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>From Year</p>", unsafe_allow_html=True)
        t3_fy = st.selectbox("t3fy", all_years_t3, index=0, label_visibility="collapsed", key="t3_fy")
    with tc3:
        st.markdown("<p style='margin-top:22px;color:#6b7280;font-size:13px'>to</p>", unsafe_allow_html=True)
    with tc4:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>To Month</p>", unsafe_allow_html=True)
        t3_tm = st.selectbox("t3tm", MONTHS_T3, index=len(MONTHS_T3)-1, label_visibility="collapsed", key="t3_tm")
    with tc5:
        st.markdown("<p style='font-size:0.72rem;color:#6b7280;margin-bottom:3px'>To Year</p>", unsafe_allow_html=True)
        t3_ty = st.selectbox("t3ty", all_years_t3, index=len(all_years_t3)-1, label_visibility="collapsed", key="t3_ty")

    t3_from_m = MONTHS_T3.index(t3_fm) + 1
    t3_to_m   = MONTHS_T3.index(t3_tm) + 1
    t3_fy = int(t3_fy); t3_ty = int(t3_ty)
    st.caption(f"Showing: {t3_fm} {t3_fy} – {t3_tm} {t3_ty}")

    # ── Filter and aggregate data ─────────────────────────────────
    full_df = data["Campaign Performance"].copy()
    full_df["Year"]  = pd.to_numeric(full_df["Year"],  errors="coerce").fillna(0).astype(int)
    full_df["Month"] = pd.to_numeric(full_df["Month"], errors="coerce").fillna(0).astype(int)
    camp_col = "Campaign Objective" if "Campaign Objective" in full_df.columns else "Campaign"

    # Selected date range
    camp_df = full_df[
        ((full_df["Year"] > t3_fy) |
         ((full_df["Year"] == t3_fy) & (full_df["Month"] >= t3_from_m))) &
        ((full_df["Year"] < t3_ty) |
         ((full_df["Year"] == t3_ty) & (full_df["Month"] <= t3_to_m)))
    ].copy()

    # Aggregate by campaign
    num_cols = {c:"sum" for c in ["Spend ($)","CRM Leads","Appointments","Customers","Sales Amount ($)"] if c in camp_df.columns}
    camp_agg = camp_df.groupby(camp_col).agg(num_cols).reset_index()
    camp_agg["ROI"]       = camp_agg.apply(lambda r: (r["Sales Amount ($)"]-r["Spend ($)"])/r["Spend ($)"]*100 if r["Spend ($)"]>0 else 0, axis=1)
    camp_agg["APT/Lead"]  = camp_agg.apply(lambda r: r["Appointments"]/r["CRM Leads"]*100 if r["CRM Leads"]>0 else 0, axis=1)
    camp_agg["Order/APT"] = camp_agg.apply(lambda r: r["Customers"]/r["Appointments"]*100 if r["Appointments"]>0 else 0, axis=1)
    camp_agg["_roi_sort"] = camp_agg["ROI"]
    camp_agg = camp_agg.sort_values(["CRM Leads","Sales Amount ($)","_roi_sort"], ascending=[False,False,False]).drop(columns=["_roi_sort"])

    # Total row
    tot = camp_df.sum(numeric_only=True)
    tot_roi = (tot["Sales Amount ($)"]-tot["Spend ($)"])/tot["Spend ($)"]*100 if tot.get("Spend ($)",0)>0 else 0
    tot_al  = tot["Appointments"]/tot["CRM Leads"]*100 if tot.get("CRM Leads",0)>0 else 0
    tot_oa  = tot["Customers"]/tot["Appointments"]*100 if tot.get("Appointments",0)>0 else 0

    avg_al = camp_agg["APT/Lead"].mean()
    avg_oa = camp_agg["Order/APT"].mean()

    def f2(n):
        try:
            v = float(n)
            return "0" if v==0 else f"{v:,.1f}"
        except: return "0"

    def badge_t3(v, avg):
        c = "#065f46" if v>=avg else "#991b1b"
        b = "#d1fae5" if v>=avg else "#fee2e2"
        return f'<span style="background:{b};color:{c};padding:1px 5px;border-radius:3px;font-size:10px;font-weight:600;">{f2(v)}%</span>'

    # Build trend data for Chart.js
    # All months in selected range
    sel_months = []
    y, m = t3_fy, t3_from_m
    while (y < t3_ty) or (y == t3_ty and m <= t3_to_m):
        sel_months.append((y, m))
        m += 1
        if m > 12: m = 1; y += 1

    chart_labels = [f"{MONTHS_T3[mo-1]} {yr}" for yr, mo in sel_months]

    # Build trend for each campaign and total
    def get_trend(camp_name=None):
        d = {}
        for field, col in [("leads","CRM Leads"),("cost","Spend ($)"),("apt","Appointments"),("cust","Customers"),("sales","Sales Amount ($)")]:
            vals = []
            for yr, mo in sel_months:
                if camp_name:
                    sub = full_df[(full_df[camp_col]==camp_name) & (full_df["Year"]==yr) & (full_df["Month"]==mo)]
                else:
                    sub = full_df[(full_df["Year"]==yr) & (full_df["Month"]==mo)]
                vals.append(float(sub[col].sum()) if col in sub.columns else 0)
            d[field] = vals
        # ROI trend
        d["roi"] = [(s-c)/c*100 if c>0 else 0 for c,s in zip(d["cost"],d["sales"])]
        return d

    all_trends = {"__total__": get_trend()}
    for nm in camp_agg[camp_col].tolist():
        all_trends[nm] = get_trend(nm)

    chart_data_json = json.dumps({"labels": chart_labels, "trends": all_trends})

    # Table rows
    ts = "text-align:right;padding:6px 8px;border-bottom:0.5px solid #f3f4f6;font-size:12px;color:#374151;"

    def dr_t3(r):
        nm = str(r[camp_col]).replace("'","\\'")
        return (f'<tr style="cursor:pointer;" onclick="sel(this,\'{nm}\')">' +
            f'<td style="text-align:left;padding:6px 8px;border-bottom:0.5px solid #f3f4f6;font-weight:500;font-size:12px;">{r[camp_col]}</td>' +
            f'<td style="{ts}">${r["Spend ($)"]:,.0f}</td>' +
            f'<td style="{ts}">{int(r["CRM Leads"])}</td>' +
            f'<td style="{ts}">{int(r["Appointments"])}</td>' +
            f'<td style="{ts}">{int(r["Customers"])}</td>' +
            f'<td style="{ts}">${r["Sales Amount ($)"]:,.0f}</td>' +
            f'<td style="{ts}">{badge_t3(r["ROI"],0)}</td>' +
            f'<td style="{ts}">{badge_t3(r["APT/Lead"],avg_al)}</td>' +
            f'<td style="{ts}">{badge_t3(r["Order/APT"],avg_oa)}</td>' +
            f'</tr>')

    tbody = ('<tr style="background:#1f2937;color:#fff;font-weight:700;cursor:pointer;" onclick="sel(this,\'__total__\')">' +
             f'<td style="text-align:left;padding:7px 8px;font-size:12px;color:#fff;">📊 Total</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">${tot.get("Spend ($)",0):,.0f}</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{int(tot.get("CRM Leads",0))}</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{int(tot.get("Appointments",0))}</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{int(tot.get("Customers",0))}</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">${tot.get("Sales Amount ($)",0):,.0f}</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{f2(tot_roi)}%</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{f2(tot_al)}%</td>' +
             f'<td style="text-align:right;padding:6px 8px;font-size:12px;color:#fff;">{f2(tot_oa)}%</td>' +
             f'</tr>')

    tbody += "".join(dr_t3(r) for _, r in camp_agg.iterrows())

    html_part1 = """
<style>
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
table{width:100%;border-collapse:collapse;white-space:nowrap;font-size:12px;}
thead tr{background:#111827;}
th{padding:8px;font-size:10px;color:#9ca3af;text-transform:uppercase;text-align:right;letter-spacing:0.05em;}
th:first-child{text-align:left;color:#fff;}
tr.sel td{background:#dbeafe!important;}
.cb{background:#fff;border:0.5px solid #e5e7eb;border-radius:10px;padding:14px;margin-top:20px;}
.mt{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;}
.mb{font-size:11px;padding:4px 12px;border-radius:6px;border:0.5px solid #e5e7eb;cursor:pointer;background:#fff;color:#6b7280;font-weight:500;}
.mb.on{background:#111827;color:#fff;border-color:#111827;}
</style>
<div style="overflow-x:auto;">
<table>
<thead><tr>
<th style="text-align:left;color:#fff;min-width:200px;">Campaign</th>
<th>Cost</th><th>Leads</th><th>APT</th><th>Customers</th>
<th>Sales</th><th>ROI</th><th>APT/Lead</th><th>Order/APT</th>
</tr></thead>
<tbody id="tb">""" + tbody + """</tbody>
</table></div>
<div class="cb">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <b id="ctitle" style="font-size:13px;">📊 Total — Trend</b>
    <div style="font-size:11px;color:#6b7280;">
      <span style="display:inline-block;width:10px;height:3px;background:#1877F2;margin-right:4px;vertical-align:middle;"></span>This period
    </div>
  </div>
  <div class="mt">
    <button class="mb on" onclick="sm('leads',this)">Leads</button>
    <button class="mb" onclick="sm('cost',this)">Spend</button>
    <button class="mb" onclick="sm('apt',this)">APT</button>
    <button class="mb" onclick="sm('cust',this)">Customers</button>
    <button class="mb" onclick="sm('sales',this)">Sales</button>
    <button class="mb" onclick="sm('roi',this)">ROI %</button>
  </div>
  <div style="position:relative;height:260px;"><canvas id="cc"></canvas></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
var D="""

    html_part2 = """;
var sk='__total__',cm='leads',ch=null;
function sel(row,key){
  if(sk===key){sk='__total__';document.querySelectorAll('tr').forEach(function(r){r.classList.remove('sel');});}
  else{document.querySelectorAll('tr').forEach(function(r){r.classList.remove('sel');});row.classList.add('sel');sk=key;}
  document.getElementById('ctitle').textContent=(sk==='__total__'?'📊 Total':sk)+' — Trend';
  draw();
}
function sm(m,btn){cm=m;document.querySelectorAll('.mb').forEach(function(b){b.classList.remove('on');});btn.classList.add('on');draw();}
function draw(){
  var t=D.trends[sk]||D.trends['__total__'];
  var isR=cm==='roi';
  if(ch){ch.destroy();ch=null;}
  ch=new Chart(document.getElementById('cc'),{type:'line',data:{labels:D.labels,datasets:[
    {data:t[cm]||[],borderColor:'#1877F2',backgroundColor:'rgba(24,119,242,0.08)',fill:true,tension:0.3,pointRadius:3}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},
    tooltip:{callbacks:{label:function(c){return isR?' '+c.parsed.y.toFixed(1)+'%':' '+c.parsed.y.toLocaleString(undefined,{maximumFractionDigits:0});}}}},
    scales:{x:{ticks:{font:{size:10},maxRotation:45,autoSkip:true},grid:{display:false}},
            y:{min:0,ticks:{font:{size:10},callback:function(v){return isR?v.toFixed(0)+'%':v.toLocaleString();}},grid:{color:'#f3f4f6'}}}}});
}
draw();
</script>"""

    n_rows = len(camp_agg)
    import streamlit.components.v1 as components
    components.html(html_part1 + chart_data_json + html_part2, height=n_rows*34+520, scrolling=False)

