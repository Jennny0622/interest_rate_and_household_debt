from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Interest Rates and Household Debt in Australia",
    page_icon="📊",
    layout="wide",
)


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_data():
    cash = pd.read_csv(DATA_DIR / "cash_rate_quarterly.csv")
    household = pd.read_csv(DATA_DIR / "household_financial_dataset.csv")

    cash["year"] = cash["quarter"].str[:4].astype(int)
    household["year"] = household["Quarter"].str[:4].astype(int)

    return cash, household


cash, household = load_data()


st.title("Interest Rates and Household Debt in Australia")
st.caption("Econometric and balance sheet evidence, 2015–2025")

st.write(
    "This dashboard summarises a university data science project on the "
    "relationship between the Australian cash rate and household finances. "
    "Python was used for data preparation, and R was used for the regression "
    "analysis and the original figures."
)


# Latest values
latest_cash = cash.iloc[-1]
latest_household = household.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    f"Cash rate ({latest_cash['quarter']})",
    f"{latest_cash['cash_rate']:.2f}%",
)
col2.metric(
    f"Debt-to-income ratio ({latest_household['Quarter']})",
    f"{latest_household['Household debt to income']:.1f}%",
)
col3.metric(
    f"Debt-to-assets ratio ({latest_household['Quarter']})",
    f"{latest_household['Household debt to assets']:.1f}%",
)
col4.metric(
    "Baseline coefficient (p = 0.022)",
    "−$5.6bn",
)


st.divider()

st.subheader("Explore the data")

start_year, end_year = st.slider(
    "Select the period",
    min_value=2015,
    max_value=2025,
    value=(2015, 2025),
)

cash_filtered = cash[
    cash["year"].between(start_year, end_year)
].copy()
household_filtered = household[
    household["year"].between(start_year, end_year)
].copy()


cash_chart = px.line(
    cash_filtered,
    x="quarter",
    y="cash_rate",
    markers=True,
    title="Quarterly Cash Rate",
    labels={"quarter": "Quarter", "cash_rate": "Cash rate (%)"},
)
cash_chart.update_traces(line_color="#1f4e79")
cash_chart.update_layout(
    hovermode="x unified",
    title_x=0.02,
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=60, b=20),
)
st.plotly_chart(cash_chart, use_container_width=True)


left, right = st.columns(2)

debt_income_chart = px.line(
    household_filtered,
    x="Quarter",
    y="Household debt to income",
    title="Household Debt-to-Income Ratio",
    labels={
        "Quarter": "Quarter",
        "Household debt to income": "Debt-to-income ratio (%)",
    },
)
debt_income_chart.update_traces(line_color="#222222")
debt_income_chart.update_layout(
    hovermode="x unified",
    title_x=0.02,
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=60, b=20),
)
left.plotly_chart(debt_income_chart, use_container_width=True)


debt_assets_chart = px.line(
    household_filtered,
    x="Quarter",
    y="Household debt to assets",
    title="Household Debt-to-Assets Ratio",
    labels={
        "Quarter": "Quarter",
        "Household debt to assets": "Debt-to-assets ratio (%)",
    },
)
debt_assets_chart.update_traces(line_color="#b04a3a")
debt_assets_chart.update_layout(
    hovermode="x unified",
    title_x=0.02,
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=60, b=20),
)
right.plotly_chart(debt_assets_chart, use_container_width=True)


st.subheader("Regression results")

results = pd.DataFrame(
    {
        "Model": [
            "Baseline",
            "Post-2019",
            "First difference",
            "Excluding COVID-19",
        ],
        "Coefficient ($ million)": [-5607, -6716, 723, -787],
        "p-value": [0.022, 0.013, 0.827, 0.711],
        "Result at 5% level": [
            "Significant",
            "Significant",
            "Not significant",
            "Not significant",
        ],
    }
)

st.dataframe(results, hide_index=True, use_container_width=True)

st.write(
    "The baseline model shows a negative association between the cash rate "
    "and household net lending. However, the result is no longer statistically "
    "significant after the COVID-19 quarters are excluded. The evidence does "
    "not establish that higher interest rates caused household debt to fall."
)


st.subheader("Main interpretation")

st.write(
    "Household debt-to-income and debt-to-assets ratios declined near the end "
    "of the sample. This did not result from a fall in household liabilities. "
    "Liabilities increased by about 20% between 2022Q1 and 2025Q3, while "
    "household income and assets grew faster."
)


with st.expander("Limitations"):
    st.write(
        "The sample is short and includes only one major tightening cycle. "
        "The regression models do not control for other factors such as income, "
        "employment and housing prices. The data also represent the household "
        "sector as a whole and do not show differences between households."
    )


st.divider()

st.markdown(
    "**Project by Jeongyoon Kim**  \n"
    "[View the code and full report on GitHub]"
    "(https://github.com/Jennny0622/interest_rate_and_household_debt)"
)
