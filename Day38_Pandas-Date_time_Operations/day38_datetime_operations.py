# ============================================================
# DAY 38 — DATE-TIME OPERATIONS
# Topics: pd.to_datetime, .dt accessor, timedelta, date
#         filtering, strftime/strptime, date_range
# File: Day38_DateTime_Practice.xlsx
# ============================================================

import pandas as pd
from datetime import datetime, timedelta


# ── LOAD EXCEL ───────────────────────────────────────────────────────────────
FILE = "Day38_DateTime_Practice.xlsx"

df_txn   = pd.read_excel(FILE, sheet_name="Raw_Transactions")
df_stock = pd.read_excel(FILE, sheet_name="Stock_Prices")

print("=" * 60)
print("LOADED RAW_TRANSACTIONS")
print("=" * 60)
print(df_txn[["Transaction_ID", "Date_Raw", "Category", "Amount_INR"]].head(5))
print(f"\nDate_Raw dtype (before parse): {df_txn['Date_Raw'].dtype}")


# ============================================================
# CONCEPT 1 — pd.to_datetime()
# Converts string / mixed date text → proper datetime object
# infer_datetime_format=True → pandas auto-detects format
# dayfirst=True → tells pandas DD/MM/YYYY not MM/DD/YYYY
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 1 — pd.to_datetime() with mixed formats")
print("=" * 60)

# When formats are MIXED (3 different styles in this column),
# we must use errors='coerce' to prevent crashing.
# We then handle remaining NaTs with a second pass.

df_txn["Date"] = pd.to_datetime(df_txn["Date_Raw"],dayfirst=True,errors="coerce")  # NaT if it can't parse

print(f"\nDates parsed: {df_txn['Date'].notna().sum()} / {len(df_txn)}")
print(f"Date dtype now: {df_txn['Date'].dtype}")
print("\nFirst 5 parsed dates:")
print(df_txn[["Date_Raw", "Date"]].head(5).to_string(index=False))


# ============================================================
# CONCEPT 2 — .dt ACCESSOR
# Once a column is datetime dtype, the .dt accessor unlocks
# all date component extraction properties.
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 2 — .dt Accessor (extracting date components)")
print("=" * 60)

df_txn["Year"]        = df_txn["Date"].dt.year          # int: 2026
df_txn["Month"]       = df_txn["Date"].dt.month         # int: 1–12
df_txn["Day"]         = df_txn["Date"].dt.day           # int: 1–31
df_txn["Day_Name"]    = df_txn["Date"].dt.day_name()    # 'Monday', 'Tuesday'...
df_txn["Month_Name"]  = df_txn["Date"].dt.month_name()  # 'January', 'February'...
df_txn["Quarter"]     = df_txn["Date"].dt.quarter       # int: 1–4
df_txn["Week_Number"] = df_txn["Date"].dt.isocalendar().week.astype("Int64")
df_txn["Is_Weekend"]  = df_txn["Date"].dt.weekday >= 5  # 5=Sat, 6=Sun → True

print("\nDate components extracted:")
cols = ["Date", "Year", "Month", "Month_Name", "Day_Name", "Quarter", "Is_Weekend"]
print(df_txn[cols].head(8).to_string(index=False))


# ============================================================
# CONCEPT 3 — DATETIME ARITHMETIC with timedelta
# timedelta = a duration of time. You can add/subtract it
# from a datetime to get a new datetime.
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 3 — Datetime Arithmetic (timedelta)")
print("=" * 60)

today = datetime.today()

# Days since each transaction
df_txn["Days_Ago"] = (today - df_txn["Date"]).dt.days

# Is transaction within the last 90 days?
df_txn["Within_90_Days"] = df_txn["Days_Ago"] <= 90

print(f"\nToday's date: {today.strftime('%d %B %Y')}")
print("\nDays since each transaction (first 5):")
print(df_txn[["Date", "Description", "Days_Ago", "Within_90_Days"]].head(5).to_string(index=False))

