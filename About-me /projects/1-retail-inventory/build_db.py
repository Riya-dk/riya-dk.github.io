"""Build SQLite database from project-datasources CSV files."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent.parent / "project-datasources" / "1-retail-inventory" / "data"
DB_PATH = ROOT / "retail.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS FactSales")
    cur.execute("DROP TABLE IF EXISTS FactInventory")
    cur.execute("DROP TABLE IF EXISTS DimProduct")
    cur.execute("DROP TABLE IF EXISTS DimStore")
    cur.execute("DROP TABLE IF EXISTS DimDate")

    cur.execute("""
        CREATE TABLE DimProduct (ProductID INTEGER PRIMARY KEY, ProductName TEXT, Subcategory TEXT, Cost REAL, Price REAL)
    """)
    cur.execute("""
        CREATE TABLE DimStore (StoreID INTEGER PRIMARY KEY, StoreName TEXT, Region TEXT)
    """)
    cur.execute("""
        CREATE TABLE DimDate (DateKey INTEGER PRIMARY KEY, FullDate TEXT, Month INTEGER, Year INTEGER)
    """)
    cur.execute("""
        CREATE TABLE FactSales (ProductID INTEGER, StoreID INTEGER, DateKey INTEGER, UnitsSold INTEGER, Revenue REAL,
            FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
            FOREIGN KEY (StoreID) REFERENCES DimStore(StoreID))
    """)
    cur.execute("""
        CREATE TABLE FactInventory (ProductID INTEGER, StoreID INTEGER, DateKey INTEGER, OnHandQty INTEGER,
            FOREIGN KEY (ProductID) REFERENCES DimProduct(ProductID),
            FOREIGN KEY (StoreID) REFERENCES DimStore(StoreID))
    """)

    with open(DATA / "DimProduct.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        cur.executemany("INSERT INTO DimProduct VALUES (?, ?, ?, ?, ?)",
            [(int(row["ProductID"]), row["ProductName"], row["Subcategory"], float(row["Cost"]), float(row["Price"])) for row in r])

    with open(DATA / "DimStore.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        cur.executemany("INSERT INTO DimStore VALUES (?, ?, ?)",
            [(int(row["StoreID"]), row["StoreName"], row["Region"]) for row in r])

    with open(DATA / "DimDate.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        cur.executemany("INSERT INTO DimDate VALUES (?, ?, ?, ?)",
            [(int(row["DateKey"]), row["FullDate"], int(row["Month"]), int(row["Year"])) for row in r])

    with open(DATA / "FactSales.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        cur.executemany("INSERT INTO FactSales VALUES (?, ?, ?, ?, ?)",
            [(int(row["ProductID"]), int(row["StoreID"]), int(row["DateKey"]), int(row["UnitsSold"]), float(row["Revenue"])) for row in r])

    with open(DATA / "FactInventory.csv", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        cur.executemany("INSERT INTO FactInventory VALUES (?, ?, ?, ?)",
            [(int(row["ProductID"]), int(row["StoreID"]), int(row["DateKey"]), int(row["OnHandQty"])) for row in r])

    conn.commit()
    conn.close()
    print(f"Built {DB_PATH}")

if __name__ == "__main__":
    main()
