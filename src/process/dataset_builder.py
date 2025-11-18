from .calculate_ratios import calculate_ratios
from .rank_stocks import rank
import pandas as pd


def build_dataset(financial_dict):
    rows = []
    for ticker, data in financial_dict.items():
        ratios = calculate_ratios(data)
        row = {"ticker": ticker, **ratios}
        rows.append(row)


    df = pd.DataFrame(rows)
    df = rank(df)
    return df