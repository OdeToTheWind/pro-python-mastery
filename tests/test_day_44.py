# tests/test_day_44.py
import pandas as pd

def test_pandas_dataframe():
    data = {"Name": ["A", "B"], "Score": [90, 85]}
    df = pd.DataFrame(data)
    assert len(df) == 2
    assert df["Score"].mean() == 87.5