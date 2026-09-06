# 1. Baseline model
baseline_data <- read.csv(
  "data/processed/baseline_analysis_dataset.csv"
)

baseline_model <- lm(
  net_lending_borrowing ~ cash_rate,
  data = baseline_data
)

summary(baseline_model)
confint(baseline_model)


# 2. Lagged cash rate model
lagged_data <- read.csv(
  "data/processed/lagged_cash_rate_dataset.csv"
)

current_rate_model <- lm(
  net_lending_borrowing ~ cash_rate,
  data = lagged_data
)

lagged_rate_model <- lm(
  net_lending_borrowing ~ cash_rate + cash_rate_lag1 + cash_rate_lag2,
  data = lagged_data
)

summary(lagged_rate_model)
anova(current_rate_model, lagged_rate_model)


# 3. Post-2019 model
post_2019_data <- read.csv(
  "data/processed/post_2019_dataset.csv"
)

post_2019_model <- lm(
  net_lending_borrowing ~ cash_rate,
  data = post_2019_data
)

summary(baseline_model)
summary(post_2019_model)


# 4. First-difference model
difference_data <- read.csv(
  "data/processed/first_difference_dataset.csv"
)

difference_model <- lm(
  diff_net_lending ~ cash_rate,
  data = difference_data
)

summary(difference_model)


# 5. Lagged first-difference models
lagged_difference_data <- read.csv(
  "data/processed/lagged_difference_dataset.csv"
)

lag1_difference_model <- lm(
  diff_net_lending ~ cash_rate_lag1,
  data = lagged_difference_data
)

lag2_difference_model <- lm(
  diff_net_lending ~ cash_rate_lag2,
  data = lagged_difference_data
)

summary(lag1_difference_model)
summary(lag2_difference_model)
