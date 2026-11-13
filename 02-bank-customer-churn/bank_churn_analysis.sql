-- Bank Customer Churn Analysis (MySQL)
-- 10 business questions on 10,000 bank customers

USE bank_churn;

-- Preview the data
SELECT * FROM `bank customer churn prediction` LIMIT 10;

-- Q1: What percentage of customers left the bank?
select
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`;


-- Q2: Which country has the highest churn rate?
select Country,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by country
order by Churn_Customer_rate desc;

-- Q3: Do male or female customers leave more?
select gender,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by gender
order by Churn_Customer_rate desc;

-- Q4: Which age group has the highest churn rate?
Select
case
when age < 30 THEN '18-29'
when age < 40 THEN '30-39'
when age < 50 THEN '40-49'
when age < 60 THEN '50-59'
Else '60+'
END As Group_Age,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by Group_Age
order by Group_Age desc;

-- Q5: Are inactive members more likely to leave?
select
Case when active_member = 1 THEN 'Active' else 'Inactive'
END As Active_Number,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by Active_Number
order by Active_Number desc;

-- Q6: How does the number of products affect churn?
select products_number,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by products_number
order by products_number;

-- Q7: Do customers with zero balance behave differently?
select
case when balance = 0 THEN 'Zero Balance' ELSE 'Remaining Balance' END As Account_type,
count(*) As Total_customers,
sum(churn) As Churn_customers,
round(100 * Avg(churn),2) As Churn_Customer_rate from `bank customer churn prediction`
group by Account_type
order by Account_type;

-- Q8: How much balance did the bank lose from churned customers in each country?
SELECT  country,
    ROUND(SUM(balance), 0)                                      AS total_balance,
    ROUND(SUM(CASE WHEN churn = 1 THEN balance ELSE 0 END), 0)  AS lost_balance,
    ROUND(100.0 * SUM(CASE WHEN churn = 1 THEN balance ELSE 0 END)
          / SUM(balance), 2)                                    AS lost_balance_pct
FROM `bank customer churn prediction`
GROUP BY country
ORDER BY lost_balance DESC;

-- Q9: What are the top 10 riskiest segments by country and age group?
WITH segment AS (
    SELECT
        country,
        CASE
            WHEN age < 30 THEN '18-29'
            WHEN age < 40 THEN '30-39'
            WHEN age < 50 THEN '40-49'
            WHEN age < 60 THEN '50-59'
            ELSE '60+'
        END                           AS age_group,
        COUNT(*)                      AS customers,
        ROUND(100.0 * AVG(churn), 2)  AS churn_rate_pct
    FROM `bank customer churn prediction`
    GROUP BY country, age_group
)
SELECT
    country,
    age_group,
    customers,
    churn_rate_pct,
    RANK() OVER (ORDER BY churn_rate_pct DESC) AS risk_rank
FROM segment
WHERE customers >= 50
ORDER BY risk_rank
LIMIT 10;

-- Q10: Which high-risk customers are still with the bank?
select
customer_id,country,gender,age,balance,products_number from `bank customer churn prediction`
where churn = 0
AND active_member = 0
AND age between 40 and 60
AND balance > 100000
order by balance desc
limit 20;
