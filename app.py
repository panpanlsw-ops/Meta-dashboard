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

@st.cache_data
def load_data(f):
    xls=pd.ExcelFile(f)
    return {n:pd.read_excel(xls,sheet_name=n) for n in xls.sheet_names}

def ch(h=210):
    return dict(height=h, margin=dict(t=8,b=32,l=50,r=12),
                paper_bgcolor="white", plot_bgcolor="white",
                xaxis=dict(showgrid=False, tickformat="%b %d"),
                yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode="x unified")

for k,v in [("page","overview"),("t1c","All Campaigns"),("gran","Daily")]:
    if k not in st.session_state: st.session_state[k]=v

try:    data=load_data("meta_ads_data.xlsx")
except: data={}

camp_list = ["All"]
if "Campaign Performance" in data:
    camp_list += list(data["Campaign Performance"]["Campaign Objective"].unique())
off_list = ["All"]
if "Territory Performance" in data:
    off_list += sorted(data["Territory Performance"]["Territory"].unique().tolist())

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

    st.markdown("**FILTERS**")
    sel_camp = st.selectbox("Campaign", camp_list)
    sel_off  = st.selectbox("Office / Territory", off_list)
    date_range = None
    if "Daily Performance" in data:
        dr=data["Daily Performance"].copy()
        dr["Date"]=pd.to_datetime(dr["Date"])
        mn,mx=dr["Date"].min().date(),dr["Date"].max().date()
        date_range=st.date_input("Date range",value=(mn,mx),min_value=mn,max_value=mx)

    st.markdown("---")
    st.markdown("**VIEWS**")

    for key,icon,label in [("overview","📊","MTD Overview"),
                            ("trends","📈","Trends"),
                            ("territory","🗺️","By Territory")]:
        active = st.session_state.page == key
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

# ════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════
titles = {"overview":"MTD Overview","trends":"Trends","territory":"By Territory"}

# Top bar
col_bar, col_ls = st.columns([8,1])
with col_bar:
    st.markdown(
        f'<div style="background:#1877F2;padding:11px 20px;border-radius:8px;' +
        f'display:flex;align-items:center;gap:12px;margin-bottom:18px">' +
        f'<span style="color:white;font-weight:700;font-size:1rem">Meta Ads</span>' +
        f'<span style="width:1px;height:20px;background:rgba(255,255,255,0.35);display:inline-block"></span>' +
        f'<span style="color:white;font-size:0.9rem;font-weight:600">{titles[st.session_state.page]}</span>' +
        f'<span style="margin-left:auto;color:rgba(255,255,255,0.85);font-size:0.8rem">Dec 2024</span>' +
        f'</div>', unsafe_allow_html=True)
with col_ls:
    st.markdown(
        f'<div style="background:#1877F2;padding:6px 12px;border-radius:8px;' +
        f'display:flex;align-items:center;justify-content:center;margin-bottom:18px">' +
        f'<div style="background:white;border-radius:5px;padding:2px 8px">' +
        f'<img src="data:image/png;base64,{LS_B64}" height="22" style="display:block;object-fit:contain">' +
        f'</div></div>', unsafe_allow_html=True)

