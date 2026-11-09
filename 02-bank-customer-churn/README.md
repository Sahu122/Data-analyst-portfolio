# Bank Customer Churn Analysis (Banking) - SQL

Analysis of 10,000 bank customers in MySQL to find out **who is leaving the bank, why, and which customers the bank should try to keep first**.

---

## 1. Business problem

A bank is losing customers. Every customer who leaves also takes their money (balance) with them.
The management wants to know:

- How many customers are leaving?
- Which types of customers leave the most?
- How much money is the bank losing?
- Which current customers are most likely to leave next?

---

## 2. Data

- **Source:** Kaggle - Bank Customer Churn Prediction
- **File:** [`Bank_Customer_Churn_Prediction.csv`](Bank_Customer_Churn_Prediction.csv)
- **Size:** 10,000 rows, 12 columns
- **Missing values:** none

| Column | Meaning |
|---|---|
| customer_id | Unique customer ID |
| credit_score | Customer credit score |
| country | France, Spain or Germany |
| gender | Male or Female |
| age | Customer age |
| tenure | Years with the bank |
| balance | Account balance |
| products_number | Number of bank products the customer has |
| credit_card | 1 = has a credit card |
| active_member | 1 = active, 0 = inactive |
| estimated_salary | Estimated yearly salary |
| churn | **1 = left the bank**, 0 = stayed |

---

## 3. Tools and SQL skills

**Tool:** MySQL Workbench

**Skills used:**
- `GROUP BY` with `COUNT`, `SUM`, `AVG`
- `CASE WHEN` to create groups (age groups, active/inactive, zero balance)
- Conditional aggregation: `SUM(CASE WHEN ... THEN ... ELSE 0 END)`
- CTE (`WITH ... AS`)
- Window function: `RANK() OVER (...)`
- Filtering with `WHERE`, `BETWEEN`, `AND`
- `ORDER BY`, `LIMIT`, `ROUND`

All queries are in [`bank_churn_analysis.sql`](bank_churn_analysis.sql).

---

## 4. Steps

1. Created a database and a `customers` table in MySQL
2. Imported the CSV file with the Table Data Import Wizard
3. Checked the row count (10,000) and missing values (none)
4. Answered 10 business questions with SQL
5. Built a call list of high-risk customers for the retention team

---

## 5. Business questions and results

| # | Question | Result |
|---|---|---|
| Q1 | What percentage of customers left the bank? | **20.37%** (2,037 of 10,000) |
| Q2 | Which country has the highest churn rate? | **Germany 32.4%** vs Spain 16.7% and France 16.2% |
| Q3 | Do male or female customers leave more? | **Female 25.1%** vs Male 16.5% |
| Q4 | Which age group has the highest churn rate? | **Age 50-59: 56.0%**; under 40: only 8-11% |
| Q5 | Are inactive members more likely to leave? | **Inactive 26.9%** vs Active 14.3% |
| Q6 | How does the number of products affect churn? | 2 products: **7.6%**; 3 products: **82.7%**; 4 products: **100%** |
| Q7 | Do customers with zero balance behave differently? | Customers with balance: **24.1%** vs zero balance: 13.8% |
| Q8 | How much balance did the bank lose in each country? | Germany lost **32.6%** of its total balance; overall loss **24%** |
| Q9 | What are the riskiest segments (country + age)? | **Germany, age 50-59: 70%** churn |
| Q10 | Which high-risk customers are still with the bank? | **425 customers** holding **56.5 million** |

---

## 6. Key insights

1. **1 in 5 customers left the bank** (20.4%).
2. **Germany has double the churn** of France and Spain, and lost a third of its customer balance.
3. **Churn jumps sharply after age 40.** In Germany, 7 out of 10 customers aged 50-59 left.
4. **Inactive customers leave almost 2x more** than active customers.
5. **2 products is the sweet spot.** Customers with 3 or 4 products leave almost all the time.
6. **The bank is losing its valuable customers.** Customers with money in their account leave more than zero-balance customers.
7. **425 high-value customers are at risk right now**: inactive, aged 40-60, with more than 100,000 each.

---

## 7. Recommendations

1. **Start a retention programme in Germany**, focused on customers aged 40-60.
2. **Re-engage inactive customers** with offers, reminders and app notifications.
3. **Move 1-product customers to a second product**, and review why customers with 3-4 products are unhappy (for example, high fees or unwanted products).
4. **Give priority service and better rates** to high-balance customers.
5. **Call the 425 high-risk customers first**, starting with the highest balance.

---

## 8. Screenshots
<img width="1070" height="707" alt="image" src="https://github.com/user-attachments/assets/ec97e9d0-7bff-4c73-a85c-7ec519a560e8" />


