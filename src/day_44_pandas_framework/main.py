"""Day 44 – Introduction to the Pandas Framework.

Scenario: a *coffee-chain sales analysis* – load a CSV into a DataFrame,
clean it, add derived columns and answer business questions.

Deliverables (syllabus):
* DataFrames (creation, ``read_csv``, dtypes, ``loc``/``iloc``)
* Data-analysis basics (cleaning, filtering, derived columns, ``groupby``,
  sorting, pivot tables, summary statistics)
"""

from __future__ import annotations

import io

import pandas as pd

DELIVERABLES: dict[str, str] = {
    "creating a DataFrame from CSV": "load_sales",
    "cleaning (missing values, types)": "load_sales",
    "derived columns": "load_sales",
    "selection with loc / iloc and boolean masks": "best_days",
    "groupby aggregation": "revenue_by_store",
    "pivot table": "monthly_pivot",
    "summary statistics": "summary",
}

SALES_CSV = """date,store,product,units,unit_price
2026-03-30,Downtown,Latte,40,3.40
2026-03-30,Airport,Latte,55,3.90
2026-03-31,Downtown,Espresso,,2.20
2026-04-01,Downtown,Latte,38,3.40
2026-04-01,Airport,Muffin,20,2.80
2026-04-02,Campus,Latte,61,3.10
2026-04-02,Campus,Espresso,25,2.00
"""


def load_sales(csv_text: str = SALES_CSV) -> pd.DataFrame:
    """Read, clean and enrich the raw sales data."""
    df = pd.read_csv(io.StringIO(csv_text), parse_dates=["date"])
    df["units"] = df["units"].fillna(0).astype(int)  # missing count → 0 sold
    df["revenue"] = (df["units"] * df["unit_price"]).round(2)
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df


def revenue_by_store(df: pd.DataFrame) -> pd.Series:
    return df.groupby("store")["revenue"].sum().sort_values(ascending=False).round(2)


def best_days(df: pd.DataFrame, min_revenue: float) -> pd.DataFrame:
    """Boolean mask + ``loc`` column selection."""
    mask = df["revenue"] >= min_revenue
    return df.loc[mask, ["date", "store", "product", "revenue"]].reset_index(drop=True)


def monthly_pivot(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="product", columns="month", values="units", aggfunc="sum", fill_value=0)


def summary(df: pd.DataFrame) -> dict[str, float | str]:
    top = df.groupby("product")["units"].sum().idxmax()
    return {
        "rows": len(df),
        "total_revenue": round(float(df["revenue"].sum()), 2),
        "mean_units": round(float(df["units"].mean()), 2),
        "top_product": str(top),
        "first_row_store": str(df.iloc[0]["store"]),  # position-based access
    }


def main() -> None:
    pd.set_option("display.width", 120)
    df = load_sales()
    print("Day 44 – Coffee sales with pandas\n")
    print(df.head(), "\n")
    print("dtypes:", dict(df.dtypes.astype(str)))
    print("\nRevenue by store:\n", revenue_by_store(df))
    print("\nDays ≥ €150:\n", best_days(df, 150))
    print("\nUnits pivot:\n", monthly_pivot(df))
    print("\nSummary:", summary(df))


if __name__ == "__main__":
    main()
