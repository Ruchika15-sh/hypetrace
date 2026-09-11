# HypeTrace
### Celebrity Influence & Trend Decay Analytics for the Fashion Industry

*Tracking how fame moves fashion — and how fast it fades.*

---

## Overview

HypeTrace is an end-to-end data analytics project that measures how celebrity endorsements and controversies affect public demand (via Google Trends search interest) and brand value (via parent-company stock price) in the fashion industry.

The project combines a full ETL pipeline, a relational PostgreSQL database, SQL analysis, a Power BI business dashboard, and a custom multi-page Plotly/Dash web app for deeper, code-driven interactivity.


**Power BI dashboard:** see `/powerbi/hypetrace_dashboard.pbix`

---

## Key Questions Explored

- Does a celebrity endorsement or controversy measurably move public search interest in a brand?
- Do controversies suppress demand more than endorsements boost it, or vice versa?
- How does search interest relate to a brand's (or parent company's) stock price?
- How quickly does a spike in public interest decay back to baseline?

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data collection | Python, `pytrends` (Google Trends), `yfinance` (stock prices) |
| Data cleaning / EDA | pandas, numpy, matplotlib |
| Database | PostgreSQL (migrated to Neon for cloud deployment) |
| ETL | Python + SQLAlchemy |
| Analysis | SQL (joins, window functions), Python (event-study methodology, `scipy` curve fitting) |
| Business dashboard | Power BI |
| Interactive app | Plotly, Dash |

---

## Why Three Visualization Tools?

This project deliberately uses **matplotlib**, **Power BI**, and **Plotly/Dash** — each for a different purpose, not redundantly:

- **matplotlib** — used only during exploratory data analysis (EDA) in Jupyter notebooks, for quick, disposable sanity checks while cleaning and understanding the data.
- **Power BI** — the business-facing dashboard, built for a non-technical viewer to explore KPIs and filter by brand without touching code. Demonstrates BI-tool competency.
- **Plotly/Dash** — a custom-built, multi-page interactive app used specifically where Power BI's out-of-the-box visuals fall short: rich custom hover tooltips tied directly to Python analysis logic, and a curve-fitting trend-decay model that isn't a standard BI chart type.

---

## Project Structure

```
hypetrace/
├── data/
│   ├── raw/              # untouched scraped/collected data
│   └── processed/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_event_study.ipynb
│   └── 04_trend_decay_model.ipynb
├── src/
│   ├── scrape_trends.py
│   ├── scrape_stocks.py
│   ├── db_connection.py
│   ├── db_schema.sql
│   └── queries.sql
├── dashboard/
│   ├── app.py
│   ├── db.py
│   └── pages/
│       ├── overview.py
│       ├── event_study.py
│       ├── trend_decay.py
│       └── brand_comparison.py
├── powerbi/
│   └── hypetrace_dashboard.pbix
└── reports/
    └── figures/
```

---

## Data Sources

- **Google Trends**: 5 years of weekly search interest for 8 fashion brands (Gucci, Nike, Zara, Balenciaga, H&M, Valentino, Christian Dior, Louis Vuitton)
- **Stock prices**: weekly closing prices for 9 publicly traded parent companies (Nike, LVMH, Kering, Inditex, Adidas, Ralph Lauren, Capri Holdings, Tapestry, H&M) via `yfinance`
- **Events dataset**: 11 manually curated real-world celebrity endorsement/controversy events, each tagged with brand, celebrity, date, event type, occasion, description, and source link

### Note on data coverage
Search-interest and stock data are only available for brands with individual public trading or search-trend history. Several sub-brands (Gucci, Balenciaga, Valentino, Christian Dior, Louis Vuitton, Zara) don't trade individually — they're owned by parent companies (Kering, LVMH, Inditex). To make stock comparisons meaningful, sub-brands were mapped to their parent company's stock price via a `parent_company` column and a SQL view (`brand_stock_trend_summary`). This is a deliberate modeling choice, documented here for transparency.

---

## Database Design

Normalized PostgreSQL schema:

- `brands` — dimension table (brand_id, brand_name, parent_company)
- `trend_metrics` — weekly search interest per brand
- `stock_prices` — weekly close price per (parent) brand
- `events` — celebrity/controversy events, linked to brands
- `brand_stock_trend_summary` — view joining sub-brands to parent-company stock data

See `src/db_schema.sql` for full definitions and `src/queries.sql` for analytical SQL queries, including window functions (rolling averages, brand popularity ranking).

---

## Methodology: Event Study

For each curated event, we compare average search interest in a 14-day window **before** the event to a 14-day window **after** it:

```
lift % = ((after_avg - before_avg) / before_avg) × 100
```

This is a simplified version of the event-study methodology used in finance/marketing analytics to isolate the impact of a specific event on a metric.

**Key finding:** results are brand- and context-dependent. Controversies do not consistently suppress demand more than endorsements boost it — e.g., a Kate Middleton endorsement of Zara produced a modest +8.5% lift, while a Demi Moore endorsement of Gucci was followed by a -52% drop, likely influenced by broader seasonal patterns rather than the event alone. This nuance is intentionally preserved rather than flattened into a simple narrative.

---

## Methodology: Trend Decay

Using the Balenciaga controversy (Nov 2022) as a case study, an exponential decay curve (`a·e^(-b·x) + c`) is fitted to search interest over the 90 days following the peak, using `scipy.optimize.curve_fit`. This yields an estimated **half-life** — the time for interest to fall to half its peak intensity (~91 days for this event).

**Caveat:** the curve fit includes 14 days of pre-spike baseline data to anchor the model's lower bound, so it models "peak relative to normal" rather than pure post-peak decay in isolation. This is documented as a deliberate methodology choice.

---

## Setup / Running Locally

```bash
# clone and set up environment
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# add a .env file with:
# DB_HOST=...
# DB_NAME=...
# DB_USER=...
# DB_PASSWORD=...

# run the Dash app
py dashboard/app.py
```

---

## Future Improvements

- Expand the curated events dataset beyond 11 entries for a larger sample
- Add sentiment analysis on news/social mentions around each event
- Extend trend-decay modeling across multiple events, not just one case study
- Add authentication + write-back so the events dataset can be crowd-sourced/expanded over time

---

## Author

Built as a portfolio project to demonstrate an end-to-end analytics workflow: data collection, ETL, SQL, exploratory analysis, event-study methodology, and both BI and custom interactive visualization.