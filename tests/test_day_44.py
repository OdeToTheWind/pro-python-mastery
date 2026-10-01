"""Tests for Day 44 – Pandas."""

import pandas as pd
import pytest

from src.day_44_pandas_framework.main import (
    best_days,
    load_sales,
    main,
    monthly_pivot,
    revenue_by_store,
    summary,
)


@pytest.fixture
def df():
    return load_sales()


def test_load_sales_cleans_and_enriches(df):
    assert len(df) == 7
    assert df["units"].isna().sum() == 0
    assert df.loc[2, "units"] == 0
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df.loc[0, "revenue"] == 136.0
    assert list(df["month"].unique()) == ["2026-03", "2026-04"]


def test_revenue_by_store_sorted(df):
    result = revenue_by_store(df)
    assert list(result.index) == ["Airport", "Downtown", "Campus"]
    assert result["Airport"] == 270.5


def test_best_days_filter(df):
    result = best_days(df, 150)
    assert list(result.columns) == ["date", "store", "product", "revenue"]
    assert list(result["store"]) == ["Airport", "Campus"]


def test_monthly_pivot(df):
    pivot = monthly_pivot(df)
    assert pivot.loc["Latte", "2026-03"] == 95
    assert pivot.loc["Muffin", "2026-03"] == 0


def test_summary(df):
    assert summary(df) == {"rows": 7, "total_revenue": 774.8, "mean_units": 34.14,
                           "top_product": "Latte", "first_row_store": "Downtown"}


def test_custom_csv():
    df = load_sales("date,store,product,units,unit_price\n2026-01-01,X,Tea,2,1.5\n")
    assert df["revenue"].tolist() == [3.0]


def test_main(capsys):
    main()
    assert "Revenue by store" in capsys.readouterr().out
