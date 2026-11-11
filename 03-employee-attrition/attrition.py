from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Show all columns when printing tables (no "..." in the middle)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def main():
    base_dir = Path(__file__).resolve().parent
    excel_path = base_dir / "WA_Fn-UseC_-HR-Employee-Attrition_1.xlsx"
    df = pd.read_excel(excel_path)

    print(df.shape)
    print(df.head())

    # Q1 : What percentage of employees left?
    total = len(df)
    print("Total Employees:", total)

    left = (df["Attrition"] == "Yes").sum()
    print("Employees who left:", left)
    rate = round(100 * left / total, 2)
    print("Attrition rate:", rate, "%")

    # Q1 chart choice: pie chart because this is a share of two groups (left vs stayed).
    left_share = [left, total - left]
    labels = ["Left", "Stayed"]
    plt.figure(figsize=(6, 6))
    plt.pie(
        left_share,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#d9534f", "#5bc0de"],
    )
    plt.title("Attrition Share")
    plt.tight_layout()
    plt.savefig(base_dir / "q1_attrition_share.png")
    plt.close()

    # Q2 : Which department has the highest attrition?
    df["Left"] = (df["Attrition"] == "Yes").astype(int)

    q2 = df.groupby("Department")["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q2["attrition_rate"] = (q2["attrition_rate"] * 100).round(2)
    q2 = q2.sort_values("attrition_rate", ascending=False)
    print(q2)

    q2["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by Department")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q2_department.png")
    plt.close()

    # Q3 : Do employees who work overtime leave more?
    q3 = df.groupby("OverTime")["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q3["attrition_rate"] = (q3["attrition_rate"] * 100).round(2)
    q3 = q3.sort_values("attrition_rate", ascending=False)
    print(q3)

    q3["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by OverTime")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q3_overtime.png")
    plt.close()

    # Q4. Which age group leaves the most?
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[17, 29, 39, 49, 60],
        labels=["18-29", "30-39", "40-49", "50-60"],
    )
    q4 = df.groupby("AgeGroup", observed=True)["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q4["attrition_rate"] = (q4["attrition_rate"] * 100).round(2)
    print(q4)

    q4["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by Age Group")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q4_age_group.png")
    plt.close()

    # Q5. Does monthly income affect attrition?
    df["IncomeBand"] = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 2999, 5999, 9999, 20000],
        labels=["Below 3K", "3K-6K", "6K-10K", "10K+"],
    )
    q5 = df.groupby("IncomeBand", observed=True)["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q5["attrition_rate"] = (q5["attrition_rate"] * 100).round(2)
    print(q5)

    q5["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by Monthly Income")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q5_income.png")
    plt.close()

    # Q6. Which job role has the highest attrition?
    q6 = df.groupby("JobRole")["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q6["attrition_rate"] = (q6["attrition_rate"] * 100).round(2)
    q6 = q6.sort_values("attrition_rate", ascending=False)
    print(q6)

    q6["attrition_rate"].sort_values().plot(kind="barh", color="steelblue")
    plt.title("Attrition % by Job Role")
    plt.xlabel("Attrition %")
    plt.tight_layout()
    plt.savefig(base_dir / "q6_job_role.png")
    plt.close()

    # Q7. Does job satisfaction affect attrition?
    df["JobSatisfactionLevel"] = df["JobSatisfaction"].map(
        {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}
    )
    q7 = df.groupby("JobSatisfactionLevel")["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q7["attrition_rate"] = (q7["attrition_rate"] * 100).round(2)
    q7 = q7.reindex(["Low", "Medium", "High", "Very High"])
    print(q7)

    q7["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by Job Satisfaction")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q7_job_satisfaction.png")
    plt.close()

    # Q8. Do single employees leave more than married ones?
    q8 = df.groupby("MaritalStatus")["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q8["attrition_rate"] = (q8["attrition_rate"] * 100).round(2)
    q8 = q8.sort_values("attrition_rate", ascending=False)
    print(q8)

    q8["attrition_rate"].plot(kind="bar", color="steelblue")
    plt.title("Attrition % by Marital Status")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q8_marital_status.png")
    plt.close()

    # Q9. Do employees who live far from the office leave more?
    df["DistanceBand"] = pd.cut(
        df["DistanceFromHome"],
        bins=[0, 5, 10, 20, 30],
        labels=["1-5", "6-10", "11-20", "21-29"],
    )
    q9 = df.groupby("DistanceBand", observed=True)["Left"].agg(
        employees="count",
        left_count="sum",
        attrition_rate="mean",
    )
    q9["attrition_rate"] = (q9["attrition_rate"] * 100).round(2)
    print(q9)

    # Q9 chart choice: line chart because distance bands are ordered and show a trend.
    q9["attrition_rate"].plot(kind="line", marker="o", color="darkorange")
    plt.title("Attrition % by Distance From Home")
    plt.xlabel("Distance from home")
    plt.ylabel("Attrition %")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(base_dir / "q9_distance.png")
    plt.close()

    # Q10. Which employees are at high risk right now?
    # Risk score uses only warning signs found in Q3-Q9 (not Attrition itself,
    # because Attrition is what we want to predict).
    risk_df = df.copy()
    risk_df["RiskScore"] = (
        (risk_df["OverTime"] == "Yes").astype(int) * 20
        + (risk_df["JobSatisfaction"] <= 2).astype(int) * 15
        + (risk_df["DistanceFromHome"] > 10).astype(int) * 10
        + (risk_df["Age"] < 35).astype(int) * 10
        + (risk_df["MonthlyIncome"] < 5000).astype(int) * 15
    )

    # Check: does a higher score really mean more people left?
    score_check = risk_df.groupby("RiskScore")["Left"].agg(
        employees="count",
        attrition_rate="mean",
    )
    score_check["attrition_rate"] = (score_check["attrition_rate"] * 100).round(1)
    print("\nAttrition % by Risk Score:")
    print(score_check)

    # Only employees who are still working can be saved
    current = risk_df[risk_df["Attrition"] == "No"]
    high_risk = current.sort_values(
        ["RiskScore", "MonthlyIncome"], ascending=[False, True]
    ).head(10)

    print("\nTop 10 high-risk employees (still working):")
    print(
        high_risk[
            [
                "EmployeeNumber",
                "Age",
                "Department",
                "JobRole",
                "MonthlyIncome",
                "DistanceFromHome",
                "OverTime",
                "JobSatisfaction",
                "RiskScore",
            ]
        ]
    )

    # Chart: attrition % rises as the risk score rises
    score_check["attrition_rate"].plot(kind="line", marker="o", color="crimson")
    plt.title("Attrition % by Risk Score")
    plt.xlabel("Risk Score")
    plt.ylabel("Attrition %")
    plt.tight_layout()
    plt.savefig(base_dir / "q10_risk_score.png")
    plt.close()

    # Save the list for HR
    high_risk.to_csv(base_dir / "high_risk_employees.csv", index=False)


if __name__ == "__main__":
    main()