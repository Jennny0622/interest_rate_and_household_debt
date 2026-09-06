library(readr)
library(dplyr)
library(ggplot2)

# 1. Load processed data
cash <- read_csv(
  "Background/data/processed/cash_rate_quarterly.csv"
)

household <- read_csv(
  "Background/data/processed/household_financial_dataset.csv"
)

# 2. Cash rate trends
cash <- cash %>%
  mutate(quarter = factor(quarter, levels = unique(quarter)))

ggplot(cash, aes(x = quarter, y = cash_rate, group = 1)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Quarterly Cash Rate (2015–2025)",
    x = "Quarter",
    y = "Cash Rate (%)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

ggplot(cash, aes(x = quarter, y = rate_change)) +
  geom_col() +
  geom_hline(yintercept = 0) +
  labs(
    title = "Quarterly Rate Change (2015–2025)",
    x = "Quarter",
    y = "Change in cash rate"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

# 3. Merge household and cash rate data
cash <- cash %>%
  mutate(quarter = as.character(quarter)) %>%
  rename(Quarter = quarter)

df <- household %>%
  left_join(cash, by = "Quarter") %>%
  mutate(Quarter = factor(Quarter, levels = unique(Quarter)))

# 4. Household debt-to-income ratio and cash rate
ggplot(df, aes(x = Quarter)) +
  geom_line(
    aes(
      y = `Household debt to income`,
      colour = "Debt-to-income",
      group = 1
    ),
    linewidth = 1
  ) +
  geom_line(
    aes(
      y = cash_rate * 50,
      colour = "Cash rate",
      group = 1
    ),
    linetype = "dashed",
    linewidth = 1
  ) +
  scale_y_continuous(
    name = "Household debt-to-income ratio",
    sec.axis = sec_axis(~ . / 50, name = "Cash rate (%)")
  ) +
  scale_colour_manual(
    values = c(
      "Debt-to-income" = "black",
      "Cash rate" = "red"
    )
  ) +
  labs(
    title = "Household Debt-to-Income Ratio and Cash Rate Changes in Australia (2015–2025)",
    x = "Quarter",
    colour = ""
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

# 5. Household debt-to-assets ratio and cash rate
ggplot(df, aes(x = Quarter)) +
  geom_line(
    aes(
      y = `Household debt to assets`,
      colour = "Debt-to-assets",
      group = 1
    ),
    linewidth = 1
  ) +
  geom_line(
    aes(
      y = cash_rate * 50,
      colour = "Cash rate",
      group = 1
    ),
    linetype = "dashed",
    linewidth = 1
  ) +
  scale_y_continuous(
    name = "Household debt-to-assets ratio (%)",
    sec.axis = sec_axis(~ . / 50, name = "Cash rate (%)")
  ) +
  scale_colour_manual(
    values = c(
      "Debt-to-assets" = "black",
      "Cash rate" = "red"
    )
  ) +
  labs(
    title = "Household Debt-to-Assets Ratio and Cash Rate Changes in Australia (2015–2025)",
    x = "Quarter",
    colour = ""
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
