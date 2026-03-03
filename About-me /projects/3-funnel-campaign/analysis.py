"""Generate funnel and campaign charts."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent.parent / "project-datasources" / "3-funnel-campaign" / "data"
OUT = ROOT

def main():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise

    df = pd.read_csv(DATA / "FactFunnel.csv")
    stage_order = ["Lead", "Qualified", "Proposal", "Won"]

    # Chart 1: Funnel by stage
    counts = df.groupby("Stage").agg(LeadID=("LeadID", "nunique")).reindex(stage_order).fillna(0).reset_index()
    plt.figure(figsize=(8, 4))
    plt.bar(counts["Stage"], counts["LeadID"], color=["#6366f1", "#8b5cf6", "#a855f7", "#22c55e"])
    plt.xlabel("Stage")
    plt.ylabel("Count")
    plt.title("Funnel: Lead → Qualified → Proposal → Won")
    plt.tight_layout()
    plt.savefig(OUT / "chart1_funnel.png", dpi=100)
    plt.close()

    # Chart 2: Leads by source
    leads = df[df["Stage"] == "Lead"].groupby("Source").size().reset_index(name="Count")
    plt.figure(figsize=(6, 4))
    plt.bar(leads["Source"], leads["Count"], color="coral")
    plt.xlabel("Source")
    plt.ylabel("Leads")
    plt.title("Leads by source")
    plt.tight_layout()
    plt.savefig(OUT / "chart2_leads_by_source.png", dpi=100)
    plt.close()

    # Chart 3: Won by source
    won = df[df["Stage"] == "Won"].groupby("Source").size().reset_index(name="Count")
    plt.figure(figsize=(6, 4))
    plt.bar(won["Source"], won["Count"], color="seagreen")
    plt.xlabel("Source")
    plt.ylabel("Won deals")
    plt.title("Won deals by source")
    plt.tight_layout()
    plt.savefig(OUT / "chart3_won_by_source.png", dpi=100)
    plt.close()

    print("Charts saved to", OUT)

if __name__ == "__main__":
    main()
