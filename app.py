import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Bank Churn Analytics", layout="wide")
st.title("Bank Customer Churn Analytics")
st.write("Explore how customer activity and product use relate to churn.")

file_path = r"C:\Users\lenovo\Downloads\European_Bank.csv"
data = pd.read_csv(file_path)

st.sidebar.header("Customer filters")
engagement_filter = st.sidebar.selectbox(
    "Engagement status",
    ["All", "Active", "Inactive"]
)

min_products = int(data["NumOfProducts"].min())
max_products = int(data["NumOfProducts"].max())
product_range = st.sidebar.slider(
    "Number of products",
    min_value=min_products,
    max_value=max_products,
    value=(min_products, max_products)
)
min_balance = float(data["Balance"].min())
max_balance = float(data["Balance"].max())

balance_range = st.sidebar.slider(
    "Balance range",
    min_value=min_balance,
    max_value=max_balance,
    value=(min_balance, max_balance),
)
min_salary = float(data["EstimatedSalary"].min())
max_salary = float(data["EstimatedSalary"].max())

salary_range = st.sidebar.slider(
    "Estimated salary range",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary),
)

filtered_data = data.copy()

if engagement_filter == "Active":
    filtered_data = filtered_data[filtered_data["IsActiveMember"] == 1]
elif engagement_filter == "Inactive":
    filtered_data = filtered_data[filtered_data["IsActiveMember"] == 0]

filtered_data = filtered_data[
    filtered_data["NumOfProducts"].between(
        product_range[0], product_range[1]
    )
]
filtered_data = filtered_data[
    filtered_data["Balance"].between(balance_range[0], balance_range[1])
]
filtered_data = filtered_data[
    filtered_data["EstimatedSalary"].between(salary_range[0], salary_range[1])
]

customer_count = len(filtered_data)
col1, col2 = st.columns(2)
col1.metric("Total customers", f"{customer_count:,}")

if customer_count > 0:
    st.subheader("Inactive customers with higher balances")

    high_balance_cutoff = data["Balance"].median()
    at_risk = filtered_data[
        (filtered_data["IsActiveMember"] == 0) &
        (filtered_data["Balance"] >= high_balance_cutoff)
    ]

    risk_count, risk_churn_col = st.columns(2)
    risk_count.metric("Inactive, higher-balance customers", f"{len(at_risk):,}")

    if len(at_risk) > 0:
        risk_churn = at_risk["Exited"].mean() * 100
        risk_churn_col.metric("Churn rate in this group", f"{risk_churn:.2f}%")
        st.dataframe(
            at_risk[["CustomerId", "Geography", "Balance", "NumOfProducts", "Exited"]].head(20)
        )
    else:
        risk_churn_col.metric("Churn rate in this group", "—")
        st.info("No customers in this group match the selected filters.")
    churn_rate = filtered_data["Exited"].mean() * 100
    engagement_summary = (
        filtered_data.groupby("IsActiveMember", as_index=False)["Exited"].mean()
    )
    engagement_summary["Engagement"] = engagement_summary["IsActiveMember"].map(
        {0: "Inactive", 1: "Active"}
    )

    chart = px.bar(
        engagement_summary,
        x="Engagement",
        y="Exited",
        labels={"Engagement": "Activity status", "Exited": "Churn rate"},
        title="Churn rate by engagement status"
    )
    chart.update_yaxes(tickformat=".0%")
    st.plotly_chart(chart, use_container_width=True)
    product_summary = (
        filtered_data.groupby("NumOfProducts", as_index=False)
        .agg(churn_rate=("Exited", "mean"), customers=("Exited", "size"))
    )

    product_chart = px.bar(
        product_summary,
        x="NumOfProducts",
        y="churn_rate",
        hover_data=["customers"],
        labels={
            "NumOfProducts": "Number of products",
            "churn_rate": "Churn rate",
            "customers": "Customer count"
        },
        title="Churn rate by number of products"
    )
    product_chart.update_yaxes(tickformat=".0%")
    st.plotly_chart(product_chart, use_container_width=True)
    col2.metric("Churn rate", f"{churn_rate:.2f}%")
    
    st.subheader("First five customer records")
    st.dataframe(filtered_data.head())
else:
    col2.metric("Churn rate", "—")
    st.info("No customers match these filters.")
st.subheader("Credit card ownership and churn")

card_summary = (
    data.groupby("HasCrCard", as_index=False)
    .agg(churn_rate=("Exited", "mean"), customers=("Exited", "size"))
)
card_summary["Card ownership"] = card_summary["HasCrCard"].map(
    {0: "No card", 1: "Has card"}
)

card_chart = px.bar(
    card_summary,
    x="Card ownership",
    y="churn_rate",
    hover_data=["customers"],
    title="Churn rate by credit card ownership"
)
card_chart.update_yaxes(tickformat=".0%")
st.plotly_chart(card_chart, use_container_width=True)
if len(filtered_data) > 0:
    retention_summary = (
        filtered_data.groupby(
            ["IsActiveMember", "NumOfProducts"],
            as_index=False
        )
        .agg(
            customers=("Exited", "size"),
            retention_strength=(
                "Exited",
                lambda values: (1 - values.mean()) * 100
            )
        )
    )
    retention_summary["Engagement"] = retention_summary[
        "IsActiveMember"
    ].map({0: "Inactive", 1: "Active"})

    st.subheader("Retention strength by engagement and product count")
    retention_chart = px.bar(
        retention_summary,
        x="NumOfProducts",
        y="retention_strength",
        color="Engagement",
        barmode="group",
        hover_data=["customers"],
        labels={
            "NumOfProducts": "Number of products",
            "retention_strength": "Customers retained (%)"
        }
    )
    retention_chart.update_yaxes(range=[0, 100], ticksuffix="%")
    st.plotly_chart(retention_chart, use_container_width=True)

if len(filtered_data) > 0:
    balance_activity = filtered_data.copy()
    median_balance = data["Balance"].median()

    balance_activity["Balance group"] = balance_activity["Balance"].apply(
        lambda value: "At/above median" if value >= median_balance else "Below median"
    )
    balance_activity["Engagement"] = balance_activity["IsActiveMember"].map(
        {0: "Inactive", 1: "Active"}
    )

    balance_summary = (
        balance_activity.groupby(
            ["Balance group", "Engagement"], as_index=False
        )
        .agg(churn_rate=("Exited", "mean"), customers=("Exited", "size"))
    )

    st.subheader("Churn by balance and engagement")
    balance_chart = px.bar(
        balance_summary,
        x="Balance group",
        y="churn_rate",
        color="Engagement",
        barmode="group",
        hover_data=["customers"],
        labels={
            "Balance group": "Balance segment",
            "churn_rate": "Churn rate",
            "customers": "Customer count"
        }
    )
    balance_chart.update_yaxes(tickformat=".0%")
    st.plotly_chart(balance_chart, use_container_width=True)