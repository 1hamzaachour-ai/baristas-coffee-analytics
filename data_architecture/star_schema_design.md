# Baristas Coffee Shop — Star Schema Design

Sales analytics data model for **Baristas Coffee Shop**, a Tunisian specialty coffee
chain (espresso, cold brew, frappés, artisanal pastries). Grain, relationships and
attributes are purpose-built for the Tunisian market: TND pricing, local mobile
wallets (Flouci, D17), and Tunisian delivery platforms (Glovo, Jumia Food).

## 1. Model overview

Star schema — one central fact table, six conformed dimensions, all single-direction
(dimension → fact) 1-to-Many relationships. No snowflaking, no bidirectional filters —
keeps the model fast and predictable for DAX time intelligence.

```
                     Dim_Date  ────┐
                                   │
                     Dim_Time  ────┤
                                   │
                    Dim_Store  ────┤
                                   ├──▶  Fact_Sales
                  Dim_Product  ────┤
                                   │
                  Dim_Payment  ────┤
                                   │
                  Dim_Channel  ────┘
```

## 2. Fact_Sales

**Grain: one row per ordered line item, per transaction.** A single receipt
(e.g. 1 Cappuccino + 1 Croissant) produces two fact rows sharing the same
`TransactionID`.

| Column            | Type    | Description                                              |
|-------------------|---------|------------------------------------------------------------|
| `SalesLineID`      | INT (PK) | Surrogate key, unique per line item                        |
| `TransactionID`     | INT      | Groups line items belonging to the same order/receipt      |
| `DateKey`           | INT (FK) | → `Dim_Date.DateKey`                                        |
| `TimeKey`           | INT (FK) | → `Dim_Time.TimeKey`                                         |
| `StoreKey`          | INT (FK) | → `Dim_Store.StoreKey`                                        |
| `ProductKey`        | INT (FK) | → `Dim_Product.ProductKey`                                     |
| `PaymentKey`        | INT (FK) | → `Dim_Payment.PaymentKey`                                      |
| `ChannelKey`        | INT (FK) | → `Dim_Channel.ChannelKey`                                       |
| `Quantity`          | INT      | Units of the product sold in this line                            |
| `UnitPriceTND`      | DECIMAL  | Price at time of sale (may reflect promo — kept at line grain)     |
| `UnitCostTND`       | DECIMAL  | COGS at time of sale                                                |
| `LineRevenueTND`    | DECIMAL  | `Quantity * UnitPriceTND`                                            |
| `LineCostTND`       | DECIMAL  | `Quantity * UnitCostTND`                                              |
| `LineProfitTND`     | DECIMAL  | `LineRevenueTND - LineCostTND`                                         |

**Design notes**
- Keeping `UnitPriceTND`/`UnitCostTND` on the fact row (not only in `Dim_Product`)
  preserves historical pricing accuracy if menu prices change over the 6-month window.
- `TransactionID` is intentionally **not** the fact grain — it enables basket-level
  measures (AOV, Pastry Attachment Rate) via `DISTINCTCOUNT`/`SUMMARIZE` without a
  separate transaction-header table.

## 3. Dimension tables

### Dim_Date
Standard calendar dimension, one row per calendar day covering the 6-month window
(and ideally a full rolling year for YoY headroom).

| Column | Type | Description |
|---|---|---|
| `DateKey` (PK) | INT | YYYYMMDD |
| `Date` | DATE | Full date |
| `Day` | INT | Day of month |
| `DayName` | TEXT | Monday…Sunday |
| `DayOfWeekNum` | INT | 1 (Mon) – 7 (Sun) |
| `IsWeekend` | BOOLEAN | Fri/Sat treated as Tunisian weekend-adjacent per store calendar |
| `Month` | INT | 1–12 |
| `MonthName` | TEXT | January…December |
| `MonthYear` | TEXT | "Jan 2026" — sort by `Year*100+Month` |
| `Quarter` | TEXT | Q1…Q4 |
| `Year` | INT | Calendar year |
| `IsHoliday` | BOOLEAN | Tunisian public holidays flag (optional enrichment) |

