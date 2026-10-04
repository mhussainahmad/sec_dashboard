# sec_dashboard

A small Flask app that looks up a company by ticker and shows its annual revenue, gross profit and net income from SEC EDGAR's XBRL data, as tables and line charts.

## Overview

- On startup, `app.py` downloads `https://www.sec.gov/files/company_tickers.json` to map tickers to CIK numbers.
- The search form (`templates/index.html`) posts a ticker to `/search`.
- `/search` fetches `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` for that company and pulls three US-GAAP concepts:
  - `RevenueFromContractWithCustomerExcludingAssessedTax`
  - `GrossProfit`
  - `NetIncomeLoss`
- For each concept it keeps the 10-K values with calendar-year frames (CY1994 to CY2023). It then renders them in `templates/search.html` as a table plus a Chart.js line chart, with values in billions of USD.

A company that does not report a concept (for example, older filers without the ASC 606 revenue tag) shows `-` for that section.

## Repository layout

```
app.py              Flask app: ticker lookup, EDGAR requests, data shaping
templates/
  index.html        Ticker search form (Bootstrap)
  search.html       Tables and Chart.js charts for the three metrics
requirements.txt
```

## Getting started

```bash
pip install -r requirements.txt requests numpy   # requests and numpy are imported but not listed in requirements.txt
python app.py                                      # serves on http://127.0.0.1:5000 in debug mode
```

The SEC asks automated clients to send a descriptive `User-Agent` with a contact address. Replace the placeholder `headers = {'User-Agent': "email@email.com"}` in `app.py` with your own before running.

## Limitations

- Tickers must exactly match the SEC list (uppercase, e.g. `AAPL`). An unknown ticker is not handled and raises an error.
- The year range is fixed in code. The start/end year inputs are present but commented out.

## Tech stack

Python, Flask, pandas, requests, Bootstrap 5, Chart.js.
