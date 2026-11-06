# Inventory & Demand Forecasting (Supply Chain) - Excel
  # StockPilot: Inventory & Demand Forecasting (Supply Chain) - Excel

StockPilot is an Excel planning tool for an online seller that stores products in Amazon warehouses (FBA). It answers four daily questions:

- **What** should we restock?
- **How much** should we send?
- **Where** (which state and warehouse) should we send it?
- **What** should we stop sending because it is overstocked?

> Product names, ASINs and SKUs in this file are masked (demo data).

---

## 1. Business problem

The seller manages **1,037 products** and faces two costly problems at the same time:

| Problem | Impact |
|---|---|
| **Stock-outs** - popular products run out | Lost sales and lower search ranking |
| **Overstock** - slow products pile up in the warehouse | Money stuck in stock and monthly storage fees |

Before this tool, these decisions were made manually product by product. StockPilot brings all the data into one file and gives a clear action for every product.

---

## 2. Data used (12 input sheets)

| Sheet | What it contains |
|---|---|
| 30_Day_Sale | Units sold and traffic per SKU in the last 30 days |
| 07_Day_Sale | Units sold and traffic per SKU in the last 7 days |
| Inventory Ledger | Live warehouse stock per product and location (5,300+ rows) |
| in Transit | Stock already on the way to the warehouse |
| Upcoming | Stock planned for future shipments |
| ABC Warehouse | Stock available in our own warehouse |
| State Level Traffic | Customer page views per product per state (26,000+ rows) |
| FC Mapping | Amazon warehouses (FCs) in each state |
| Storage Fees Cost | Storage fee per unit |
| Block Asins | 146 SKUs blocked from restock |
| Rules | All limits and weights in one place |

---

## 3. Problems solved

### 3.1 Daily demand
The tool calculates the average daily sale for every product:

> **Daily sale = last 7 days sale ÷ 7**

The last 7 days are used instead of 30 because they show the most recent demand trend.

### 3.2 Days of coverage
It shows how many days the current stock will last:

> **Days of coverage = live stock ÷ daily sale**

### 3.3 Total pipeline stock
It adds all stock that is available or on the way:

> **Pipeline stock = live stock + in transit + upcoming**

### 3.4 Restock quantity ("To send")
It calculates how many units are needed to reach **30 days of cover**, after removing the stock already in transit:

> **To send = (30 − days of coverage) × daily sale − in transit**
>
> If the result is negative, the tool shows 0 (no restock needed).

### 3.5 Stock-out alerts (3 rules)

| Alert | Rule | Meaning |
|---|---|---|
| **Zero Stock** | Sells 10+ units a month, but no stock live, in transit or upcoming | Sales are being lost right now - order immediately |
| **Critical** | Less than 5 days of live stock | Will run out within days |
| **At Risk** | Less than 25 days of cover, even after counting the pipeline | Needs to be in the next shipment |

### 3.6 Overstock detection (3 rules)
A product is checked only if it has **at least 10 units live**. It is marked as overstock if **any one** of these is true:

| Rule | Condition |
|---|---|
| A - High coverage | 25 or more days of cover |
| B - Dead stock | No sales in the last 7 days and 31+ days of cover |
| C - Excess stock | Stock is more than 1.5× the monthly sale |

### 3.7 Suggested action for each overstock product

| Situation | Action |
|---|---|
| No sales in 7 days | Stop restock, consider clearance or promotion |
| Stock 3× or more of monthly sale | Reduce the next restock significantly or run a promotion |
| Stock 1.5× or more of monthly sale | Slow down the next shipment and monitor demand |
| Moderate excess | Monitor and review in the next cycle |

### 3.8 Storage cost estimate
For every overstocked product, the tool estimates the **monthly storage cost** and the **total storage cost until the stock is sold**.

### 3.9 State-wise stock allocation
When a new shipment is ready, the tool decides how to split it across states. Each state gets a priority score:

