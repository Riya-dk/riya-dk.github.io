-- 1. Which electronics products drive most revenue?
SELECT
  p.ProductName,
  p.Subcategory,
  SUM(s.Revenue) AS TotalRevenue,
  SUM(s.UnitsSold) AS TotalUnits
FROM FactSales s
JOIN DimProduct p ON s.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName, p.Subcategory
ORDER BY TotalRevenue DESC
LIMIT 10;

-- 2. Where are we experiencing stockouts?
SELECT st.StoreName, st.Region, p.ProductName, p.Subcategory, i.OnHandQty, i.DateKey
FROM FactInventory i
JOIN DimStore st ON i.StoreID = st.StoreID
JOIN DimProduct p ON i.ProductID = p.ProductID
WHERE i.OnHandQty = 0
ORDER BY st.StoreName, p.ProductName;

-- 3. Which products are potential overstock (low turnover)?
WITH sales_by_product AS (
  SELECT ProductID, SUM(UnitsSold) AS TotalUnitsSold FROM FactSales GROUP BY ProductID
),
inv_by_product AS (
  SELECT ProductID, AVG(OnHandQty) AS AvgOnHand FROM FactInventory GROUP BY ProductID
)
SELECT p.ProductName, p.Subcategory,
  COALESCE(s.TotalUnitsSold, 0) AS TotalUnitsSold,
  ROUND(COALESCE(inv.AvgOnHand, 0), 2) AS AvgOnHand,
  ROUND(CASE WHEN COALESCE(inv.AvgOnHand, 0) > 0
    THEN 1.0 * s.TotalUnitsSold / inv.AvgOnHand ELSE NULL END, 2) AS InventoryTurnover
FROM DimProduct p
LEFT JOIN sales_by_product s ON p.ProductID = s.ProductID
LEFT JOIN inv_by_product inv ON p.ProductID = inv.ProductID
ORDER BY InventoryTurnover ASC;

-- 4. How does performance vary by store and region?
SELECT st.Region, st.StoreName, SUM(s.Revenue) AS TotalRevenue, SUM(s.UnitsSold) AS TotalUnits
FROM FactSales s
JOIN DimStore st ON s.StoreID = st.StoreID
GROUP BY st.StoreID, st.StoreName, st.Region
ORDER BY st.Region, TotalRevenue DESC;

-- 5. Revenue and margin by subcategory
SELECT p.Subcategory, COUNT(DISTINCT p.ProductID) AS ProductCount,
  SUM(s.Revenue) AS TotalRevenue, SUM(s.UnitsSold) AS TotalUnits,
  ROUND(SUM(s.Revenue) - SUM(s.UnitsSold * p.Cost), 2) AS GrossProfit
FROM FactSales s
JOIN DimProduct p ON s.ProductID = p.ProductID
GROUP BY p.Subcategory
ORDER BY TotalRevenue DESC;
