# Medical Insurance Cost & Risk Analysis (Python + Power BI)

An end-to-end analysis of medical insurance charges. The data is cleaned and analysed in **Python**, then turned into an interactive **Power BI** report that shows **what drives insurance cost** and **which customers are high risk**.

![Overview](images/01_overview.png)

---

## 📌 Business Problem

An insurance company wants to understand why some customers cost much more than others. Management wants to know:

- What is the average cost per customer, and who costs the most?
- How much do smoking, age, BMI, region and gender affect charges?
- Which group of customers is high risk, and how much of the total cost do they take?
- What should the company do to manage this risk?

---

## 📂 Dataset

- **Source:** Medical Cost Personal Dataset (Kaggle)
- **Size:** 1,338 rows, 7 columns (1,337 rows after removing 1 duplicate)
- **Each row = one policyholder**

| Column | Description |
|---|---|
| `age` | Age of the policyholder (18–64) |
| `sex` | Gender (male / female) |
| `bmi` | Body Mass Index |
| `children` | Number of children covered by the policy |
| `smoker` | Smoker or not (yes / no) |
| `region` | Region in the US (northeast, northwest, southeast, southwest) |
| `charges` | Yearly medical insurance cost billed to the customer |

---

## 🛠 Tools Used

| Tool | Used for |
|---|---|
| **Python** (pandas, numpy) | Data checking, cleaning, feature engineering, analysis |
| **Power BI** | DAX measures, interactive 2-page report |
| **VS Code** | Writing and running the Python script |

---

## 📁 Project Structure

```
05-medical-insurance-cost/
├── analysis.py                    # Python cleaning + analysis script
├── insurance.xlsx                 # Raw data
├── insurance_clean.xlsx           # Cleaned data (used in Power BI)
├── medical-insurance-cost.pbix    # Power BI report
├── images/
│   ├── 01_overview.png
│   └── 02_risk_analysis.png
└── README.md
```

---

## 🐍 Part 1: Python (Cleaning & Analysis)

### Step 1: Data check
- Loaded the data with pandas and checked `shape`, `info()`, `describe()`
- Checked missing values with `isnull().sum()` → **no missing values**
- Checked duplicates with `duplicated().sum()` → **1 duplicate row**

### Step 2: Data cleaning
- Removed the duplicate row with `drop_duplicates()` → **1,337 rows**

### Step 3: Feature engineering (4 new columns)

| New column | How it was created | Values |
|---|---|---|
| `age_group` | `pd.cut()` on `age` | 18-25, 26-35, 36-45, 46-55, 56-64 |
| `bmi_category` | `pd.cut()` on `bmi` | Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (30+) |
| `has_children` | `np.where(children > 0)` | Yes / No |
| `smoker_flag` | `np.where(smoker == 'yes')` | 1 / 0 |

```python
df['age_group'] = pd.cut(df['age'], bins=[17, 25, 35, 45, 55, 64],
                         labels=['18-25', '26-35', '36-45', '46-55', '56-64'])

df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100],
                            labels=['Underweight', 'Normal', 'Overweight', 'Obese'], right=False)

df['has_children'] = np.where(df['children'] > 0, 'Yes', 'No')
df['smoker_flag'] = np.where(df['smoker'] == 'yes', 1, 0)
```

### Step 4: Analysis with `groupby`

| # | Question | Result |
|---|---|---|
| 1 | Smoker vs non-smoker average charges | $32,050 vs $8,441 |
| 2 | Average charges by age group | $9,111 (18-25) → $18,796 (56-64) |
| 3 | Average charges by BMI category | $8,852 (Underweight) → $15,572 (Obese) |
| 4 | Average charges by region | Southeast highest ($14,735), Southwest lowest ($12,347) |
| 5 | Male vs female average charges | $13,975 vs $12,570 |
| 6 | Smoker + BMI category | Smoker + Obese = $41,558 |
| 7 | Correlation with charges | smoker 0.79, age 0.30, bmi 0.20, children 0.07 |

### Step 5: Export
- Saved the cleaned data as `insurance_clean.xlsx` for Power BI

---

## 📊 Part 2: Power BI Report

### DAX measures

```DAX
Total Customers = COUNTROWS('Data')

Smoker % = DIVIDE(SUM('Data'[smoker_flag]), [Total Customers])

High Risk Customers =
CALCULATE(
    [Total Customers],
    'Data'[smoker] = "yes",
    'Data'[bmi_category] = "Obese"
)

High Risk % = DIVIDE([High Risk Customers], [Total Customers])

High Risk Charges % =
DIVIDE(
    CALCULATE(SUM('Data'[charges]), 'Data'[smoker] = "yes", 'Data'[bmi_category] = "Obese"),
    SUM('Data'[charges])
)

Overall Avg = CALCULATE(AVERAGE('Data'[charges]), ALL('Data'))

Diff vs Overall % =
DIVIDE(AVERAGE('Data'[charges]) - [Overall Avg], [Overall Avg])
```

