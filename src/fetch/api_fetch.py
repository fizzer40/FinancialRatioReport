import yfinance as yf


def fetch_api_financials(ticker):
    try:
        stock = yf.Ticker(ticker)
        return {
        "ticker": ticker,
        "balance_sheet": stock.balance_sheet,
        "income_statement": stock.financials,
        "cashflow": stock.cashflow,
        }
    except Exception as e:
        print(f"API fetch failed for {ticker}: {e}")
        return None