# Baristas Coffee Shop — Power BI Dashboard Wireframe & Visual Spec

3-page report, dark-roast/espresso brand palette (deep brown `#3B2416`, cream
`#F5EBDD`, accent copper `#C08552`, success green `#4C8C4A` for growth, muted
red `#B5473C` for declines). Canvas: 1280×720, Power BI standard 16:9.

---

## Page 1 — Executive Sales Overview

```
┌───────────────────────────────────────────────────────────────────────────┐
│  BARISTAS COFFEE SHOP            [Date Slicer]  [Store Slicer]  [Channel] │
├───────────────┬───────────────┬───────────────┬───────────────────────────┤
│ Total Revenue │ Total Orders  │  AOV (TND)    │      Top Branch           │
│  84,815 TND   │    6,028      │   14.07 TND   │    Baristas La Marsa      │
│  ▲ MoM %      │  ▲ MoM %      │  ▲ MoM %      │   (KPI card, revenue tag) │
├───────────────┴───────────────┴───────────────┴───────────────────────────┤
│  HOURLY SALES — Morning Rush vs Afternoon Coffee Peak (Line/Area Chart)   │
│                                                                             │
│      revenue                    ╱╲          ╱────╲                        │
│         │              ╱╲      ╱  ╲        ╱      ╲                       │
│         │             ╱  ╲____╱    ╲______╱        ╲___                   │
│         └──────────────────────────────────────────────── hour (7-22)     │
│         shaded band: 08:00-10:30 (Morning) & 16:30-19:30 (Afternoon)      │
├───────────────────────────────┬───────────────────────────────────────────┤
│  PAYMENT METHOD MIX (Donut)   │  CHANNEL DISTRIBUTION (Stacked Bar)       │
│   Cash 55% / Carte 30% /      │   Walk-In / Takeaway / Glovo / Jumia,     │
│   Flouci 8% / D17 7%          │   stacked by day-part (Morning/Lunch/     │
│                                │   Afternoon Peak/Evening)                 │
├───────────────────────────────┴───────────────────────────────────────────┤
│  BRANCH PERFORMANCE — La Marsa vs Lac 2 vs Ennasr vs Menzah (Bar Chart)   │
│   Revenue (TND) bars, sorted descending, data labels, Full Cafe vs        │
│   Express color-coded                                                     │
└───────────────────────────────────────────────────────────────────────────┘
```

**Visual specs**

| Visual | Type | Fields | Notes |
|---|---|---|---|
| KPI cards (x4) | Card | `[Total Revenue (TND)]`, `[Total Transactions]`, `[Average Order Value (TND)]`, `[Top Branch]` | Add `[MoM Growth %]` as a trend indicator below each card |
| Hourly sales | Line/Area chart | Axis: `Dim_Time[Hour]`; Values: `[Total Revenue (TND)]` | Add two shaded reference bands (08:00-10:30, 16:30-19:30) via constant lines/analytics pane |
| Payment mix | Donut chart | Legend: `Dim_Payment[PaymentMethod]`; Values: `[Total Revenue (TND)]` | Data labels as % |
| Channel distribution | Stacked bar | Axis: `Dim_Time[TimeSlot]`; Legend: `Dim_Channel[ChannelName]`; Values: `[Total Revenue (TND)]` | Confirms delivery spike inside Afternoon Coffee Peak |
| Branch performance | Clustered/bar chart | Axis: `Dim_Store[StoreName]`; Values: `[Total Revenue (TND)]`; Color: `Dim_Store[StoreType]` | Sort descending by revenue |

**Slicers:** `Dim_Date[Date]` (range), `Dim_Store[StoreName]`, `Dim_Channel[ChannelName]` — placed in the top slicer bar, synced across all 3 pages.

---

## Page 2 — Menu & Product Performance

```
┌───────────────────────────────────────────────────────────────────────────┐
│  MENU & PRODUCT PERFORMANCE               [Date Slicer]  [Category]      │
├─────────────────────────────────────────┬─────────────────────────────────┤
│  UNIT MARGIN (TND) vs VOLUME SOLD        │  CATEGORY REVENUE BREAKDOWN     │
│  (Scatter Plot)                          │  (Treemap or Donut)             │
│                                           │                                  │
│  margin ▲                                │   Espresso & Classic Coffee     │
│    Hi  │  ★ Niche      ★ Stars           │   Cold Brew & Iced Coffee       │
│        │                                 │   Signature Frappes & Smoothies │
│    Lo  │  · · ·      ● Volume Drivers    │   Bakery & Pastries             │
│        └───────────────────────▶ volume  │   Savory Snacks                 │
│         bubble size = Total Revenue      │                                  │
├───────────────────────────────────────────────────────────────────────────┤
│  TOP / BOTTOM 10 PRODUCTS BY REVENUE (Horizontal Bar, ranked)             │
├───────────────────────────────────────────────────────────────────────────┤
│  PASTRY ATTACHMENT RATE %  |  DIGITAL vs CASH RATIO %   (KPI cards)       │
└───────────────────────────────────────────────────────────────────────────┘
```

