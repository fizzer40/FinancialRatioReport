"""
financial_ratio_report.py
Main entry point for generating financial ratio reports.
"""

import argparse
from pathlib import Path

from data.ticker_loader import load_tickers
from data.storage import ParquetStorage
from services.ratio_service import RatioService


def run_report(ticker_file: str, output_dir: str, verbose: bool = False):
    # Load tickers
    tickers = load_tickers(ticker_file)
    if verbose:
        print(f"Loaded {len(tickers)} tickers...")

    # Prepare storage handler
    storage = ParquetStorage(Path(output_dir))

    # Create ratio service
    ratio_service = RatioService(storage)

    # Fetch ratios for each ticker
    for ticker in tickers:
        if verbose:
            print(f"Processing {ticker}...")
        try:
            ratios = ratio_service.fetch_ratios(ticker)
            ratio_service.store_ratios(ticker, ratios)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    if verbose:
        print("Run complete.")


def main():
    parser = argparse.ArgumentParser(description="Generate financial ratio reports.")
    parser.add_argument(
        "--tickers",
        required=True,
        help="Path to ticker list (CSV or TXT).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory where parquet ratio files will be saved.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )

    args = parser.parse_args()

    run_report(args.tickers, args.output, args.verbose)


if __name__ == "__main__":
    main()
