# Company Profit & Discount Impact Analysis (Power BI)

An interactive Power BI report that analyses company sales and profit, shows **how much discounts cost the business**, finds **where the company is losing money**, and turns the findings into clear business recommendations.

![Executive Overview](images/01_executive_overview.png)

---

## 📌 Business Problem

The company sells 6 products in 5 countries across 5 customer segments. Management wants to know:

- How is the business performing overall?
- Are discounts hurting profit, and by how much?
- Which segments, products and countries are making a loss?
- What would happen to profit if discounts were reduced?

---

## 📂 Dataset

| Item | Details |
|---|---|
| Source | Microsoft Power BI **Financial Sample** dataset |
| Rows | 700 orders |
| Period | Sep 2013 – Dec 2014 |
| Countries | Canada, France, Germany, Mexico, United States of America |
| Segments | Government, Small Business, Enterprise, Midmarket, Channel Partners |
| Products | Paseo, VTT, Amarilla, Velo, Montana, Carretera |
| Key columns | Units Sold, Sale Price, Gross Sales, Discounts, Sales, COGS, Profit, Discount Band, Date |

**Relationships in the data**
- Gross Sales − Discounts = Sales
- Sales − COGS = Profit

---

## 🛠 Tools Used

- **Power BI Desktop**: Power Query, DAX, Quick measures, What-If parameter
- **Data modelling**: date hierarchy and time intelligence
- **Visuals**: cards, column/bar/line/donut charts, matrix with conditional formatting, Pareto (line + column) chart, slicers, page navigation

---

## 🧹 Data Preparation (Power Query)

- Checked data types (Date as date, money columns as decimal)
- Checked for missing values and duplicates
- Kept "None" as a real Discount Band value (not blank)
- Created a calculated column **Country Product** for the Pareto analysis

---

## ❓ Business Questions

1. What are the company's Total Sales, Total Profit and overall Profit Margin %?
2. How much did Sales and Profit grow in Q4 2014 compared with Q4 2013?
3. How did profit change month-over-month (MoM), and which months had the biggest rise or fall?
4. How much revenue was given away as discounts, and which Discount Band hurt the profit margin most?
5. Which Segment + Product + Country combinations are making a loss, and how much?
6. Do 20% of Country–Product combinations bring 80% of profit (Pareto analysis)?
7. What are the Top 3 most profitable products in each country and segment?
8. If the company reduces discounts by 5% / 10%, how much will profit increase (What-If analysis)?
9. Which segment has high sales but a low margin?
10. What should the company do to increase profit?

---

## 🧮 Key DAX Measures

```DAX
Total Sales = SUM(financials[Sales])
Total Profit = SUM(financials[Profit])
Total Gross Sales = SUM(financials[Gross Sales])
Total Discount = SUM(financials[Discounts])

Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
Discount % = DIVIDE([Total Discount], [Total Gross Sales], 0)

Discount Share % =
DIVIDE([Total Discount], CALCULATE([Total Discount], ALL(financials[Discount Band])), 0)
```

**Pareto analysis**
```DAX
Country Product = financials[Country] & " - " & financials[Product]   -- calculated column

Cumulative Profit % =
VAR CurrentProfit = [Total Profit]
VAR CumProfit =
    CALCULATE(
        [Total Profit],
        FILTER(ALL(financials[Country Product]), [Total Profit] >= CurrentProfit)
    )
VAR AllProfit = CALCULATE([Total Profit], ALL(financials[Country Product]))
RETURN DIVIDE(CumProfit, AllProfit)
```

**What-If analysis** (uses the What-If parameter `Discount Reduction %`, 0–50 in steps of 5)
```DAX
Discount Saved = [Total Discount] * ('Discount Reduction %'[Discount Reduction % Value] / 100)
New Profit = [Total Profit] + [Discount Saved]
Profit Increase % = DIVIDE([Discount Saved], ABS([Total Profit]))
```

**Time intelligence**: `Total Sales YoY%`, `Total Profit YoY%` and `Total Profit MoM%` were created with Quick measures on the date hierarchy.

---

