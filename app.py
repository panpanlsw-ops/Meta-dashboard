import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Meta Ads Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
#MainMenu, footer { display:none!important }
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

LS_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCABPAIYDASIAAhEBAxEB/8QAHAABAAEFAQEAAAAAAAAAAAAAAAcBAgQFBgMI/8QANRAAAQMDAgQEBAUDBQAAAAAAAQIDBAAFEQYhBxIxQRMUUWEIFTJxIkKBgpEjobEWM1KSwf/EABsBAQADAQEBAQAAAAAAAAAAAAABAgQDBQYH/8QAMBEAAgIBAwICBgsAAAAAAAAAAAECEQMEBSESMRNBIjJRYcHRBhQzYoGRkqHh8PH/2gAMAwEAAhEDEQA/APsulKUApSlAKUpQClKUApSmR6igFKZHqKUApSlAKUpQClKUApSlAUV1ptQ4NWLISklasAb5zihBcetUWQncnAqMeIHGjS+mFuQoqzd7ik8oYjKBSlXopfQH23PtUduSONHE1eI7SrBaXDtkllJT7q+tX6AD7VnnqIxdR5fuPb0uxZ8sPFzNY4e2XH5LuyatU8QdI6ZCvnF7isuAZ8FCudw/tTk1FuofiPtyFKZ09YJMxfRC5Cw2D+0ZP+KytMfDvY46hI1HdZVzfO622z4SCfc/Uf5qT7BorSthSlNpsMGOU/nDQK/+x3qlZ5/dRt6tj0flLNL9MfmQKriVxp1GT8ksLsdpX0mPAUQP3ryP8V5u2n4h54LjjtzQCM4Etlv+wNfT6UpHRI29Krio+qt+tNkr6SY8X2Glxpe9X+58gagmca9JIEy6zL5GZSRl4updbHsSOYD9a6jhNxyvruoIVl1R4c2PLeSwiSlAQ4hSjhOQNlDOOwqYuNt9ttj4d3R24hpzzDKo7LK9/FWoEAf+/pXz78OfD6XqLU0fUExlbdotzocStYP9Z1O6Uj1AO5PsKyyhkxZoxxyu+59Fp9Votx2vLqNZgjDp4TSq3XFf2j63b6e1XVY31Ixjar69Y/NRSlKAUpSgKK+2ax57BkxHY6XnWC4gp8Ro4WjI6g+te7nbriuW1Jf5qZZs2moSJ91OyluEiPFB/O6of2QNz7daiTSXJeGKWV1Eh/hzxEftl21NM1lq2fIYtMoxIEM8pXIPMsfSACtWw32G9Y+vdQ611NCanX0ztHaQkuhpAZZLsh7P0hQSQQVds4H37+/w12K3zNa6xmXdiNcLnAn8qJC2xsorXzqSk9MkbemP56n4hLvbZ+i1xoklC3IF9iMyMbBC8hXLnoTgiszhKcfSdI47fuePb9D4mKN5efSlylTfZfFnlpuzcOtA32BZ2bBc519lxw+045ELrikgZVj8qcY3Axviute4lWFh62MKh3cP3NbjcVnyKgta21FLicdiCN89q5XiG1Olce9JMWu5ot0tVrk8j6mUu467cpIzkA/xWBxIj3OPrHhjb5F4ZauyXX0uzC2FpK+VIKuUkdTtv3Iq6qCqKMms3TV6icp5ZOTtK3+HHf3m/wCKXEl23cM7hfdPNSGJjMwQFeajlKo7m2VFB67EYzseYVkaQt92clWDUFh1jcL7aZKFJuTcuQlxJBRkLQAPwqCsApHr7V7pesL1kZ0TrCexdpk55USS4E8qFvEKcQFEfSopSOXfIIHtUZWSwXLhbxytFhsdyflWO+5Ko7hyUpGclQ6ZTjPN1IzVm6kmY8uXIskZvlOlw+z/AJ7MmW564tMO7TLbFjXC6SYKQqaIEcuiODuAo7DmxvyjfHatbqLivo+0adg3zzjsyNcUr8p5dpSi4tPVGOqTnbfFcTwan3aLH1bZo6Y7V3bvb8ibNmuYbbbXjDmM5X9KsdB0JI7xm9YWo/DeXrBxjxufVKVMT/D5eaMFnLiU9EpUr07iqPJJ+qapaiWLGsk65vj2V7fidddrXdNXastV44ntXG32+Y74VqtEVhThOTnlWpP0Ejck4UQD0AxUns8QNIafTNtDMKfCjWVSGJRbgL8GLzfSVEdEnrn3zV+s5sK6ap0TFgympDnzFUvDawohlDDmV4HbKkjPuKinXjl0bu/FXyRYcgmRCTcWkpKn/LlsBZbOcAgZzkEdemKiMVjtrlmndd81OeKSaUI8JLsuL/1k637WFis0SDJkSnH1XEjyLMZsuuysgEciE7kYI36DvWAeIFrai3R+Zb7vCVa2EyZLL8MhYaJP404yFJHKckE4wajyO7a7fxn0bcUSEHTb9g8naJK1/wBMLA2GT0UU4G+++K7fixdLWvRmqrWh5k3FFikOrSnHMhsoUBk9snOB33xXZStMyrUzlGUrSr5Gw0/rm0XqXb2I8W5si5NKehuSIim23kpHMcKPsQcHtXXVEXBwzYNh03Lumo40qDOtzUeBEDQQpt7c4GCebCAQScY5T61LtWTs0aXJLJDqkhSlKk0ljoCk4JIyCMg4IrCXa4fy16A22ppl5KgstKKFHPU8w3yfWs9X2pRpMeVHAwOEmiILy5EKBMjPOf7jjNwfQpff8RC9+vetrbtAaQhWkWtNkjSYoeU/ySh4xLiscysrzucDf2rqaVHSjhHTYo9oo0zmmbA5PZnuWWCuWwEhp8spK0BIwAFdRgVS7aY0/dpSZdzssCW+lPKHHmErUB7Eit1TY0pF3ig1VI5e7aE0nc7N8oes0duL44kpEceEpLw6OApwQr3qun9EWGy3VV3ZZkSrkW/CEuZJW+6lH/BKlk8qfYYrp6UpFfAx9Sl0q0aS9aV07eZKJV0ssKY+hPKFutAnl9D6j2NZ7lvguQDb1wo6oZRyeAUAo5fTl6YrLFVx7VNIv0Ru6RprDpfT1hWtdms8KApwcq1MMpQSOuMjtntVYumrDFmSJcWzwWX5KVJfcQwkKdCjkhR7/rW4FV79aikR4UKqjSf6W06LR8o+SwDbyvxPLFhJbCvUJ6A/avGNo7S0eE9CasFvEd8hTyCykhzGcc2euMnr0ya6GqUpB4oPyRpLdpTTVumNS7fYrfFkM58NxlhKSjIwcYG2RtW8qlVqS0YqPYUpShYUpSgFKUoBSlKAUpSgFKUoBSlKAUpSgFKUoBSlKA//2Q=="

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