**Calculated column** (used to sort BMI categories in the correct order instead of A–Z):

```DAX
BMI Order =
SWITCH(
    TRUE(),
    'Data'[bmi] < 18.5, 1,
    'Data'[bmi] < 25, 2,
    'Data'[bmi] < 30, 3,
    4
)
```

### Report pages

| Page | What it shows |
|---|---|
| **1. Overview** | KPI cards (Total Customers, Total Charges, Avg Charges, Smoker %), average charges by smoker, age group, BMI category and region, share of total charges by smoker, slicers for Region, Smoker and Gender |
| **2. Risk Analysis** | High-risk KPI cards, average charges by age group and smoker, BMI category × smoker chart and matrix with conditional formatting, each age group vs the overall average (%) |

![Risk Analysis](images/02_risk_analysis.png)

---

## ❓ Business Questions Solved

| # | Question | Answer |
|---|---|---|
| 1 | How many customers are there and what is the total cost? | 1,337 customers, $17.75M total charges |
| 2 | What is the average charge per customer? | $13,279 |
| 3 | What % of customers are smokers? | 20.5% (274 smokers, 1,063 non-smokers) |
| 4 | How much more do smokers cost? | $32,050 vs $8,441 → **3.8x** |
| 5 | Which region has the highest charges? | Southeast ($14,735 average, 364 customers) |
| 6 | Is there a difference between male and female? | Male $13,975 vs female $12,570. Males have more smokers (23.6% vs 17.4%) |
| 7 | Smokers are 20% of customers. What is their share of total charges? | **49.5%** |
| 8 | How big is the high-risk group (Smoker + Obese)? | 145 customers (10.8%) who take **33.9%** of total charges |
| 9 | Is a young smoker more expensive than an old non-smoker? | Yes. Age 18-25 smoker: $27,934 vs age 56-64 non-smoker: $14,088 (2x) |
| 10 | Why is Southeast the most expensive region? | Highest smoker share (25%) and highest average BMI (33.4) |
| 11 | How far is each age group from the overall average? | 18-25: −31.4%, 26-35: −21.0%, 36-45: +1.6%, 46-55: +20.4%, 56-64: +41.5% |

---

## 💡 Key Insights

**Smoking is the biggest cost driver**
- Smokers cost **3.8x** more than non-smokers ($32,050 vs $8,441).
- Smokers are only **20.5%** of customers but account for **49.5%** of total charges.
- Smoking has the strongest correlation with charges (**0.79**), far above age (0.30) and BMI (0.20).

**Smoker + Obese is the high-risk group**
- Only **145 customers (10.8%)** are both smokers and obese, but they take **33.9%** of total charges.
- Their average cost is **$41,558**, which is 4.7x a non-smoking obese customer ($8,856).
- Obesity alone adds little: among non-smokers, Obese costs only 15% more than Normal BMI. The risk comes from the **combination**.

**Age and region**
- Charges rise steadily with age: from $9,111 (18-25) to $18,796 (56-64).
- Smoking outweighs age: the youngest smokers cost 2x the oldest non-smokers.
- Southeast is the most expensive region because it has the most smokers and the highest average BMI.

---

## ✅ Recommendations

1. **Create a separate risk tier for Smoker + Obese customers.** They are 10.8% of customers but 33.9% of cost, so their premium should reflect this risk.
2. **Offer smoking-cessation programs and discounts for quitting.** Smoking is the largest cost driver (3.8x), so even a small drop in smokers reduces claims significantly.
3. **Run wellness programs in the Southeast region first.** It has the highest smoker share (25%) and the highest average BMI.

---

## 🧩 Challenges Faced

- **BMI categories were sorted A–Z in Power BI** (Normal, Obese, Overweight, Underweight). Sorting `bmi_category` by a column built from itself gave a **circular dependency error**. I fixed it by building the `BMI Order` column from the numeric `bmi` column instead.
- **Chart order changed when slicers were applied** because the chart was sorted by value. Sorting by the category column with `BMI Order` keeps the order fixed for every filter.
- **Smoker is a text column**, so it did not appear in the correlation. I created `smoker_flag` (1/0) in Python to measure it.

---

## ▶️ How to Run

1. Install the libraries: `pip install pandas numpy openpyxl`
2. Run `python analysis.py` to create `insurance_clean.xlsx`
3. Open `medical-insurance-cost.pbix` in Power BI Desktop

---

## 👤 Author

**Pratap Kumar Sahu**
GitHub: [Sahu122](https://github.com/Sahu122)
