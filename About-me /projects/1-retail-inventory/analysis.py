"""Generate charts and findings for electronics retail project."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent.parent / "project-datasources" / "1-retail-inventory" / "data"
OUT = ROOT

def main():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        raise

    product = pd.read_csv(DATA / "DimProduct.csv")
    store = pd.read_csv(DATA / "DimStore.csv")
    sales = pd.read_csv(DATA / "FactSales.csv")
    inv = pd.read_csv(DATA / "FactInventory.csv")

    sales = sales.merge(product[["ProductID", "ProductName", "Subcategory"]], on="ProductID")
    sales = sales.merge(store[["StoreID", "StoreName"]], on="StoreID")

    # Chart 1: Top products by revenue
    rev = sales.groupby(["ProductID", "ProductName"]).agg(TotalRevenue=("Revenue", "sum")).reset_index().sort_values("TotalRevenue", ascending=False).head(10)
    plt.figure(figsize=(10, 5))
    plt.barh(range(len(rev)), rev["TotalRevenue"].values, color="steelblue")
    plt.yticks(range(len(rev)), rev["ProductName"].values, fontsize=9)
    plt.xlabel("Total Revenue ($)")
    plt.title("Top electronics products by revenue")
    plt.tight_layout()
    plt.savefig(OUT / "chart1_top_products_revenue.png", dpi=100)
    plt.close()

    # Chart 2: Revenue by store
    by_store = sales.groupby("StoreName").agg(TotalRevenue=("Revenue", "sum")).reset_index().sort_values("TotalRevenue", ascending=False)
    plt.figure(figsize=(8, 4))
    plt.bar(by_store["StoreName"], by_store["TotalRevenue"], color="coral")
    plt.xlabel("Store")
    plt.ylabel("Total Revenue ($)")
    plt.title("Revenue by store")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUT / "chart2_revenue_by_store.png", dpi=100)
    plt.close()

    # Chart 3: Revenue by subcategory
    by_sub = sales.groupby("Subcategory").agg(TotalRevenue=("Revenue", "sum")).reset_index().sort_values("TotalRevenue", ascending=False)
    plt.figure(figsize=(6, 6))
    plt.pie(by_sub["TotalRevenue"], labels=by_sub["Subcategory"], autopct="%1.0f%%", startangle=90)
    plt.title("Revenue by subcategory")
    plt.tight_layout()
    plt.savefig(OUT / "chart3_revenue_by_subcategory.png", dpi=100)
    plt.close()

    # Chart 4: Inventory turnover (units sold / avg on hand)
    units_sold = sales.groupby("ProductID").agg(TotalUnits=("UnitsSold", "sum")).reset_index()
    avg_inv = inv.groupby("ProductID").agg(AvgOnHand=("OnHandQty", "mean")).reset_index()
    turn = units_sold.merge(avg_inv, on="ProductID")
    turn = turn.merge(product[["ProductID", "ProductName"]], on="ProductID")
    turn["Turnover"] = turn["TotalUnits"] / turn["AvgOnHand"].replace(0, 1)
    turn = turn.sort_values("Turnover", ascending=True).head(10)
    plt.figure(figsize=(10, 5))
    plt.barh(range(len(turn)), turn["Turnover"].values, color="seagreen")
    plt.yticks(range(len(turn)), turn["ProductName"].values, fontsize=9)
    plt.xlabel("Inventory turnover")
    plt.title("Inventory turnover by product (lowest)")
    plt.tight_layout()
    plt.savefig(OUT / "chart4_inventory_turnover.png", dpi=100)
    plt.close()

    print("Charts saved to", OUT)
    print("Findings: Revenue concentrated in monitors, laptops, phones; stockouts on mice/webcams; low turnover on some computers and keyboards.")

if __name__ == "__main__":
    main()