### Dim_Time
Intraday time dimension at minute grain, mapped to named Tunisian café traffic slots.

| Column | Type | Description |
|---|---|---|
| `TimeKey` (PK) | INT | HHMM as integer, e.g. 830 |
| `Hour` | INT | 0–23 |
| `Minute` | INT | 0–59 |
| `TimeSlot` | TEXT | Morning Rush / Midday Lunch / Afternoon Coffee Peak / Evening Social |

`TimeSlot` mapping used consistently across generator, DAX and visuals:

| Slot | Hours |
|---|---|
| Morning Rush | 07:00 – 10:30 |
| Midday Lunch | 10:30 – 14:00 |
| Afternoon Coffee Peak | 14:00 – 19:00 |
| Evening Social | 19:00 – 22:00 |

### Dim_Store
| Column | Type | Description |
|---|---|---|
| `StoreKey` (PK) | INT | Surrogate key |
| `StoreName` | TEXT | e.g. "Baristas La Marsa" |
| `City` | TEXT | La Marsa, Lac 2, Ennasr, Menzah |
| `Region` | TEXT | Greater Tunis / Sahel / South |
| `StoreType` | TEXT | Express (kiosk/takeaway-first) vs Full Café (dine-in + terrace) |
| `OpenDate` | DATE | Store opening date |

### Dim_Product
| Column | Type | Description |
|---|---|---|
| `ProductKey` (PK) | INT | Surrogate key |
| `ProductName` | TEXT | e.g. "Iced Caramel Frappé" |
| `Category` | TEXT | Espresso & Classic Coffee / Cold Brew & Frappes / Pastries & Bakery / Savory Snacks |
| `UnitCostTND` | DECIMAL | Standard cost |
| `UnitPriceTND` | DECIMAL | Standard menu price |
| `MarginTND` | DECIMAL | `UnitPriceTND - UnitCostTND` |

### Dim_Payment
| Column | Type | Description |
|---|---|---|
| `PaymentKey` (PK) | INT | Surrogate key |
| `PaymentMethod` | TEXT | Cash / Carte Bancaire / Flouci / D17 |
| `PaymentType` | TEXT | Cash vs Digital (grouping attribute for Digital Payment Adoption %) |

### Dim_Channel
| Column | Type | Description |
|---|---|---|
| `ChannelKey` (PK) | INT | Surrogate key |
| `ChannelName` | TEXT | Walk-In / Dine-In, Takeaway, Glovo, Jumia Food |
| `ChannelGroup` | TEXT | In-Store vs Delivery (grouping attribute for Delivery vs In-Store Mix) |

## 4. Relationships (Power BI model view)

All relationships are **1-to-Many, single filter direction, dimension → fact**:

| From | To | Cardinality | Filter direction |
|---|---|---|---|
| `Dim_Date[DateKey]` | `Fact_Sales[DateKey]` | 1:* | Single (Date → Fact) |
| `Dim_Time[TimeKey]` | `Fact_Sales[TimeKey]` | 1:* | Single |
| `Dim_Store[StoreKey]` | `Fact_Sales[StoreKey]` | 1:* | Single |
| `Dim_Product[ProductKey]` | `Fact_Sales[ProductKey]` | 1:* | Single |
| `Dim_Payment[PaymentKey]` | `Fact_Sales[PaymentKey]` | 1:* | Single |
| `Dim_Channel[ChannelKey]` | `Fact_Sales[ChannelKey]` | 1:* | Single |

Mark `Dim_Date` as the official **Date Table** in Power BI (Table tools → Mark as
Date Table) to unlock native DAX time-intelligence functions (`TOTALYTD`,
`SAMEPERIODLASTYEAR`, etc.).

No many-to-many or bidirectional relationships are needed — every dimension
attribute a visual needs (TimeSlot, PaymentType, ChannelGroup, Category) is
pre-computed and stored directly on its dimension row, not derived through a
second hop.
