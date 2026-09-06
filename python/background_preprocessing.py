"""
background_preprocessing.py

Preprocesses the background datasets used in the Interest Rate and Household Debt project.
"""

from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Cash rate preprocessing
def preprocess_cash_rate():
    """Create a quarterly cash-rate dataset for 2015Q1–2025Q4."""

    input_path = RAW_DATA_DIR / "cash_rate.xlsx"
    output_path = PROCESSED_DATA_DIR / "cash_rate_quarterly.csv"

    df = pd.read_excel(
        input_path,
        skiprows=11,
        header=None
    )

    df = df.iloc[:, :2].copy()
    df.columns = ["date", "cash_rate"]

    df["cash_rate"] = df["cash_rate"].ffill()

    df["quarter"] = df["date"].dt.to_period("Q")

    quarterly = (
        df.groupby("quarter", as_index=False)["cash_rate"]
        .mean()
    )

    quarterly = quarterly.loc[
        (quarterly["quarter"] >= "2015Q1")
        & (quarterly["quarter"] <= "2025Q4")
    ].copy()

    quarterly["rate_change"] = quarterly["cash_rate"].diff()

    quarterly["quarter"] = quarterly["quarter"].astype(str)

    quarterly.to_csv(output_path, index=False)

    return quarterly


# 2. Household balance-sheet preprocessing
def preprocess_household_balance_sheet():
    """Clean household balance-sheet data and convert dates to quarters."""
    input_path = RAW_DATA_DIR / "household_business_balance_sheet.xlsx"
    output_path = PROCESSED_DATA_DIR / "household_balance_sheet.csv"

    df = pd.read_excel(
        input_path,
        sheet_name="Data",
        header=1
    )

    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df[df["Date"].notna()].reset_index(drop=True)

    df = df[
        [
            "Date",
            "Household total liabilities",
            "Household net worth",
            "Household dwellings",
        ]
    ].copy()

    df["Date"] = df["Date"].dt.to_period("Q").astype(str)
    df.rename(columns={"Date": "Quarter"}, inplace=True)

    df.to_csv(output_path, index=False)

    return df

# 3. Household financial-ratio preprocessing
def preprocess_household_financial_ratios():
    """Clean household financial-ratio data and convert dates to quarters."""

    input_path = RAW_DATA_DIR / "household_finances.xlsx"
    output_path = PROCESSED_DATA_DIR / "household_financial_ratios.csv"

    df = pd.read_excel(
        input_path,
        sheet_name="Data",
        header=1
    )

    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.iloc[9:].reset_index(drop=True)

    df = df[
        [
            "Date",
            "Household debt to income",
            "Household debt to assets",
            "Household financial assets to income",
        ]
    ].copy()

    df["Date"] = df["Date"].dt.to_period("Q").astype(str)
    df.rename(columns={"Date": "Quarter"}, inplace=True)

    df.to_csv(output_path, index=False)

    return df



# 4. Merge household datasets
def merge_household_data(balance_sheet, financial_ratios):
    """Merge the two cleaned household datasets by quarter."""

    output_path = PROCESSED_DATA_DIR / "household_financial_dataset.csv"

    merged = pd.merge(
        balance_sheet,
        financial_ratios,
        on="Quarter",
        how="left"
    )
    
    # Remove rows with missing household data
    merged = merged.dropna()

    merged.to_csv(output_path, index=False)

    return merged


def main():
    preprocess_cash_rate()

    balance_sheet = preprocess_household_balance_sheet()
    financial_ratios = preprocess_household_financial_ratios()

    merge_household_data(
        balance_sheet,
        financial_ratios
    )

    print("Background preprocessing completed successfully.")
    print(f"Processed files saved to: {PROCESSED_DATA_DIR}")


if __name__ == "__main__":
    main()
