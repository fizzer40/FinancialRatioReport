import pandas as pd
from datetime import datetime
from pathlib import Path


def export_rankings(df):
    output_path = Path("data/ratios_latest.xlsx")
    df.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")