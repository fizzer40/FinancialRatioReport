from yahooquery import Ticker


def validate_ticker(ticker: str) -> bool:
    data = Ticker(ticker).price
    return isinstance(data, dict) and ticker in data