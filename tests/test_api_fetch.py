import pandas as pd
from src.fetch.api_fetch import yq_ratios


def test_yq_ratios_empty():
    df = yq_ratios([], 0)
    assert df == "BLANK"