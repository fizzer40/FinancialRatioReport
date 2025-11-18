def main():
    from src.tickers.load_tickers import load_ticker_list
    from src.fetch.fetch_controller import fetch_financial_data
    from src.process.dataset_builder import build_dataset
    from src.export.export_excel import export_rankings


print("Running daily financial scan...")


tickers = load_ticker_list()
financials = fetch_financial_data(tickers)
dataset = build_dataset(financials)
export_rankings(dataset)


print("Scan complete.")




if __name__ == "__main__":
    main()