@st.cache_data(ttl=3600)
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
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="background:#111111;margin:-1rem -1rem 1rem -1rem;padding:20px 16px 16px;">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="background:#1877F2;border-radius:8px;width:36px;height:36px;
                    display:flex;align-items:center;justify-content:center;flex-shrink:0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 24" height="16">
            <path d="M2 12C2 7.2 5.2 3 9.2 3c2.2 0 4.2 1.2 5.8 3.3C16.6 4.2 18.6 3 20.6 3
            c4 0 7.2 4.2 7.2 9 0 2.5-.8 4.8-2.1 6.4-1.2 1.4-2.7 2.2-4.3 2.2
            -2 0-3.6-1-5.6-3.9-2 2.9-3.6 3.9-5.6 3.9-1.6 0-3.1-.8-4.3-2.2
            C2.8 16.8 2 14.5 2 12zm7.2-5.5C6 6.5 4 9 4 12s2 5.5 5.2 5.5
            c1.4 0 2.6-.8 4.2-3.4-1.6-2.8-2.8-4.6-4.2-4.6zm11.4 0c-1.4 0-2.6 1.8-4.2 4.6
            1.6 2.6 2.8 3.4 4.2 3.4 3.2 0 5.2-2.5 5.2-5.5s-2-5.5-5.2-5.5z" fill="white"/>
          </svg>
        </div>
        <div>
          <div style="color:white;font-size:1rem;font-weight:700">Meta Ads</div>
          <div style="color:#888;font-size:0.72rem">Dashboard</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    sel_camp = "All"
    sel_off  = "All"
    date_range = None

    # Campaign selector — only show in Trends tab
    if st.session_state.get("page","overview") == "trends" and "Campaign Performance" in data:
        st.markdown("<p style='color:#888888;font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin:8px 0 4px'>Campaign</p>", unsafe_allow_html=True)
        camp_names_sb = ["All Campaigns"] + sorted(
            data["Campaign Performance"]["Campaign Objective"].dropna().unique().tolist()
        )
        if "trend_selected_camp" not in st.session_state:
            st.session_state["trend_selected_camp"] = "All Campaigns"
        sel_trend_sb = st.selectbox(
            "Camp", camp_names_sb,
            index=camp_names_sb.index(st.session_state["trend_selected_camp"])
                  if st.session_state["trend_selected_camp"] in camp_names_sb else 0,
            label_visibility="collapsed",
            key="trend_camp_sidebar"
        )
        st.session_state["trend_selected_camp"] = sel_trend_sb
    MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    all_years = []
    if "Campaign Performance" in data:
        cp = data["Campaign Performance"]
        if "Year" in cp.columns:
            all_years = sorted(cp["Year"].unique().tolist())
    if not all_years:
        all_years = [2024, 2025, 2026]

    st.markdown("<p style='color:#888888;font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin:6px 0 4px'>From</p>", unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    from_month = fc1.selectbox("FM", MONTHS, index=0, label_visibility="collapsed", key="from_month")
    from_year  = fc2.selectbox("FY", all_years, index=0, label_visibility="collapsed", key="from_year")
    st.markdown("<p style='color:#888888;font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin:6px 0 4px'>To</p>", unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    to_month = tc1.selectbox("TM", MONTHS, index=len(MONTHS)-1, label_visibility="collapsed", key="to_month")
    to_year  = tc2.selectbox("TY", all_years, index=len(all_years)-1, label_visibility="collapsed", key="to_year")
    from_m    = MONTHS.index(from_month) + 1
    to_m      = MONTHS.index(to_month) + 1
    from_year = int(from_year)
    to_year   = int(to_year)

    st.markdown("---")
    st.markdown("**VIEWS**")

    for key,icon,label in [("overview","📊","MTD Overview"),
                            ("territory","🗺️","By Territory"),
                            ("trends","📈","Trends")]:
        active = st.session_state.page == key
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

# ════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════
titles = {"overview":"MTD Overview","territory":"By Territory","trends":"Trends"}

# Top bar — Meta Ads brand + LifeSource logo side by side
st.markdown(
    f'<div style="background:#1877F2;padding:10px 20px;border-radius:8px;' +
    f'display:flex;align-items:center;gap:10px;margin-bottom:18px">' +
    f'<div style="background:white;border-radius:6px;padding:3px 10px;display:flex;align-items:center">' +
    f'<img src="data:image/png;base64,{LS_B64}" height="24" style="display:block;object-fit:contain">' +
    f'</div>' +
    f'<span style="width:1px;height:22px;background:rgba(255,255,255,0.35);display:inline-block"></span>' +
    f'<span style="color:white;font-weight:700;font-size:1rem">Meta Ads</span>' +
    f'<span style="width:1px;height:22px;background:rgba(255,255,255,0.35);display:inline-block"></span>' +
    f'<span style="color:white;font-size:0.9rem;font-weight:600">{titles[st.session_state.page]}</span>' +
    f'<span style="margin-left:auto;color:rgba(255,255,255,0.85);font-size:0.8rem">{from_month} {from_year} – {to_month} {to_year}</span>' +
    f'</div>', unsafe_allow_html=True)

# ── PAGE 1 ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "overview":

    if "Overview" in data:
        ov_all = data["Overview"].copy()
        # Filter by selected date range
        ov = ov_all[
            ((ov_all["Year"] > from_year) |
             ((ov_all["Year"] == from_year) & (ov_all["Month"] >= from_m))) &
            ((ov_all["Year"] < to_year) |
             ((ov_all["Year"] == to_year) & (ov_all["Month"] <= to_m)))
        ]
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
            if m not in ov_sum.index or ov_sum[m] == 0:
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
        # Filter by date range
        if "Year" in camp_df.columns and "Month" in camp_df.columns:
            camp_df["Year"] = pd.to_numeric(camp_df["Year"], errors="coerce").fillna(0).astype(int)
        camp_df["Month"] = pd.to_numeric(camp_df["Month"], errors="coerce").fillna(0).astype(int)
        camp_df = camp_df[
                ((camp_df["Year"] > from_year) |
                 ((camp_df["Year"] == from_year) & (camp_df["Month"] >= from_m))) &
                ((camp_df["Year"] < to_year) |
                 ((camp_df["Year"] == to_year) & (camp_df["Month"] <= to_m)))
            ]
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

# ── PAGE 2 ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "territory":

    if "Territory Summary" not in data:
        st.warning("No Territory Performance sheet found."); st.stop()

    raw = data["Territory Summary"].copy()

    # Apply filters from sidebar
    tdf = raw.copy()
    # Filter by date range
    if "Year" in tdf.columns and "Month" in tdf.columns:
        tdf["Year"] = pd.to_numeric(tdf["Year"], errors="coerce").fillna(0).astype(int)
        tdf["Month"] = pd.to_numeric(tdf["Month"], errors="coerce").fillna(0).astype(int)
        tdf = tdf[
            ((tdf["Year"] > from_year) |
             ((tdf["Year"] == from_year) & (tdf["Month"] >= from_m))) &
            ((tdf["Year"] < to_year) |
             ((tdf["Year"] == to_year) & (tdf["Month"] <= to_m)))
        ]
    if sel_off != "All":
        tdf = tdf[tdf["Territory"] == sel_off]

    # Show date range label
    dr_label = f"{from_month} {from_year} – {to_month} {to_year}"
    st.markdown(
        f"<p style='font-size:0.78rem;color:#6b7280;margin-bottom:12px'>Showing: {dr_label}</p>",
        unsafe_allow_html=True)

    # Aggregate by territory
    terr = tdf.groupby("Territory").agg({
        "Unique Leads":"sum","New Leads":"sum","Appointments":"sum","Quote":"sum",
        "Customers":"sum","Sales Amount ($)":"sum",
    }).reset_index()
    tot = terr.sum(numeric_only=True)

    terr["Leads %"]     = (terr["Unique Leads"]    /tot["Unique Leads"]     *100).round(2) if tot["Unique Leads"] else 0
    terr["Sales %"]     = (terr["Sales Amount ($)"]/tot["Sales Amount ($)"] *100).round(2) if tot["Sales Amount ($)"] else 0
    terr["APT/Leads"]   = (terr["Appointments"]    /terr["Unique Leads"].replace(0,1)*100).round(2)
    terr["Order/APT"]   = (terr["Customers"]       /terr["Appointments"].replace(0,1)*100).round(2)
    terr["Order/Leads"] = (terr["Customers"]       /terr["Unique Leads"].replace(0,1)*100).round(2)
    terr = terr.sort_values("Sales Amount ($)", ascending=False)

    ul  = int(tot["Unique Leads"])
    apt = int(tot["Appointments"])
    cu  = int(tot["Customers"])
    sal = tot["Sales Amount ($)"]
    ap  = round(apt/ul*100) if ul else 0

    # ── KPI strip ──────────────────────────────────────────────────
    def tcell(color, label, value):
        return (
            f'<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;' +
            f'padding:16px 14px 14px;position:relative;box-shadow:0 1px 4px rgba(0,0,0,0.05)">' +
            f'<div style="position:absolute;top:0;left:0;right:0;height:4px;border-radius:10px 10px 0 0;background:{color}"></div>' +
            f'<div style="font-size:0.62rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px">{label}</div>' +
            f'<div style="font-size:1.3rem;font-weight:700;color:#111827">{value}</div></div>'
        )

    st.markdown(
        '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:20px">' +
        tcell("#1877F2","Total Leads",     fn(ul))  +
        tcell("#06b6d4","Appointments",    fn(apt)) +
        tcell("#ec4899","Customers",       fn(cu))  +
        tcell("#22c55e","Total Sales",     fc(sal)) +
        tcell("#f59e0b","APT / Leads",     f"{ap}%") +
        '</div>', unsafe_allow_html=True)

    # ── Regional Office Performance table ──────────────────────────
    # Sort by Unique Leads desc, then Sales Amount desc
    terr = terr.sort_values(["Unique Leads","Sales Amount ($)"], ascending=[False,False])

    def bar(pct, color):
        w = min(float(pct), 100)
        return (f'<div style="display:flex;align-items:center;gap:6px">' +
                f'<div style="flex:1;height:4px;background:#e5e7eb;border-radius:3px;min-width:50px">' +
                f'<div style="width:{w}%;height:100%;background:{color};border-radius:3px"></div></div>' +
                f'<span style="font-size:11px;color:#374151;white-space:nowrap">{pct:.2f}</span></div>')

    html = """
    <style>
    .terr-tbl{width:100%;border-collapse:collapse;font-size:12px}
    .terr-tbl thead tr{background:#111827}
    .terr-tbl thead th{color:white;padding:9px 10px;text-align:left;font-weight:500;
        font-size:11px;letter-spacing:0.05em;white-space:nowrap}
    .terr-tbl tbody tr{border-bottom:1px solid #e5e7eb}
    .terr-tbl tbody tr:hover{background:#f0f7ff}
    .terr-tbl td{padding:8px 10px;white-space:nowrap;color:#111827;font-size:12px}
    .terr-tbl tr.tot td{background:#dbeafe;color:#1e3a5f;font-weight:600;border-bottom:2px solid #93c5fd}
    </style>
    <div style="overflow-x:auto">
    <table class="terr-tbl">
    <thead><tr>
      <th>Regional Office</th>
      <th>Unique Leads</th><th>New Leads</th><th>APT</th><th>Quote</th>
      <th>Customers</th><th>Sales Amount</th>
      <th>Leads %</th><th>Sales %</th>
      <th>APT/Leads</th><th>Order/Leads</th>
    </tr></thead>
    <tbody>"""

    al_tot = round(tot["Appointments"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0
    ol_tot = round(tot["Customers"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0
    html += (f'<tr class="tot"><td><b>Total</b></td>' +
             f'<td>{fn(tot["Unique Leads"])}</td><td>{fn(tot["New Leads"])}</td>' +
             f'<td>{fn(tot["Appointments"])}</td><td>{fn(tot.get("Quote",0))}</td>' +
             f'<td>{fn(tot["Customers"])}</td><td>{fc(tot["Sales Amount ($)"])}</td>' +
             f'<td>100%</td><td>100%</td>' +
             f'<td>{al_tot:.1f}%</td><td>{ol_tot:.2f}%</td></tr>')

    for idx, r in terr.iterrows():
        tid = f"t{idx}"
        # Territory row — clickable
        html += (f'<tr onclick="tog(\'{tid}\')" style="cursor:pointer;background:white;border-bottom:1px solid #e5e7eb">' +
                 f'<td><span id="{tid}-a" style="display:inline-block;font-size:10px;color:#9ca3af;margin-right:6px;transition:transform 0.15s">▶</span>' +
                 f'<b>{r["Territory"]}</b></td>' +
                 f'<td>{int(r["Unique Leads"])}</td><td>{int(r["New Leads"])}</td>' +
                 f'<td>{int(r["Appointments"])}</td><td>{int(r["Quote"])}</td>' +
                 f'<td>{int(r["Customers"])}</td><td>{fc(r["Sales Amount ($)"])}</td>' +
                 f'<td>{bar(min(100,float(str(r.get("Leads %",0)).replace("%","").replace(",","").strip() or 0)), "#1877F2")}</td>' +
                 f'<td>{bar(min(100,float(str(r.get("Sales %",0)).replace("%","").replace(",","").strip() or 0)), "#22c55e")}</td>' +
                 f'<td>{str(r.get("APT/Leads","0%"))}</td>' +
                 f'<td>{str(r.get("Order/Leads","0%"))}</td></tr>')

        # Campaign breakdown
        # Use Territory Detail filtered by date range
        t_detail = data.get("Territory Detail", pd.DataFrame())
        if not t_detail.empty and "Territory" in t_detail.columns:
            t_det = t_detail.copy()
            if "Year" in t_det.columns and "Month" in t_det.columns:
                t_det["Year"]  = pd.to_numeric(t_det["Year"],  errors="coerce").fillna(0).astype(int)
                t_det["Month"] = pd.to_numeric(t_det["Month"], errors="coerce").fillna(0).astype(int)
                t_det = t_det[
                    ((t_det["Year"] > from_year) |
                     ((t_det["Year"] == from_year) & (t_det["Month"] >= from_m))) &
                    ((t_det["Year"] < to_year) |
                     ((t_det["Year"] == to_year) & (t_det["Month"] <= to_m)))
                ]
            camp_data = t_det[t_det["Territory"] == r["Territory"]].groupby("Campaign").agg({
                "Unique Leads":"sum","New Leads":"sum","Appointments":"sum",
                "Quote":"sum","Customers":"sum","Sales Amount ($)":"sum"
            }).reset_index().sort_values("Unique Leads", ascending=False)
        else:
            camp_data = pd.DataFrame()

        t_ul = r["Unique Leads"] if r["Unique Leads"] else 1
        t_sa = r["Sales Amount ($)"] if r["Sales Amount ($)"] else 1

        for _, cr in camp_data.iterrows():
            c_leads_pct = cr["Unique Leads"] / t_ul * 100 if t_ul else 0
            c_sales_pct = cr["Sales Amount ($)"] / t_sa * 100 if t_sa else 0
            c_apt_leads = cr["Appointments"] / cr["Unique Leads"] * 100 if cr["Unique Leads"] else 0
            c_ord_leads = cr["Customers"] / cr["Unique Leads"] * 100 if cr["Unique Leads"] else 0
            html += (f'<tr class="{tid}-camp" style="display:none;background:#f5f8ff;border-bottom:1px solid #eff0f6">' +
                     f'<td style="padding-left:28px;color:#111827;font-weight:400;font-size:11.5px">{cr["Campaign"]}</td>' +
                     f'<td style="font-size:11.5px">{int(cr["Unique Leads"])}</td>' +
                     f'<td style="font-size:11.5px">{int(cr["New Leads"])}</td>' +
                     f'<td style="font-size:11.5px">{int(cr["Appointments"])}</td>' +
                     f'<td style="font-size:11.5px">{int(cr.get("Quote",0))}</td>' +
                     f'<td style="font-size:11.5px">{int(cr["Customers"])}</td>' +
                     f'<td style="font-size:11.5px">{fc(cr["Sales Amount ($)"])}</td>' +
                     f'<td>{bar(c_leads_pct, "#1877F2")}</td>' +
                     f'<td>{bar(c_sales_pct, "#22c55e")}</td>' +
                     f'<td style="font-size:11.5px">{c_apt_leads:.1f}%</td>' +
                     f'<td style="font-size:11.5px">{c_ord_leads:.2f}%</td></tr>')

    html += """</tbody></table></div>
    <script>
    function tog(id){
      var rows=document.querySelectorAll('.'+id+'-camp');
      var arrow=document.getElementById(id+'-a');
      var open=rows[0]&&rows[0].style.display!=='none'&&rows[0].style.display!=='';
      rows.forEach(function(r){r.style.display=open?'none':'table-row';});
      if(arrow){arrow.style.transform=open?'rotate(0deg)':'rotate(90deg)';}
    }
    </script>"""
    import streamlit.components.v1 as components
    n_terr = len(terr)
    t_det = data.get("Territory Detail", pd.DataFrame())
    if not t_det.empty and "Campaign" in t_det.columns:
        n_camp = sum(len(t_det[t_det["Territory"]==r["Territory"]]["Campaign"].unique()) for _,r in terr.iterrows())
    else:
        n_camp = 0
    tbl_height = max(500, (n_terr + 2) * 38 + n_camp * 34)
    components.html(html, height=tbl_height, scrolling=True)

# ── PAGE 3 ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "trends":

    if "Campaign Performance" not in data:
        st.warning("No Campaign Performance sheet found."); st.stop()

    # Full dataset for chart (all months)
    full_df = data["Campaign Performance"].copy()
    full_df["Year"]  = pd.to_numeric(full_df["Year"],  errors="coerce").fillna(0).astype(int)
    full_df["Month"] = pd.to_numeric(full_df["Month"], errors="coerce").fillna(0).astype(int)

    # Date-filtered dataset for summary table
    camp_df = full_df[
        ((full_df["Year"] > from_year) |
         ((full_df["Year"] == from_year) & (full_df["Month"] >= from_m))) &
        ((full_df["Year"] < to_year) |
         ((full_df["Year"] == to_year) & (full_df["Month"] <= to_m)))
    ].copy()

    # Aggregate by campaign for table (one row per campaign)
    agg_cols = {c:"sum" for c in ["Spend ($)","CRM Leads","Appointments","Customers","Sales Amount ($)"] if c in camp_df.columns}
    camp_agg = camp_df.groupby("Campaign Objective").agg(agg_cols).reset_index()
    camp_agg["Cost/Lead"]  = camp_agg.apply(lambda r: fc(r["Spend ($)"]/r["CRM Leads"]) if r["CRM Leads"]>0 else "—", axis=1)
    camp_agg["APT/Lead"]   = camp_agg.apply(lambda r: f'{r["Appointments"]/r["CRM Leads"]*100:.1f}%' if r["CRM Leads"]>0 and r["Appointments"]>0 else "—", axis=1)
    camp_agg["Order/APT"]  = camp_agg.apply(lambda r: f'{r["Customers"]/r["Appointments"]*100:.1f}%' if r["Appointments"]>0 else "—", axis=1)

    # Total row
    tot = camp_df.sum(numeric_only=True)
    total_row = {
        "Campaign Objective":"Total",
        "Spend ($)": fc(tot["Spend ($)"]),
        "CRM Leads": fn(tot["CRM Leads"]),
        "Cost/Lead": fc(tot["Spend ($)"]/tot["CRM Leads"]) if tot["CRM Leads"]>0 else "—",
        "Appointments": fn(tot["Appointments"]),
        "APT/Lead": f'{tot["Appointments"]/tot["CRM Leads"]*100:.1f}%' if tot["CRM Leads"]>0 else "—",
        "Customers": fn(tot["Customers"]),
        "Order/APT": f'{tot["Customers"]/tot["Appointments"]*100:.1f}%' if tot["Appointments"]>0 else "—",
        "Sales Amount ($)": fc(tot["Sales Amount ($)"]),
    }

    # Format display table
    disp = camp_agg.copy()
    disp["Spend ($)"]        = disp["Spend ($)"].apply(fc)
    disp["CRM Leads"]        = disp["CRM Leads"].apply(fn)
    disp["Appointments"]     = disp["Appointments"].apply(fn)
    disp["Customers"]        = disp["Customers"].apply(fn)
    disp["Sales Amount ($)"] = disp["Sales Amount ($)"].apply(fc)
    col_rename = {"Campaign Objective":"Campaign","Spend ($)":"Cost","CRM Leads":"Leads","Appointments":"APT","Sales Amount ($)":"Sales"}
    disp = disp.rename(columns=col_rename)
    disp = disp[["Campaign","Cost","Leads","Cost/Lead","APT","APT/Lead","Customers","Order/APT","Sales"]]

    total_disp = pd.DataFrame([{
        "Campaign":"Total","Cost":total_row["Spend ($)"],"Leads":total_row["CRM Leads"],
        "Cost/Lead":total_row["Cost/Lead"],"APT":total_row["Appointments"],
        "APT/Lead":total_row["APT/Lead"],"Customers":total_row["Customers"],
        "Order/APT":total_row["Order/APT"],"Sales":total_row["Sales Amount ($)"]}])
    disp = pd.concat([total_disp, disp], ignore_index=True)

    # ── Clickable HTML table ─────────────────────────────────────
    import streamlit.components.v1 as components

    tbl_html = """
    <style>
    body{margin:0;font-family:-apple-system,sans-serif}
    table{width:100%;border-collapse:collapse;font-size:12px}
    thead tr{background:#111827}
    thead th{color:white;padding:9px 10px;text-align:left;font-weight:500;font-size:11px;letter-spacing:.04em;white-space:nowrap}
    tbody tr{border-bottom:1px solid #e5e7eb;cursor:pointer}
    tbody tr:hover td{background:#f0f7ff}
    tbody tr.selected td{background:#dbeafe!important;font-weight:500}
    tbody tr.total-row td{background:#f8fafc;font-weight:500}
    tbody td{padding:8px 10px;color:#111827;white-space:nowrap}
    </style>
    <table id="ctable">
    <thead><tr>
      <th>Campaign</th><th>Cost</th><th>Leads</th><th>Cost/Lead</th>
      <th>APT</th><th>APT/Lead</th><th>Customers</th><th>Order/APT</th><th>Sales</th>
    </tr></thead>
    <tbody>
    """

    rows_data = []
    for _, row in disp.iterrows():
        is_total = row["Campaign"] == "Total"
        row_class = "total-row" if is_total else "camp-row"
        camp_val = "" if is_total else row["Campaign"]
        tbl_html += f'<tr class="{row_class}" onclick="selectCamp(this, \'{camp_val.replace("'","\'")}\')">'
        for col in ["Campaign","Cost","Leads","Cost/Lead","APT","APT/Lead","Customers","Order/APT","Sales"]:
            tbl_html += f'<td>{row[col]}</td>'
        tbl_html += "</tr>"

    tbl_html += """
    </tbody></table>
    <script>
    var selected = null;
    function selectCamp(tr, name) {
        if (tr.classList.contains("total-row")) return;
        if (selected === tr) {
            tr.classList.remove("selected");
            selected = null;
            window.parent.postMessage({type:"streamlit:setComponentValue", value:""}, "*");
        } else {
            if (selected) selected.classList.remove("selected");
            tr.classList.add("selected");
            selected = tr;
            window.parent.postMessage({type:"streamlit:setComponentValue", value:name}, "*");
        }
    }
    </script>
    """

    components.html(
        tbl_html,
        height=min(600, (len(disp)+1)*35+60),
        scrolling=True
    )

    # Get selected campaign from sidebar
    sel_camp_name = st.session_state.get("trend_selected_camp", "All Campaigns")

    # Determine which campaign to chart
    if sel_camp_name and sel_camp_name != "All Campaigns":
        chart_df = full_df[full_df["Campaign Objective"].astype(str) == str(sel_camp_name)].copy()
        chart_title = sel_camp_name
    else:
        chart_df = full_df.copy()
        chart_title = "All Campaigns"

    # Metric toggle buttons
    metric_opts   = ["Spend ($)","CRM Leads","Appointments","Customers","Sales Amount ($)"]
    metric_labels = ["Spend","Leads","APT","Customers","Sales"]
    if "trend_metric" not in st.session_state:
        st.session_state.trend_metric = "CRM Leads"

    # Render pill buttons
    btn_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 14px">'
    for m, lbl in zip(metric_opts, metric_labels):
        active = st.session_state.trend_metric == m
        if active:
            btn_html += f'<span style="background:#111827;color:white;border:1px solid #111827;font-size:0.82rem;padding:5px 16px;border-radius:6px;font-weight:500">{lbl}</span>'
        else:
            btn_html += f'<span style="background:white;color:#374151;border:1px solid #d1d5db;font-size:0.82rem;padding:5px 16px;border-radius:6px">{lbl}</span>'
    btn_html += '</div>'
    st.markdown(btn_html, unsafe_allow_html=True)

    # Hidden buttons to capture clicks
    cols = st.columns(len(metric_opts))
    for i, (m, lbl) in enumerate(zip(metric_opts, metric_labels)):
        if cols[i].button(lbl, key=f"tmbtn_{i}", use_container_width=True):
            st.session_state.trend_metric = m
            st.rerun()
    metric = st.session_state.trend_metric

    # Hide native buttons with CSS
    st.markdown("""<style>
    div[data-testid="stHorizontalBlock"] button {
        opacity: 0 !important;
        height: 10px !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
    }
    </style>""", unsafe_allow_html=True)

    # Aggregate monthly
    if "Year" in chart_df.columns and "Month" in chart_df.columns and len(chart_df) > 0:
        agg_c = {c:"sum" for c in metric_opts if c in chart_df.columns}
        agg = chart_df.groupby(["Year","Month"]).agg(agg_c).reset_index()
        agg["Period"] = pd.to_datetime(
            agg.apply(lambda r: f"{int(r['Year'])}-{int(r['Month']):02d}-01", axis=1))
        agg = agg.sort_values("Period")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=agg["Period"], y=agg[metric],
            mode="lines+markers",
            line=dict(color="#1877F2", width=2),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(24,119,242,0.08)",
            hovertemplate=f"<b>%{{x|%b %Y}}</b><br>{sel_metric_lbl}: %{{y:,.0f}}<extra></extra>"
        ))
        fig.update_layout(
            height=300,
            title=dict(text=f"{chart_title} — {sel_metric_lbl}", font=dict(size=13,color="#111827"), x=0),
            margin=dict(t=40,b=40,l=55,r=20),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickformat="%b %Y"),
            yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
            hovermode="x unified", showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

