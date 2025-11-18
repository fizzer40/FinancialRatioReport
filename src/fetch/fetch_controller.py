from .api_fetch import fetch_api_financials
from .scrape_fetch import scrape_financials


def fetch_financial_data(tickers):
    results = {}
    for t in tickers:
        data = fetch_api_financials(t)
        if data is None:
            data = scrape_financials(t)
        if data:
            results[t] = data
    return results