# Manual timedelta examples
print("\n--- timedelta examples ---")
print(f"Today + 30 days  : {(today + timedelta(days=30)).strftime('%d %b %Y')}")
print(f"Today - 90 days  : {(today - timedelta(days=90)).strftime('%d %b %Y')}")
print(f"Today + 1 year   : {(today + timedelta(days=365)).strftime('%d %b %Y')}")


# ============================================================
# CONCEPT 4 — FILTERING BY DATE RANGE
# Boolean masks using comparison operators on datetime column
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 4 — Filtering by Date Range")
print("=" * 60)

# Method A: Filter by specific month
jan_mask = (df_txn["Month"] == 1) & (df_txn["Year"] == 2026)
df_jan   = df_txn[jan_mask]
print(f"\nJanuary 2026 transactions: {len(df_jan)}")
print(df_jan[["Date", "Description", "Amount_INR"]].to_string(index=False))

# Method B: Filter by date range (Q1 = Jan–Mar)
q1_start = pd.Timestamp("2026-01-01")
q1_end   = pd.Timestamp("2026-03-31")
df_q1    = df_txn[(df_txn["Date"] >= q1_start) & (df_txn["Date"] <= q1_end)]
print(f"\nQ1 2026 (Jan–Mar) transactions: {len(df_q1)}")

# Method C: Weekend transactions only
df_weekend = df_txn[df_txn["Is_Weekend"]]
print(f"\nWeekend transactions: {len(df_weekend)}")
print(df_weekend[["Date", "Day_Name", "Description", "Amount_INR"]].to_string(index=False))


# ============================================================
# CONCEPT 5 — strftime() and strptime()
# strftime = datetime → string (format FOR output)
# strptime = string → datetime (parse FROM string)
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 5 — strftime() & strptime()")
print("=" * 60)

# strftime — format a datetime as a custom string
sample_date = datetime(2026, 4, 25)
print(f"\nstrftime examples on {sample_date}:")
print(f"  '%d-%m-%Y'         → {sample_date.strftime('%d-%m-%Y')}")
print(f"  '%B %d, %Y'        → {sample_date.strftime('%B %d, %Y')}")
print(f"  '%A, %d %b %Y'     → {sample_date.strftime('%A, %d %b %Y')}")
print(f"  '%d/%m/%Y %H:%M'   → {sample_date.strftime('%d/%m/%Y %H:%M')}")
print(f"  '%Y-%m'            → {sample_date.strftime('%Y-%m')}   ← Month label")

# strptime — parse a string into datetime
date_str = "25-04-2026"
parsed   = datetime.strptime(date_str, "%d-%m-%Y")
print(f"\nstrptime: '{date_str}' → {parsed}")

# Apply strftime on the full column
df_txn["Date_Formatted"] = df_txn["Date"].dt.strftime("%d %b %Y")
print("\nFormatted dates column (first 5):")
print(df_txn[["Date", "Date_Formatted"]].head(5).to_string(index=False))


# ============================================================
# CONCEPT 6 — pd.date_range()
# Generate a sequence of dates — very useful for reports,
# time series analysis, and filling missing trading days.
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 6 — pd.date_range()")
print("=" * 60)

# Daily range
daily = pd.date_range(start="2026-04-01", end="2026-04-07", freq="D")
print(f"\nDaily range (Apr 1–7): {list(daily.strftime('%d %b'))}")

# Business days only (Mon–Fri)
bdays = pd.date_range(start="2026-04-01", end="2026-04-15", freq="B")
print(f"Business days (Apr 1–15): {list(bdays.strftime('%d %b (%a)'))}")

# Monthly periods
monthly = pd.date_range(start="2026-01-01", periods=6, freq="MS")  # MS = Month Start
print(f"Monthly (6 periods): {list(monthly.strftime('%b %Y'))}")


# ============================================================
# CONCEPT 7 — STOCK DATA: Daily % Returns + Date Filtering
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 7 — Stock Price Date Analysis")
print("=" * 60)

