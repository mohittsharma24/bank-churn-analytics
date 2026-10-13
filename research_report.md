# Customer Churn Analysis: Engagement, Product Use, and Financial Commitment

## Abstract
This project analyzed customer churn in a dataset of 10,000 bank customers. Overall, 20.37% had left the bank. Churn was higher among inactive customers and among customers with balances at or above the median. Churn also varied substantially by number of products, though the groups with three or four products were small. Credit card ownership showed little difference in churn. These findings describe associations in the dataset; they do not establish causes or predict what any individual customer will do. The results can help guide further investigation and carefully measured retention efforts.
## 1. Introduction
Customer churn means a customer leaves the bank.
Banks study churn to understand which customer behaviors are associated with customers leaving.
This project examines whether customer activity, number of products, and account balance are related to churn among 10,000 bank customers.
## 2. Project Objectives
 -Compare churn rates for active and inactive customers.
-Measure how churn varies by the number of products held.
-Identify inactive customers with higher balances who may warrant retention attention.
## 3. Dataset Description
This project uses European_Bank.csv, which contains 10,000 customer records and 14 columns. The fields include customer demographics, account balance, tenure, number of products, credit card ownership, activity status, and estimated salary. Exited is the churn target: 1 means the customer left, and 0 means the customer stayed. The dataset has no missing values. IsActiveMember is the available proxy for engagement; the data does not include transaction or login history.
## 4. Analytical Methodology
1.Checked the dataset size, columns, missing values, and churn labels.
2.Compared churn rates by activity status, product count, and credit card ownership.
3.Compared churn for customers below and at or above the median account balance.
4.Examined inactive customers at or above the median balance as a higher-balance group for further review.
5.Compared account balance with estimated annual salary using a descriptive balance-to-salary ratio.
6.Built a Streamlit dashboard with engagement, product-count, balance, and salary filters.
## 5. Results and Discussion
The dataset contains 10,000 customers, with no missing values. Overall, 2,037 customers left the bank, giving an overall churn rate of 20.37%.

Churn was 26.85% among inactive customers and 14.27% among active customers. This is a difference of 12.58 percentage points, showing an association between activity status and churn in this dataset.

Churn varied by product count: 27.71% for one product, 7.58% for two products, 82.71% for three products, and 100% for four products. The three-product group contained 266 customers, while the four-product group contained 60. These smaller groups should be interpreted cautiously. The results do not show a simple pattern where more products always correspond to lower churn.

Customers below the median balance had 15.76% churn, compared with 24.98% for those at or above the median. Within the inactive, at-or-above-median-balance group, 2,456 customers had a churn rate of 32.33%. The median is an exploratory threshold, not an official definition of a premium customer.

Credit card ownership had only a small difference in churn: 20.81% among customers without a card and 20.18% among customers with a card. This suggests little difference between these groups in this dataset.

Among the 2,500 customers in the top balance-to-salary-ratio quartile, churn was 24.2%. This ratio is descriptive and should not be treated as a validated measure of financial risk.

These are observed associations in this dataset; they do not establish that any one behavior caused customers to leave.
## 6. Recommendations
-Review inactive customers with balances at or above the median for possible retention outreach. The median is an exploratory segment threshold, so it should be reviewed before being used operationally.
-Explore ways to improve customer engagement, since inactive customers had higher churn in this dataset. Measure the results of any outreach before assuming it improves retention.
-Investigate the three- and four-product customer groups separately. Their churn rates were high, but their group sizes were much smaller than the one- and two-product groups.
-Avoid treating credit card ownership alone as a strong retention lever, because churn differed little between customers with and without a card.
-Use customer-level outreach with additional context and validated criteria; do not treat these group comparisons as predictions about an individual customer.
## 7. Limitations
-The dataset is a snapshot and does not include transaction or login history. IsActiveMember is only a broad proxy for engagement.
-The analysis describes associations and does not establish that a behavior caused a customer to leave.
-The median balance and top-quartile balance-to-salary ratio are exploratory thresholds, not validated measures of customer value or financial risk.
-The three-product and four-product groups are relatively small, especially the four-product group of 60 customers, so their churn rates need cautious interpretation.
-This analysis compares groups one factor at a time in several places; other customer characteristics may also relate to churn.
## 8. Conclusion
In this dataset, churn was associated with customer activity, product count, and account balance. Inactive customers and inactive customers with higher balances had higher churn rates, while credit card ownership showed little difference. Product-count results were not a simple “more products, less churn” pattern, and the smallest product groups require caution. These findings can help focus further retention research, but should be validated with richer activity data and tested interventions before guiding customer-level decisions.