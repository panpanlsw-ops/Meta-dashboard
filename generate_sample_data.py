import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()

# ── Sheet 1: Overview ──────────────────────────────────────────────────────────
ws1 = wb.active
ws1.title = "Overview"

header_font = Font(bold=True, color="FFFFFF", size=11)
header_fill = PatternFill("solid", start_color="1877F2")
center = Alignment(horizontal="center", vertical="center")

overview_headers = ["Metric","Current Period","Previous Period","Change %"]
for col, h in enumerate(overview_headers, 1):
    c = ws1.cell(1, col, h)
    c.font = header_font; c.fill = header_fill; c.alignment = center

overview_data = [
    ["Spend ($)",        112300,  128700, -12.7],
    ["Clicks",           263900,  305700, -13.7],
    ["Conversions",        2700,    3546, -23.8],
    ["CRM Leads",          3100,    4600, -32.4],
    ["Appointments",        480,     390,  23.1],
    ["Customers",           210,     175,  20.0],
    ["Sales Amount ($)", 560000,  430000,  30.2],
]
for row in overview_data:
    ws1.append(row)

for col in range(1, 5):
    ws1.column_dimensions[get_column_letter(col)].width = 22

# ── Sheet 2: Campaign Performance ─────────────────────────────────────────────
ws2 = wb.create_sheet("Campaign Performance")

camp_headers = ["Campaign Objective","Spend ($)","Impressions","CPM ($)",
                "Clicks","CPC ($)","CRM Leads","Conversions","ROAS","CTR (%)"]
for col, h in enumerate(camp_headers, 1):
    c = ws2.cell(1, col, h)
    c.font = header_font; c.fill = header_fill; c.alignment = center

camp_data = [
    ["OUTCOME_SALES",      90900, 16100000, 5.64, 201300, 0.45, 665,  2000, 25.6, 1.25],
    ["CONVERSIONS",        17200,  2800000, 6.14,  35300, 0.49, 316,   717,  0.8, 1.26],
    ["OUTCOME_TRAFFIC",     1200,   331700, 3.62,  14100, 0.09,   0,     0, -1.0, 4.25],
    ["OUTCOME_AWARENESS",    143,    73800, 1.94,     33, 4.33,   1,     0, -1.0, 0.04],
    ["OUTCOME_ENGAGEMENT",  1900,   982600, 1.93,   7200, 0.26,   2,     0, -1.0, 0.73],
    ["OUTCOME_LEADS",        931,   271600, 3.43,   6000, 0.16, 2200,    0, -1.0, 2.21],
]
for row in camp_data:
    ws2.append(row)

col_widths = [22,12,14,10,10,10,10,12,10,10]
for i, w in enumerate(col_widths, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

# ── Sheet 3: Daily Performance ────────────────────────────────────────────────
ws3 = wb.create_sheet("Daily Performance")

daily_headers = ["Date","Spend ($)","Impressions","Reach","Clicks",
                 "CRM Leads","Conversions","Appointments","Customers","Sales Amount ($)","ROAS"]
for col, h in enumerate(daily_headers, 1):
    c = ws3.cell(1, col, h)
    c.font = header_font; c.fill = header_fill; c.alignment = center

import random, datetime
random.seed(42)
base = datetime.date(2024, 12, 1)
for i in range(31):
    d = base + datetime.timedelta(days=i)
    spend        = round(random.uniform(2800, 4500), 2)
    impr         = random.randint(500000, 900000)
    reach        = random.randint(140000, 220000)
    clicks       = random.randint(6000, 12000)
    crm_leads    = random.randint(60, 150)
    conversions  = random.randint(50, 120)
    appointments = random.randint(10, 30)
    customers    = random.randint(4, 15)
    sales        = round(random.uniform(12000, 28000), 2)
    roas         = round(random.uniform(3.5, 8.0), 2)
    ws3.append([d.strftime("%Y-%m-%d"), spend, impr, reach, clicks,
                crm_leads, conversions, appointments, customers, sales, roas])

for i, w in enumerate([14,12,14,12,10,12,12,14,12,18,8], 1):
    ws3.column_dimensions[get_column_letter(i)].width = w

# ── Sheet 4: Ad Set Performance ───────────────────────────────────────────────
ws4 = wb.create_sheet("Ad Set Performance")

adset_headers = ["Ad Set Name","Campaign","Spend ($)","Impressions",
                 "Clicks","CTR (%)","CPC ($)","CRM Leads","Conversions","ROAS"]
for col, h in enumerate(adset_headers, 1):
    c = ws4.cell(1, col, h)
    c.font = header_font; c.fill = header_fill; c.alignment = center

adsets = [
    ["Lookalike 1% - USA",      "OUTCOME_SALES",   18500, 3200000, 42000, 1.31, 0.44, 140, 410, 28.3],
    ["Retargeting - 30d",       "OUTCOME_SALES",   22100, 2100000, 38500, 1.83, 0.57, 180, 520, 30.1],
    ["Interest: Fitness",       "OUTCOME_SALES",   15400, 2800000, 31000, 1.11, 0.50, 110, 310, 22.5],
    ["Broad - 25-44",           "CONVERSIONS",      8900, 1200000, 16000, 1.33, 0.56,  95, 290, 18.7],
    ["Lookalike 3% - Global",   "OUTCOME_TRAFFIC",    600,  165000,  7100, 4.30, 0.08,   0,   0, -1.0],
    ["Page Engagement",         "OUTCOME_ENGAGEMENT", 950,  490000,  3600, 0.73, 0.26,   1,   0, -1.0],
    ["Lead Gen - Female 25-35", "OUTCOME_LEADS",      460,  135000,  3000, 2.22, 0.15, 1100,  0, -1.0],
    ["Conversion - Cart",       "OUTCOME_SALES",   12800, 2100000, 28000, 1.33, 0.46,  90, 340, 24.1],
    ["Brand Awareness - Video", "OUTCOME_AWARENESS",  143,   73800,    33, 0.04, 4.33,   1,   0, -1.0],
    ["DABA - Shopify",          "CONVERSIONS",      8300, 1600000, 19300, 1.21, 0.43, 221, 427, 22.3],
]
for row in adsets:
    ws4.append(row)

col_ws4 = [24,22,12,14,10,10,10,12,12,10]
for i, w in enumerate(col_ws4, 1):
    ws4.column_dimensions[get_column_letter(i)].width = w

wb.save("meta_ads_data.xlsx")
print("Excel file created successfully!")
