# 📊 Meta Ads Dashboard

A Streamlit dashboard that replicates a Meta Ads overview with KPI cards, charts, and tables — powered by Excel data files.

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone this repo
git clone https://github.com/YOUR_USERNAME/meta-ads-dashboard.git
cd meta-ads-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data (first time only)
python generate_sample_data.py

# 4. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/meta-ads-dashboard.git
   git push -u origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click **New app**
   - Select your repo → `app.py` → Deploy

3. **Done!** Your dashboard is live at `https://your-app.streamlit.app`

---

## 📁 Project Structure

```
meta-ads-dashboard/
├── app.py                    # Main Streamlit dashboard
├── generate_sample_data.py   # Creates sample Excel file
├── meta_ads_data.xlsx        # Sample data (auto-generated)
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 📊 Excel File Format

Your Excel file should have **4 sheets** with these columns:

### Sheet 1: `Overview`
| Metric | Current Period | Previous Period | Change % |
|--------|---------------|-----------------|----------|
| Spend ($) | 112300 | 128700 | -12.7 |
| Impressions | 20500000 | 23900000 | -14.2 |
| ... | | | |

### Sheet 2: `Campaign Performance`
| Campaign Objective | Spend ($) | Impressions | CPM ($) | Clicks | CPC ($) | Leads | Purchases | ROAS | CTR (%) |
|--------------------|-----------|-------------|---------|--------|---------|-------|-----------|------|---------|

### Sheet 3: `Daily Performance`
| Date | Spend ($) | Impressions | Reach | Clicks | Leads | Purchases | ROAS | Frequency |
|------|-----------|-------------|-------|--------|-------|-----------|------|-----------|

### Sheet 4: `Ad Set Performance`
| Ad Set Name | Campaign | Spend ($) | Impressions | Clicks | CTR (%) | CPC ($) | Leads | Purchases | ROAS |
|-------------|----------|-----------|-------------|--------|---------|---------|-------|-----------|------|

---

## 🔌 Connecting Your Own Data

**Option A — Upload via UI**
Use the file uploader in the sidebar to upload your `.xlsx` file directly.

**Option B — Replace the sample file**
Replace `meta_ads_data.xlsx` with your own file that follows the column structure above.

**Option C — Export from Meta Ads Manager**
1. Open Meta Ads Manager → Reporting
2. Customize columns to match the headers above
3. Export as Excel
4. Upload via the dashboard sidebar

---

## 📈 Dashboard Features

| Feature | Description |
|---------|-------------|
| 🔢 KPI Cards | Spend, Impressions, Reach, Frequency, Clicks, Leads, Purchases, ROAS |
| 🥧 Budget Pie Chart | Spend distribution by campaign objective |
| 📋 Campaign Table | Full metrics table by objective |
| 📅 Daily Trends | Line chart with 7-day rolling average |
| 💹 Spend vs ROAS | Dual-axis bar + line chart |
| 🎯 Top Ad Sets | Horizontal bar chart colored by ROAS |
| 🔍 Scatter Plot | Clicks vs Leads bubble chart |
| 📊 Ad Set Table | Full ad set performance report |
| 📥 CSV Export | Download filtered daily data |
| 🗓️ Date Filter | Filter daily charts by date range |
| 🎯 Campaign Filter | Filter by campaign objective |

---

## 🛠️ Customization Tips

- **Add your logo**: Replace the emoji header with an `st.image()` call
- **Add more metrics**: Extend the Overview sheet and the `row1_metrics` / `row2_metrics` lists in `app.py`
- **Change colors**: Edit `CHART_COLORS` and `META_BLUE` at the top of `app.py`
- **Connect to API**: Replace `load_excel()` with a Meta Marketing API call using `facebook-business` SDK

---

## 📦 Dependencies

- **Streamlit** — web app framework
- **Plotly** — interactive charts
- **Pandas** — data processing
- **OpenPyXL** — Excel file reading

---

*Built with ❤️ using Streamlit + Plotly*