## 📊 Dashboard Pages

| Page | Questions | What it shows |
|---|---|---|
| **1. Executive Overview** | Q1, Q2, Q3 | KPI cards, Q4 2013 vs Q4 2014 comparison, Q4 growth %, monthly profit trend with MoM % tooltip |
| **2. Discount Impact** | Q4, Q8 | Discount share by band, profit margin by band, What-If slider with current vs new profit |
| **3. Loss & Segments** | Q5, Q9 | Loss cards, Segment × Product × Country profit matrix (losses in red), segment performance table |
| **4. Products & Markets** | Q6, Q7 | Pareto chart, Top 3 products with Country and Segment slicers |

| | |
|---|---|
| ![Discount Impact](images/02_discount_impact.png) | ![Loss & Segments](images/03_loss_and_segments.png) |
| ![Products & Markets](images/04_products_and_markets.png) | |

---

## 💡 Key Insights

**Overall performance**
- The company earned **$16.89M profit** on **$118.73M sales**, a **14.23% profit margin**.
- In **Q4 2014 vs Q4 2013**, sales grew **35.69%** and profit grew **41.65%**, so profit grew faster than sales.
- Profit is **seasonal**: October and December are peak months, and November drops in both years (Nov 2014: −66% MoM, Dec 2014: +235% MoM).

**Discounts**
- Discounts cost **$9.21M**, which is **7.20%** of gross sales.
- The **High** discount band takes **57.76%** of all discounts but gives only a **9.07%** margin, compared with **21.86%** for orders with no discount. The higher the discount, the lower the margin.

**Losses**
- All **58 loss-making orders (−$777K)** come from the **Enterprise** segment. Enterprise's total profit is **−$614.5K**.
- **Root cause:** the Enterprise sale price is **125** and the cost is **120**, a margin of only **4%**, so any Medium or High discount turns an order into a loss.

**Segments**
- **Small Business** has the 2nd highest sales (**$42.43M**) but only a **9.77%** margin.
- **Channel Partners** has the lowest sales (**$1.80M**) but the best margin (**73.13%**).

**Products & markets**
- The **80/20 rule does not apply**: 20 of 30 country–product combinations (67%) make 80% of profit, so profit is well diversified.
- **Paseo** is the most profitable product (**$4.80M**) and the top product in 4 of 5 countries. In **Germany** the top product is **Velo**.

**What-If**
- Reducing discounts by **10%** adds about **$0.92M** profit (**+5.45%**).
- For Enterprise, a discount reduction of about **42%** brings the segment to **break-even**.

---

## ✅ Recommendations

1. **Fix Enterprise pricing and discounts (highest priority).** Stop Medium/High discounts for Enterprise or raise the price. A ~42% discount reduction would bring the segment to break-even.
2. **Limit the High discount band.** It takes most of the discount budget but gives the lowest margin. A 10% overall discount cut alone adds about $0.92M profit.
3. **Improve the Small Business margin.** Review pricing and discounts. A small margin gain on $42.43M of sales would add significant profit.
4. **Grow high-margin areas.** Expand Channel Partners (73% margin) and focus on Paseo, and on Velo in Germany.
5. **Plan for seasonality.** Prepare inventory and promotions for the Oct–Dec period, and use targeted offers for the November dip.

---

## ⚠️ Limitations

- 2013 has data for only 4 months (Sep–Dec), so years were compared **quarter-to-quarter (Q4 vs Q4)** rather than full year vs full year.
- The What-If analysis assumes **units sold stay the same** after a discount cut, so it is a best-case estimate.
- The dataset is a sample dataset with fixed prices per segment. Real data may show more variation.

---

## 🚀 How to Use

1. Download `Financial_Sample.pbix` from this folder.
2. Open it in **Power BI Desktop**.
3. Use the page buttons at the top to move between pages (in Power BI Desktop, use **Ctrl + Click**).
4. Use the slicers (Segment, Country) and the What-If slider to explore the data.

---

## 👤 Author

**Pratap Kumar Sahu**
GitHub: [Sahu122](https://github.com/Sahu122)
