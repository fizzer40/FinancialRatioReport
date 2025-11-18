import pandas as pd
from pathlib import Path


def load_ticker_list():
    file_path = Path("data/tickers_master.csv")
    if not file_path.exists():
        print("Ticker file not found.")
        return []
    df = pd.read_csv(file_path)
    return df["ticker"].dropna().unique().tolist()