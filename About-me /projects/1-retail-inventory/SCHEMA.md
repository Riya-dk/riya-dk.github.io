# Electronics retail – star schema

## Dimension tables
- **DimProduct**: ProductID, ProductName, Subcategory (Accessories, Computers, Displays, Phones), Cost, Price
- **DimStore**: StoreID, StoreName, Region
- **DimDate**: DateKey, FullDate, Month, Year

## Fact tables
- **FactSales**: ProductID, StoreID, DateKey, UnitsSold, Revenue
- **FactInventory**: ProductID, StoreID, DateKey, OnHandQty

## Relationships
- FactSales and FactInventory join to DimProduct, DimStore, DimDate on the respective IDs/keys.