**Visual specs**

| Visual | Type | Fields | Notes |
|---|---|---|---|
| Margin vs Volume | Scatter chart | X: `[Total Units Sold]`; Y: `Dim_Product[MarginTND]`; Details: `Dim_Product[ProductName]`; Size: `[Total Revenue (TND)]` | Add average lines (analytics pane) to split into 4 quadrants: **Stars** (high margin, high volume), **Volume Drivers** (low margin, high volume), **High-Margin Niche** (high margin, low volume), **Review** (low margin, low volume) |
| Category breakdown | Treemap or donut | Group: `Dim_Product[Category]`; Values: `[Total Revenue (TND)]` | Treemap preferred — shows relative size at a glance |
| Top/Bottom products | Bar chart (ranked) | Axis: `Dim_Product[ProductName]`; Values: `[Total Revenue (TND)]` | Use a Top N filter (10) toggled by a bookmark or slicer |
| KPI cards | Card | `[Pastry Attachment Rate %]`, `[Digital vs Cash Ratio %]` | Supports the "menu profitability" and "digital adoption" narrative |

---

## Page 3 — Transaction Audit & Search

```
┌───────────────────────────────────────────────────────────────────────────┐
│  TRANSACTION AUDIT & SEARCH        [Search Box]  [Date]  [Store]  [Channel]│
├───────────────────────────────────────────────────────────────────────────┤
│  TransactionID │ Date/Time │ Store │ Channel │ Payment │ Items │ Revenue  │
│  ─────────────────────────────────────────────────────────────────────── │
│  100482         │ 09/12 17:05│ Lac 2 │ Glovo   │ D17     │  3    │ 38.50 ▓│ <- >30 TND highlighted
│  100483         │ 09/12 17:11│ La Marsa│ Walk-In│ Cash   │  1    │  4.50  │
│  100484         │ 09/12 17:14│ Ennasr │ Takeaway│ Carte  │  2    │ 22.00  │
│  ...                                                                       │
└───────────────────────────────────────────────────────────────────────────┘
```

**Visual specs**

| Visual | Type | Fields | Notes |
|---|---|---|---|
| Transaction matrix | Table/Matrix | `TransactionID`, `Dim_Date[Date]` + `Dim_Time[Hour]`/`Minute`, `Dim_Store[StoreName]`, `Dim_Channel[ChannelName]`, `Dim_Payment[PaymentMethod]`, `[Total Units Sold]`, `[Total Revenue (TND)]` | Grouped/summarized at `TransactionID` grain (not raw line items) |
| Conditional formatting | Rule on `[Total Revenue (TND)]` | Background color scale or rule: `> 30` → copper/gold highlight | Implements the "high-value order" business rule via `[Is High Value Order (>30 TND)]` |
| Fulfillment status | Rule on `Dim_Channel[ChannelGroup]` | Icon set: In-Store = check icon, Delivery = truck icon | Simulated "fulfillment status" using channel group since no live delivery-status field exists in source data |
| Search box | Slicer (search-enabled) or Q&A visual | `TransactionID` or `Dim_Store[StoreName]` | Enables ad-hoc lookup for audit use cases |

**Drillthrough:** Right-click a bar on Page 1 (Branch Performance) or Page 2
(Top Products) → Drillthrough to Page 3, pre-filtered to that store/product,
for root-cause investigation.

---

## Theme notes

- Font: Segoe UI (default) or a rounded sans (e.g. Poppins) for a café-friendly feel.
- Number format: all currency measures formatted as `#,##0.00 "TND"` (custom format string), not `$`.
- Consistent color mapping across all 3 pages: `Dim_Channel[ChannelGroup]` and
  `Dim_Payment[PaymentType]` should use the same 2-color pairing everywhere
  (e.g. copper = In-Store/Cash-adjacent, teal = Delivery/Digital) so a reader
  builds pattern recognition across pages.
