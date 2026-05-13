# Day 38 — Date-Time Operations with pandas

**Roadmap Phase:** 3 — Data Cleaning & Processing  
**Date:** May 13, 2026  
**Author:** Bhanu Pratap Singh

---

## What This Does

Parses, manipulates, and filters financial date data using Python's `datetime` module and pandas `.dt` accessor.  
Covers mixed-format date parsing, component extraction, timedelta arithmetic, date-range filtering, and monthly financial summaries.

---

## Files

| File | Description |
|---|---|
| `Day38_DateTime_Practice.xlsx` | Input — 25 transactions (mixed date formats) + 20-day stock OHLC |
| `day38_datetime_operations.py` | Main script — all 8 concepts with finance context |
| `Day38_Output.xlsx` | Output — parsed transactions, stock analysis, monthly P&L |

---

## Key Concepts Covered

| Concept | Tool | Use Case |
|---|---|---|
| Date parsing | `pd.to_datetime()` | Convert string dates → datetime |
| Component extraction | `.dt.year / .month / .day_name()` | Build time-based filters |
| Datetime arithmetic | `timedelta` | Days since transaction |
| Date range filter | Boolean mask on datetime column | Q1 filter, monthly filter |
| String formatting | `.dt.strftime()` | Human-readable date display |
| String parsing | `datetime.strptime()` | Parse custom date strings |
| Date sequences | `pd.date_range(freq='B')` | Generate business day calendars |
| Financial analysis | `.pct_change()` + date filter | Stock daily return by weekday |

---

## How to Run

```bash
# Place Day38_DateTime_Practice.xlsx in the same folder, then:
python day38_datetime_operations.py
```

**Requirements:** `pandas`, `openpyxl`

```bash
pip install pandas openpyxl
```

---

## Portfolio Connection

- Monthly income vs expense summary → **Expense Tracker Project (Day 80)**
- Stock return analysis by date → **Financial Dashboard (Day 78)**
- Date-range filtering pipeline → **Sales Data Analyzer (Day 50)**