# ── PAGE 1 ─────────────────────────────────────────────────────────────────────
if st.session_state.page == "overview":

    if "Overview" in data:
        ov=data["Overview"].set_index("Metric")
        def kc(m,color,cur=False,pg=True):
            if m not in ov.index:
                return ('<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;' +
                        'padding:16px 14px 13px;position:relative;box-shadow:0 1px 4px rgba(0,0,0,0.06)">' +
                        f'<div style="position:absolute;top:0;left:0;right:0;height:4px;border-radius:10px 10px 0 0;background:{color}"></div>' +
                        f'<div style="font-size:0.65rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px">{m}</div>' +
                        '<div style="font-size:1.35rem;font-weight:700;color:#111827">—</div></div>')
            r=ov.loc[m]; v=fc(r["Current Period"]) if cur else fn(r["Current Period"])
            d=dlt(r["Change %"],pg)
            return ('<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;' +
                    'padding:16px 14px 13px;position:relative;box-shadow:0 1px 4px rgba(0,0,0,0.06)">' +
                    f'<div style="position:absolute;top:0;left:0;right:0;height:4px;border-radius:10px 10px 0 0;background:{color}"></div>' +
                    f'<div style="font-size:0.65rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px">{m}</div>' +
                    f'<div style="font-size:1.35rem;font-weight:700;color:#111827;margin-bottom:5px">{v}</div>{d}</div>')
        st.markdown(
            '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:10px;margin-bottom:26px">'+
            kc("Spend ($)","#1877F2",True,False)+kc("Sales Amount ($)","#22c55e",True,True)+
            kc("Clicks","#8b5cf6",False,True)+kc("Conversions","#10b981",False,True)+
            kc("CRM Leads","#f59e0b",False,True)+kc("Appointments","#ec4899",False,True)+
            kc("Customers","#06b6d4",False,True)+'</div>', unsafe_allow_html=True)

    if "Campaign Performance" in data:
        camp_df=data["Campaign Performance"].copy()
        opts=["All Campaigns"]+list(camp_df["Campaign Objective"].unique())
        st.markdown("<p style='font-size:0.85rem;color:#374151;font-weight:500;margin-bottom:10px'>Select campaign to drill down:</p>",unsafe_allow_html=True)
        bc=st.columns(len(opts))
        for i,lb in enumerate(opts):
            with bc[i]:
                if st.button(lb,key=f"cp_{i}",use_container_width=True,
                             type="primary" if st.session_state.t1c==lb else "secondary"):
                    st.session_state.t1c=lb; st.rerun()
        sel=st.session_state.t1c
        fd=camp_df if sel=="All Campaigns" else camp_df[camp_df["Campaign Objective"]==sel]
        st.markdown("<div style='height:18px'></div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3,gap="medium")
        with c1:
            st.markdown(sh("💸 Spend by Campaign")+sb_o(),unsafe_allow_html=True)
            fig=px.pie(camp_df,values="Spend ($)",names="Campaign Objective",hole=0.42,color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside",textinfo="percent",hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
            fig.update_layout(height=220,margin=dict(t=0,b=0,l=0,r=0),paper_bgcolor="white",legend=dict(font=dict(size=9)))
            st.plotly_chart(fig,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        with c2:
            st.markdown(sh("👥 CRM Leads by Campaign")+sb_o(),unsafe_allow_html=True)
            ld=camp_df[camp_df["CRM Leads"]>0].sort_values("CRM Leads")
            f2=px.bar(ld,x="CRM Leads",y="Campaign Objective",orientation="h",color="Campaign Objective",color_discrete_sequence=COLORS,text="CRM Leads")
            f2.update_traces(texttemplate="%{text:,.0f}",textposition="outside")
            f2.update_layout(height=220,margin=dict(t=0,b=0,l=0,r=45),showlegend=False,paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,visible=False),yaxis=dict(showgrid=False))
            st.plotly_chart(f2,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        with c3:
            st.markdown(sh("💰 Sales by Campaign")+sb_o(),unsafe_allow_html=True)
            sd=camp_df[camp_df["Sales Amount ($)"]>0].sort_values("Sales Amount ($)")
            f3=px.bar(sd,x="Sales Amount ($)",y="Campaign Objective",orientation="h",color="Campaign Objective",color_discrete_sequence=COLORS,text="Sales Amount ($)")
            f3.update_traces(texttemplate="$%{text:,.0f}",textposition="outside")
            f3.update_layout(height=220,margin=dict(t=0,b=0,l=0,r=65),showlegend=False,paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,visible=False),yaxis=dict(showgrid=False))
            st.plotly_chart(f3,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
        st.markdown(sh(f"📋 Campaign Breakdown — {sel}")+sb_o(),unsafe_allow_html=True)
        show=["Campaign Objective","Spend ($)","Impressions","Clicks","CRM Leads","Conversions","Appointments","Customers","Sales Amount ($)","ROAS"]
        tb=fd[[c for c in show if c in fd.columns]].copy()
        for col,func in [("Spend ($)",fc),("Impressions",fn),("Clicks",fn)]: tb[col]=tb[col].apply(func)
        for col in ["CRM Leads","Conversions","Customers"]: tb[col]=tb[col].apply(lambda x:fn(x) if x>0 else "—")
        tb["Appointments"]=tb["Appointments"].apply(fn)
        tb["Sales Amount ($)"]=tb["Sales Amount ($)"].apply(lambda x:fc(x) if x>0 else "—")
        tb["ROAS"]=tb["ROAS"].apply(lambda x:f"{x:.1f}x" if x>0 else "—")
        st.dataframe(tb,use_container_width=True,hide_index=True,height=180); st.markdown(sb_c(),unsafe_allow_html=True)

# ── PAGE 2 ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "trends":
    if "Daily Performance" not in data:
        st.warning("No Daily Performance sheet found."); st.stop()
    daily=data["Daily Performance"].copy(); daily["Date"]=pd.to_datetime(daily["Date"])
    if date_range and len(date_range)==2:
        daily=daily[(daily["Date"]>=pd.Timestamp(date_range[0]))&(daily["Date"]<=pd.Timestamp(date_range[1]))]
    if sel_camp!="All" and "Campaign" in daily.columns:
        daily=daily[daily["Campaign"]==sel_camp]
    agg=daily.groupby("Date").agg({"Spend ($)":"sum","Impressions":"sum","Reach":"sum","Clicks":"sum","CRM Leads":"sum","Conversions":"sum","Appointments":"sum","Customers":"sum","Sales Amount ($)":"sum","ROAS":"mean"}).reset_index()
    gc=st.columns([1,1,1,5])
    for i,(lbl,k) in enumerate([("Daily","Daily"),("Weekly","Weekly"),("Monthly","Monthly")]):
        if gc[i].button(lbl,key=f"g{i}",use_container_width=True,type="primary" if st.session_state.gran==lbl else "secondary"):
            st.session_state.gran=lbl; st.rerun()
    if st.session_state.gran=="Weekly":  agg=agg.resample("W", on="Date").sum().reset_index()
    if st.session_state.gran=="Monthly": agg=agg.resample("ME",on="Date").sum().reset_index()
    mopts=["Spend ($)","Sales Amount ($)","CRM Leads","Clicks","Conversions","Appointments","Customers","ROAS"]
    mshort=["Spend","Sales","Leads","Clicks","Conv.","Appt.","Cust.","ROAS"]
    mdefs=[True,True,True,False,False,False,False,False]
    mc=st.columns(8)
    sel_m=[m for i,(m,s,d) in enumerate(zip(mopts,mshort,mdefs)) if mc[i].checkbox(s,value=d,key=f"mx{i}")]
    st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
    if sel_m:
        st.markdown(sh("📈 Metrics Over Time")+sb_o(),unsafe_allow_html=True)
        fm=go.Figure()
        for m,col in zip(sel_m,COLORS):
            if m not in agg.columns: continue
            fm.add_trace(go.Scatter(x=agg["Date"],y=agg[m],name=m,mode="lines+markers",line=dict(color=col,width=2),marker=dict(size=3),hovertemplate=f"<b>%{{x|%b %d}}</b><br>{m}: %{{y:,.1f}}<extra></extra>"))
        fm.update_layout(**ch(230)); st.plotly_chart(fm,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    r1,r2=st.columns(2,gap="large")
    with r1:
        st.markdown(sh("💹 ROAS Trend")+sb_o(),unsafe_allow_html=True)
        fr=go.Figure(go.Scatter(x=agg["Date"],y=agg["ROAS"],mode="lines+markers",line=dict(color="#22c55e",width=2),fill="tozeroy",fillcolor="rgba(34,197,94,0.07)",hovertemplate="ROAS: %{y:.2f}x<extra></extra>"))
        fr.update_layout(height=190,margin=dict(t=8,b=28,l=44,r=10),paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,tickformat="%b %d"),yaxis=dict(showgrid=True,gridcolor="#f3f4f6",ticksuffix="x"))
        st.plotly_chart(fr,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    with r2:
        st.markdown(sh("💸 Spend vs Sales")+sb_o(),unsafe_allow_html=True)
        fsv=make_subplots(specs=[[{"secondary_y":True}]])
        fsv.add_trace(go.Bar(x=agg["Date"],y=agg["Spend ($)"],name="Spend",marker_color="rgba(24,119,242,0.65)",hovertemplate="$%{y:,.0f}<extra></extra>"),secondary_y=False)
        fsv.add_trace(go.Scatter(x=agg["Date"],y=agg["Sales Amount ($)"],name="Sales",line=dict(color="#22c55e",width=2),hovertemplate="$%{y:,.0f}<extra></extra>"),secondary_y=True)
        fsv.update_layout(height=190,margin=dict(t=8,b=28,l=44,r=44),paper_bgcolor="white",plot_bgcolor="white",legend=dict(orientation="h",y=1.1),hovermode="x unified",xaxis=dict(showgrid=False,tickformat="%b %d"))
        fsv.update_yaxes(showgrid=True,gridcolor="#f3f4f6",secondary_y=False); fsv.update_yaxes(showgrid=False,secondary_y=True)
        st.plotly_chart(fsv,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    r3,r4=st.columns(2,gap="large")
    with r3:
        st.markdown(sh("📡 Impressions & Reach")+sb_o(),unsafe_allow_html=True)
        fa=go.Figure()
        fa.add_trace(go.Scatter(x=agg["Date"],y=agg["Impressions"],name="Impressions",line=dict(color="#1877F2",width=2)))
        fa.add_trace(go.Scatter(x=agg["Date"],y=agg["Reach"],name="Reach",line=dict(color="#8b5cf6",width=2,dash="dash")))
        fa.update_layout(**ch(190)); st.plotly_chart(fa,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    with r4:
        st.markdown(sh("🎯 Conversion Funnel")+sb_o(),unsafe_allow_html=True)
        fcv=go.Figure()
        for m,col in [("Conversions","#10b981"),("Appointments","#06b6d4"),("Customers","#ec4899")]:
            fcv.add_trace(go.Scatter(x=agg["Date"],y=agg[m],name=m,line=dict(color=col,width=2)))
        fcv.update_layout(**ch(190)); st.plotly_chart(fcv,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)

# ── PAGE 3 ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "territory":
    if "Territory Performance" not in data:
        st.warning("No Territory Performance sheet found."); st.stop()
    raw=data["Territory Performance"].copy()
    t3c=["All Campaigns"]+sorted(raw["Campaign"].unique().tolist())
    s3=st.selectbox("Campaign",t3c,key="t3c",label_visibility="collapsed")
    tdf=raw if s3=="All Campaigns" else raw[raw["Campaign"]==s3]
    terr=tdf.groupby("Territory").agg({"Unique Leads":"sum","New Leads":"sum","Appointments":"sum","Quote":"sum","Customers":"sum","Sales Amount ($)":"sum","NL Customers":"sum","NL Sales ($)":"sum","Spend ($)":"sum","ROAS":"mean"}).reset_index()
    tot=terr.sum(numeric_only=True)
    for col,num,den in [("Leads %","Unique Leads",tot["Unique Leads"]),("Sales %","Sales Amount ($)",tot["Sales Amount ($)"])]:
        terr[col]=(terr[num]/den*100).round(2)
    terr["APT/Leads"]=(terr["Appointments"]/terr["Unique Leads"].replace(0,1)*100).round(2)
    terr["Order/APT"]=(terr["Customers"]/terr["Appointments"].replace(0,1)*100).round(2)
    terr["Order/Leads"]=(terr["Customers"]/terr["Unique Leads"].replace(0,1)*100).round(2)
    terr=terr.sort_values("Sales Amount ($)",ascending=False)
    ul=int(tot["Unique Leads"]); apt=int(tot["Appointments"]); cu=int(tot["Customers"]); sal=tot["Sales Amount ($)"]
    ap=round(apt/ul*100) if ul else 0
    def tcell(color,label,value):
        return ('<div style="background:white;border:1px solid #e5e7eb;border-radius:10px;padding:14px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.05)">'+
                f'<div style="height:4px;border-radius:3px;background:{color};margin-bottom:8px"></div>'+
                f'<div style="font-size:0.65rem;color:#9ca3af;font-weight:600;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px">{label}</div>'+
                f'<div style="font-size:1.2rem;font-weight:700;color:#111827">{value}</div></div>')
    st.markdown('<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:24px">'+tcell("#1877F2","Total Leads",fn(ul))+tcell("#10b981","Appointments",fn(apt))+tcell("#8b5cf6","Customers",fn(cu))+tcell("#22c55e","Total Sales",fc(sal))+tcell("#f59e0b","APT / Leads",f"{ap}%")+'</div>',unsafe_allow_html=True)
    d1,d2=st.columns(2,gap="large")
    with d1:
        st.markdown(sh("🥧 Leads % of Total")+sb_o(),unsafe_allow_html=True)
        fl=px.pie(terr,values="Unique Leads",names="Territory",hole=0.42,color_discrete_sequence=COLORS)
        fl.update_traces(textposition="inside",textinfo="percent",hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>")
        fl.update_layout(height=290,margin=dict(t=5,b=5,l=0,r=0),paper_bgcolor="white",legend=dict(font=dict(size=9)))
        st.plotly_chart(fl,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    with d2:
        st.markdown(sh("💰 Sales % of Total")+sb_o(),unsafe_allow_html=True)
        fs=px.pie(terr[terr["Sales Amount ($)"]>0],values="Sales Amount ($)",names="Territory",hole=0.42,color_discrete_sequence=COLORS)
        fs.update_traces(textposition="inside",textinfo="percent",hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>")
        fs.update_layout(height=290,margin=dict(t=5,b=5,l=0,r=0),paper_bgcolor="white",legend=dict(font=dict(size=9)))
        st.plotly_chart(fs,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
    st.markdown(sh("🏢 Regional Office Performance")+sb_o(),unsafe_allow_html=True)
    disp=terr[["Territory","Unique Leads","New Leads","Appointments","Quote","Customers","Sales Amount ($)","NL Customers","NL Sales ($)","Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]].copy()
    tr_r=pd.DataFrame([{"Territory":"Total","Unique Leads":int(tot["Unique Leads"]),"New Leads":int(tot["New Leads"]),"Appointments":int(tot["Appointments"]),"Quote":int(tot["Quote"]),"Customers":int(tot["Customers"]),"Sales Amount ($)":tot["Sales Amount ($)"],"NL Customers":int(tot["NL Customers"]),"NL Sales ($)":tot["NL Sales ($)"],"Leads %":100.0,"Sales %":100.0,"APT/Leads":round(tot["Appointments"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0,"Order/APT":round(tot["Customers"]/tot["Appointments"]*100,2) if tot["Appointments"] else 0,"Order/Leads":round(tot["Customers"]/tot["Unique Leads"]*100,2) if tot["Unique Leads"] else 0}])
    disp=pd.concat([disp,tr_r],ignore_index=True)
    for c in ["Sales Amount ($)","NL Sales ($)"]: disp[c]=disp[c].apply(lambda x:f"${x:,.2f}")
    for c in ["Leads %","Sales %","APT/Leads","Order/Leads"]: disp[c]=disp[c].apply(lambda x:f"{x:.2f}")
    disp["Order/APT"]=disp["Order/APT"].apply(lambda x:f"{x:.0f}%")
    disp.columns=["Regional Office","Unique Leads","New Leads","APT","Quote","Customers","Sales Amount","NL Customers","NL Sales","Leads %","Sales %","APT/Leads","Order/APT","Order/Leads"]
    st.dataframe(disp,use_container_width=True,hide_index=True,height=380); st.markdown(sb_c(),unsafe_allow_html=True)
    st.markdown(sh("📊 Campaign Breakdown by Territory")+sb_o(),unsafe_allow_html=True)
    tc=raw.copy()
    if sel_off!="All": tc=tc[tc["Territory"]==sel_off]
    pm=st.selectbox("Metric",["Sales Amount ($)","Unique Leads","Appointments","Customers","Spend ($)"],key="pm",label_visibility="collapsed")
    fg=px.bar(tc.sort_values("Territory"),x="Territory",y=pm,color="Campaign",barmode="group",color_discrete_sequence=COLORS,text_auto=".2s")
    fg.update_layout(height=280,margin=dict(t=8,b=80,l=50,r=10),paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False,tickangle=-30),yaxis=dict(showgrid=True,gridcolor="#f3f4f6"),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
    st.plotly_chart(fg,use_container_width=True); st.markdown(sb_c(),unsafe_allow_html=True)