df_stock["Date"] = pd.to_datetime(df_stock["Date"])
df_stock["Day_Name"] = df_stock["Date"].dt.day_name()
df_stock["Month"]    = df_stock["Date"].dt.month

# Daily % return for NIFTY 50
df_stock["NIFTY_Return_%"] = df_stock["NIFTY_50"].pct_change() * 100
df_stock["NIFTY_Return_%"] = df_stock["NIFTY_Return_%"].round(2)

print("\nStock data with returns (first 6 rows):")
print(df_stock[["Date", "Day_Name", "NIFTY_50", "NIFTY_Return_%"]].head(6).to_string(index=False))

# Best & worst NIFTY day
best_day  = df_stock.loc[df_stock["NIFTY_Return_%"].idxmax()]
worst_day = df_stock.loc[df_stock["NIFTY_Return_%"].idxmin()]
print(f"\nBest NIFTY day : {best_day['Date'].strftime('%d %b %Y')} → +{best_day['NIFTY_Return_%']}%")
print(f"Worst NIFTY day: {worst_day['Date'].strftime('%d %b %Y')} →  {worst_day['NIFTY_Return_%']}%")

# Filter: Only Mondays
df_mondays = df_stock[df_stock["Day_Name"] == "Monday"]
print(f"\nMonday sessions only ({len(df_mondays)} found):")
print(df_mondays[["Date", "Day_Name", "NIFTY_50", "NIFTY_Return_%"]].to_string(index=False))


# ============================================================
# CONCEPT 8 — MONTHLY INCOME vs EXPENSE SUMMARY (Real Use Case)
# ============================================================
print("\n" + "=" * 60)
print("CONCEPT 8 — Monthly Income vs Expense Summary")
print("=" * 60)

df_txn["Type"] = df_txn["Amount_INR"].apply(lambda x: "Income" if x > 0 else "Expense")
df_txn["Month_Label"] = df_txn["Date"].dt.strftime("%Y-%m")

monthly_summary = df_txn.groupby(["Month_Label", "Type"])["Amount_INR"].sum().unstack(fill_value=0)
if "Income" not in monthly_summary.columns:
    monthly_summary["Income"] = 0
if "Expense" not in monthly_summary.columns:
    monthly_summary["Expense"] = 0

monthly_summary["Net_Savings"]  = monthly_summary["Income"] + monthly_summary["Expense"]
monthly_summary["Savings_Rate"] = (monthly_summary["Net_Savings"] / monthly_summary["Income"] * 100).round(1)

print("\nMonthly Summary (INR):")
print(monthly_summary.to_string())


# ── EXPORT RESULTS ───────────────────────────────────────────────────────────
output_cols = [
    "Transaction_ID", "Date_Raw", "Date", "Date_Formatted",
    "Year", "Month", "Month_Name", "Day_Name", "Quarter",
    "Is_Weekend", "Days_Ago", "Description", "Category", "Amount_INR", "Type"
]

with pd.ExcelWriter("Day38_Output.xlsx", engine="openpyxl") as writer:
    df_txn[output_cols].to_excel(writer, sheet_name="Parsed_Transactions", index=False)
    df_stock.to_excel(writer, sheet_name="Stock_Analysis", index=False)
    monthly_summary.to_excel(writer, sheet_name="Monthly_Summary")

print("\n✅ Output saved to Day38_Output.xlsx")
print("\n--- TASK CHECKLIST ---")
print("[✓] Parsed 3 mixed date formats with pd.to_datetime()")
print("[✓] Extracted year, month, day, day_name, quarter, weekend flag")
print("[✓] Calculated days_ago using timedelta arithmetic")
print("[✓] Filtered by month, quarter, date range, weekday")
print("[✓] Used strftime for display formatting")
print("[✓] Used pd.date_range() to generate sequences")
print("[✓] Calculated stock daily % returns")
print("[✓] Built monthly income vs expense summary")