import pandas as pd

file_path = r"C:\Users\lenovo\Downloads\European_Bank.csv"
data = pd.read_csv(file_path)

print(data.head())
print("\nDataset size:", data.shape)
print("\nMissing values:\n", data.isna().sum())
print("\nStayed vs. left:\n", data["Exited"].value_counts())
churn_by_activity = data.groupby("IsActiveMember")["Exited"].mean() * 100
print("\nChurn rate by activity (%):\n", churn_by_activity)
churn_by_products = data.groupby("NumOfProducts")["Exited"].mean() * 100
print("\nChurn rate by number of products (%):\n", churn_by_products)
print("\nCustomer count by number of products:\n",
      data["NumOfProducts"].value_counts().sort_index())
balance_cutoff = data["Balance"].median()
inactive_high_balance = data[
    (data["Balance"] >= balance_cutoff) &
    (data["IsActiveMember"] == 0)
]

print("\nMedian balance:", balance_cutoff)
print("Inactive customers at or above median balance:", len(inactive_high_balance))
print("Their churn rate (%):", inactive_high_balance["Exited"].mean() * 100)
churn_by_balance = data.groupby(
    data["Balance"] >= balance_cutoff
)["Exited"].mean() * 100

print("\nChurn by balance group (%):\n", churn_by_balance)
churn_by_card = data.groupby("HasCrCard")["Exited"].mean() * 100
print("\nChurn by credit card ownership (%):\n", churn_by_card)

print("\nCustomer count by credit card ownership:\n",
      data["HasCrCard"].value_counts().sort_index())
churn_matrix = data.pivot_table(
    values="Exited",
    index="IsActiveMember",
    columns="NumOfProducts",
    aggfunc="mean"
) * 100

print("\nChurn by activity and product count (%):\n",
      churn_matrix.round(1))
churn_by_card = data.groupby("HasCrCard")["Exited"].mean() * 100
print("\nChurn by credit card ownership (%):\n", churn_by_card)

print("\nCustomer count by credit card ownership:\n",
      data["HasCrCard"].value_counts().sort_index())
data["BalanceToSalaryRatio"] = (
    data["Balance"] / data["EstimatedSalary"].replace(0, float("nan"))
)

ratio_cutoff = data["BalanceToSalaryRatio"].quantile(0.75)
high_ratio = data[data["BalanceToSalaryRatio"] >= ratio_cutoff]

print("\n75th percentile of balance-to-salary ratio:", ratio_cutoff)
print("Customers in top ratio quartile:", len(high_ratio))
print("Churn rate in top ratio quartile (%):",
      high_ratio["Exited"].mean() * 100)
print("\nChurn rate by credit card ownership (%):")
print((data.groupby("HasCrCard")["Exited"].mean() * 100).round(2))

print("\nCustomer count by credit card ownership:")
print(data["HasCrCard"].value_counts().sort_index())