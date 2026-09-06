from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# 1. Create the baseline dataset
def create_baseline_dataset():
    household = pd.read_csv(
        PROCESSED_DIR / "household_net_borrowing_quarterly.csv"
    )
    cash = pd.read_csv(
        PROCESSED_DIR / "cash_rate_quarterly.csv"
    )

    household["quarter"] = household["quarter"].astype(str)
    cash["quarter"] = cash["quarter"].astype(str)

    df = pd.merge(household, cash, on="quarter", how="inner")
    df = df.sort_values("quarter").reset_index(drop=True)

    df.to_csv(
        PROCESSED_DIR / "baseline_analysis_dataset.csv",
        index=False,
    )
    return df


# 2. Create the lagged cash rate dataset
def create_lagged_dataset(df):
    df_lagged = df.copy()
    df_lagged["cash_rate_lag1"] = df_lagged["cash_rate"].shift(1)
    df_lagged["cash_rate_lag2"] = df_lagged["cash_rate"].shift(2)

    df_lagged = df_lagged.dropna(
        subset=["cash_rate_lag1", "cash_rate_lag2"]
    )

    df_lagged.to_csv(
        PROCESSED_DIR / "lagged_cash_rate_dataset.csv",
        index=False,
    )


# 3. Create the post-2019 dataset
def create_post_2019_dataset(df):
    df_post = df.copy()
    df_post["year"] = df_post["quarter"].str[:4].astype(int)
    df_post = df_post[df_post["year"] >= 2019].copy()

    df_post.to_csv(
        PROCESSED_DIR / "post_2019_dataset.csv",
        index=False,
    )


# 4. Create the first-difference dataset
def create_difference_dataset(df):
    df_diff = df.copy()
    df_diff["diff_net_lending"] = df_diff[
        "net_lending_borrowing"
    ].diff()
    df_diff = df_diff.dropna(subset=["diff_net_lending"])

    df_diff.to_csv(
        PROCESSED_DIR / "first_difference_dataset.csv",
        index=False,
    )


# 5. Create the lagged first-difference dataset
def create_lagged_difference_dataset(df):
    df_lagged_diff = df.copy()
    df_lagged_diff["diff_net_lending"] = df_lagged_diff[
        "net_lending_borrowing"
    ].diff()
    df_lagged_diff["cash_rate_lag1"] = df_lagged_diff[
        "cash_rate"
    ].shift(1)
    df_lagged_diff["cash_rate_lag2"] = df_lagged_diff[
        "cash_rate"
    ].shift(2)

    df_lagged_diff = df_lagged_diff.dropna(
        subset=[
            "diff_net_lending",
            "cash_rate_lag1",
            "cash_rate_lag2",
        ]
    )

    df_lagged_diff.to_csv(
        PROCESSED_DIR / "lagged_difference_dataset.csv",
        index=False,
    )


def main():
    baseline = create_baseline_dataset()
    create_lagged_dataset(baseline)
    create_post_2019_dataset(baseline)
    create_difference_dataset(baseline)
    create_lagged_difference_dataset(baseline)


if __name__ == "__main__":
    main()
