"""Generate SaaS financial charts."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent.parent / "project-datasources" / "2-saas-financial" / "data"
OUT = ROOT

def main():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise

    sub = pd.read_csv(DATA / "FactSubscriptions.csv")
    plan = pd.read_csv(DATA / "DimPlan.csv")
    costs = pd.read_csv(DATA / "FactCosts.csv")

    sub = sub.merge(plan[["PlanID", "PlanName"]], on="PlanID")

    # Chart 1: MRR by plan
    by_plan = sub.groupby("PlanName").agg(MRR=("MRR", "sum")).reset_index()
    plt.figure(figsize=(6, 4))
    plt.bar(by_plan["PlanName"], by_plan["MRR"], color=["#22c55e", "#3b82f6", "#8b5cf6"])
    plt.xlabel("Plan")
    plt.ylabel("MRR ($)")
    plt.title("MRR by plan")
    plt.tight_layout()
    plt.savefig(OUT / "chart1_mrr_by_plan.png", dpi=100)
    plt.close()

    # Chart 2: MRR by segment
    by_seg = sub.groupby("Segment").agg(MRR=("MRR", "sum")).reset_index()
    plt.figure(figsize=(6, 4))
    plt.bar(by_seg["Segment"], by_seg["MRR"], color="teal")
    plt.xlabel("Segment")
    plt.ylabel("MRR ($)")
    plt.title("MRR by segment")
    plt.tight_layout()
    plt.savefig(OUT / "chart2_mrr_by_segment.png", dpi=100)
    plt.close()

    # Chart 3: Costs by category (latest month)
    latest = costs[costs["Month"] == 202503].groupby("Category").agg(Amount=("Amount", "sum")).reset_index()
    plt.figure(figsize=(6, 4))
    plt.pie(latest["Amount"], labels=latest["Category"], autopct="%1.0f%%", startangle=90)
    plt.title("Costs by category")
    plt.tight_layout()
    plt.savefig(OUT / "chart3_costs_by_category.png", dpi=100)
    plt.close()

    print("Charts saved to", OUT)

if __name__ == "__main__":
    main()