> **Priority score = 60% × customer traffic share + 40% × stock shortage**

- States with the highest scores get stock first.
- Each state gets a minimum of **20** and a maximum of **5,000** units.
- States that already have enough stock are skipped.
- The tool also picks the right Amazon warehouse (FC) in each state.

### 3.10 One Rules sheet for all settings
All limits (30 days target, 25 days risk level, 60/40 weights, min/max quantity) are stored in one **Rules** sheet. A manager can change any number there without touching a formula.

---

## 4. Excel skills used

- **Lookup:** XLOOKUP, VLOOKUP, INDEX-MATCH
- **Aggregation:** SUMIF, SUMIFS, COUNTIFS
- **Logic:** IF, AND, OR, IFERROR
- **Ranking:** LARGE, MATCH-based ordering
- **Structure:** Excel Tables (structured references), named ranges, array formulas
- **Presentation:** conditional formatting for alerts

---

## 5. Key insights (from one planning run)

1. **1,037 SKUs** sold **89,344 units in 30 days**, about **3,040 units per day** based on the last 7 days.
2. **85 SKUs** were completely out of stock while still selling 10+ units a month, which means sales were being lost.
3. **145 SKUs** were **Critical** (less than 5 days of stock) and **223** were **At Risk**.
4. Only **584 of 1,037 SKUs (56%)** were in a healthy stock position.
5. At the same time, **252 SKUs** were overstocked, and **8** were dead stock with no sales in 7 days.
6. **534 SKUs** needed restocking, about **35,600 units** in total.
7. **Maharashtra (16%)**, **Karnataka (10%)** and **Tamil Nadu (10%)** had the highest customer traffic, so they receive stock first.

---

## 6. Recommendations

1. Send the **85 Zero Stock** SKUs first, then the **Critical** ones.
2. **Stop restock** for the 8 dead-stock SKUs and clear them with a promotion.
3. **Reduce or slow down** the next shipment for the 252 overstocked SKUs to cut storage fees.
4. Send stock to **high-traffic states first** for faster delivery and more sales.
5. Run StockPilot **every week** to keep stock between 25 and 30 days of cover.

---

## 7. Frequently asked questions

**1. What problem does this project solve?**
It tells the seller which products to restock, how much to send, where to send it, and which products are overstocked. This prevents both lost sales and extra storage fees.

**2. How is daily demand calculated?**
Last 7 days sale ÷ 7. Seven days are used because they reflect the latest trend better than 30 days.

**3. What is "days of coverage"?**
Live stock ÷ daily sale. It shows how many days the current stock will last.

**4. How is the restock quantity calculated?**
(30 − current days of cover) × daily sale − stock already in transit. If the result is negative, it is set to 0.

**5. What are the three stock-out rules?**
Zero Stock (sells 10+ a month but no stock anywhere), Critical (less than 5 days of live stock) and At Risk (less than 25 days of cover including the pipeline).

**6. How is overstock identified?**
The product must have at least 10 units live, plus one of these: 25+ days of cover, no sales in 7 days with 31+ days of cover, or stock above 1.5× the monthly sale.

**7. What were the main findings?**
Out of 1,037 SKUs, 85 were out of stock while still selling, 145 were critical and 223 were at risk. At the same time, 252 were overstocked. Only 56% of products were healthy.

**8. How does the tool decide which state gets stock?**
Each state gets a score: 60% weight for its share of customer traffic and 40% for how short its stock is. The highest scores get stock first, with a minimum of 20 and a maximum of 5,000 units per state.

**9. Which Excel functions were used?**
XLOOKUP, VLOOKUP, INDEX-MATCH, SUMIFS, COUNTIFS, IF/AND/OR, IFERROR, LARGE, Excel Tables and named ranges.

**10. Why is there a separate Rules sheet?**
All limits and weights are kept in one place, so a manager can change a number without editing any formula.

