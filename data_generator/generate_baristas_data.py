"""
Baristas Coffee Shop - Synthetic Sales Data Generator
=======================================================
Generates a realistic 6-month sales dataset (fact + dimensions) for the
Baristas Coffee Shop Power BI project. Models Tunisian market specifics:
TND pricing, local payment habits (Cash / Carte Bancaire / Flouci / D17),
and local traffic patterns (Morning Rush, Afternoon Coffee Peak).

Output: CSV files written to ./data/, ready to be loaded into Power BI
via Power Query (Get Data > Folder, or one-by-one CSV import).

Run:
    python generate_baristas_data.py
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TARGET_LINE_ITEMS = 10_000          # Fact_Sales row target (grain = line item)
END_DATE = datetime(2026, 9, 14)
START_DATE = END_DATE - timedelta(days=183)   # ~6 months of trading history

OUTPUT_DIR = "data"

# Café operating window
OPEN_HOUR, OPEN_MIN = 7, 0
CLOSE_HOUR, CLOSE_MIN = 22, 0

# Named traffic slots (must match Dim_Time.TimeSlot in the star schema)
TIME_SLOTS = [
    ("Morning Rush", 7 * 60, 10 * 60 + 30),
    ("Midday Lunch", 10 * 60 + 30, 14 * 60),
    ("Afternoon Coffee Peak", 14 * 60, 19 * 60),
    ("Evening Social", 19 * 60, 22 * 60),
]

# Explicit local peak windows called out in the brief (minutes-from-midnight)
MORNING_PEAK = (8 * 60, 10 * 60 + 30)          # 08:00 - 10:30, espresso & pastry
AFTERNOON_PEAK = (16 * 60 + 30, 19 * 60 + 30)  # 16:30 - 19:30, cold drinks & social

# ---------------------------------------------------------------------------
# Dim_Store
# ---------------------------------------------------------------------------
stores = [
    {"StoreKey": 1, "StoreName": "Baristas La Marsa", "City": "La Marsa", "Region": "Greater Tunis", "StoreType": "Full Cafe",  "OpenDate": "2022-03-01", "TrafficWeight": 1.35},
    {"StoreKey": 2, "StoreName": "Baristas Lac 2",     "City": "Lac 2",    "Region": "Greater Tunis", "StoreType": "Full Cafe",  "OpenDate": "2021-11-15", "TrafficWeight": 1.30},
    {"StoreKey": 3, "StoreName": "Baristas Ennasr",    "City": "Ennasr",   "Region": "Greater Tunis", "StoreType": "Express",    "OpenDate": "2023-01-10", "TrafficWeight": 0.95},
    {"StoreKey": 4, "StoreName": "Baristas Menzah",    "City": "Menzah",   "Region": "Greater Tunis", "StoreType": "Full Cafe",  "OpenDate": "2022-07-20", "TrafficWeight": 1.05},
]
dim_store_df = pd.DataFrame(stores).drop(columns=["TrafficWeight"])
store_weights = np.array([s["TrafficWeight"] for s in stores])
store_weights = store_weights / store_weights.sum()

# ---------------------------------------------------------------------------
# Dim_Product  (category -> [(name, unit_cost, unit_price), ...])
# ---------------------------------------------------------------------------
product_catalog = {
    "Espresso & Classic Coffee": [
        ("Espresso",               1.4, 3.5),
        ("Espresso Macchiato",     1.6, 4.0),
        ("Americano",              1.5, 3.8),
        ("Cappuccino",             1.9, 4.5),
        ("Cafe Latte",             2.0, 4.8),
        ("Flat White",             2.1, 5.0),
        ("Cafe Creme",             1.8, 4.3),
    ],
    "Cold Brew & Frappes": [
        ("Cold Brew Original",     3.2, 8.5),
        ("Iced Latte",             3.4, 9.0),
        ("Iced Americano",         3.0, 8.0),
        ("Iced Caramel Macchiato", 3.8, 10.5),
        ("Caramel Frappe",         4.2, 12.0),
        ("Mocha Frappe",           4.3, 12.5),
        ("Matcha Ice Blend",       4.6, 13.5),
        ("Mixed Berry Smoothie",   4.0, 11.0),
        ("Mango Passion Smoothie", 4.1, 11.5),
    ],
    "Pastries & Bakery": [
        ("Butter Croissant",       1.6, 4.5),
        ("Pain au Chocolat",       1.8, 5.0),
        ("Blueberry Muffin",       2.0, 5.5),
        ("Cinnamon Roll",          2.4, 6.5),
        ("Cheesecake Slice",       3.2, 9.0),
    ],
    "Savory Snacks": [
        ("Chicken Panini",         3.6, 9.5),
        ("Turkey & Cheese Wrap",   3.4, 9.0),
        ("Vegetable Quiche",       3.0, 8.0),
        ("Tuna Sandwich",          3.2, 8.5),
    ],
}

product_rows = []
pk = 1
for category, items in product_catalog.items():
    for name, cost, price in items:
        product_rows.append({
            "ProductKey": pk,
            "ProductName": name,
            "Category": category,
            "UnitCostTND": cost,
            "UnitPriceTND": price,
            "MarginTND": round(price - cost, 2),
        })
        pk += 1
dim_products_df = pd.DataFrame(product_rows)

# Category popularity baseline (used outside of the two named peak windows)
category_base_weight = {
    "Espresso & Classic Coffee": 0.36,
    "Cold Brew & Frappes": 0.34,
    "Pastries & Bakery": 0.20,
    "Savory Snacks": 0.10,
}

# Category weighting during the two named local peaks
morning_peak_weight = {
    "Espresso & Classic Coffee": 0.52,
    "Cold Brew & Frappes": 0.12,
    "Pastries & Bakery": 0.30,
    "Savory Snacks": 0.06,
}
afternoon_peak_weight = {
    "Espresso & Classic Coffee": 0.18,
    "Cold Brew & Frappes": 0.59,
    "Pastries & Bakery": 0.13,
    "Savory Snacks": 0.10,
}


def pick_product(minute_of_day: int) -> dict:
    """Pick a product row, weighting categories by the current time-of-day peak."""
    if MORNING_PEAK[0] <= minute_of_day < MORNING_PEAK[1]:
        cat_weights = morning_peak_weight
    elif AFTERNOON_PEAK[0] <= minute_of_day < AFTERNOON_PEAK[1]:
        cat_weights = afternoon_peak_weight
    else:
        cat_weights = category_base_weight

    categories = list(cat_weights.keys())
    probs = np.array(list(cat_weights.values()))
    probs = probs / probs.sum()
    chosen_category = np.random.choice(categories, p=probs)

    items_in_cat = dim_products_df[dim_products_df["Category"] == chosen_category]
    return items_in_cat.sample(1, weights=None).iloc[0]


# ---------------------------------------------------------------------------
# Dim_Payment   (~55% Cash / ~30% Carte Bancaire / ~15% Mobile Wallets)
# ---------------------------------------------------------------------------
payments = [
    {"PaymentKey": 1, "PaymentMethod": "Cash",            "PaymentType": "Cash"},
    {"PaymentKey": 2, "PaymentMethod": "Carte Bancaire",   "PaymentType": "Digital"},
    {"PaymentKey": 3, "PaymentMethod": "Flouci",           "PaymentType": "Digital"},
    {"PaymentKey": 4, "PaymentMethod": "D17",              "PaymentType": "Digital"},
]
dim_payment_df = pd.DataFrame(payments)
payment_weights = [0.55, 0.30, 0.08, 0.07]   # Flouci/D17 split the 15% mobile wallet share

# ---------------------------------------------------------------------------
# Dim_Channel   (walk-in heavy baseline; delivery spikes handled at runtime)
# ---------------------------------------------------------------------------
channels = [
    {"ChannelKey": 1, "ChannelName": "Walk-In / Dine-In", "ChannelGroup": "In-Store"},
    {"ChannelKey": 2, "ChannelName": "Takeaway",           "ChannelGroup": "In-Store"},
    {"ChannelKey": 3, "ChannelName": "Glovo",               "ChannelGroup": "Delivery"},
    {"ChannelKey": 4, "ChannelName": "Jumia Food",           "ChannelGroup": "Delivery"},
]
dim_channel_df = pd.DataFrame(channels)

# Baseline channel mix (most of the day)
CHANNEL_BASELINE = [0.55, 0.25, 0.11, 0.09]
# Delivery-heavy mix used only inside the afternoon peak window
CHANNEL_AFTERNOON_PEAK = [0.35, 0.15, 0.28, 0.22]


def pick_channel(minute_of_day: int) -> int:
    if AFTERNOON_PEAK[0] <= minute_of_day < AFTERNOON_PEAK[1]:
        weights = CHANNEL_AFTERNOON_PEAK
    else:
        weights = CHANNEL_BASELINE
    return int(np.random.choice([c["ChannelKey"] for c in channels], p=weights))


# ---------------------------------------------------------------------------
# Dim_Date  (full calendar coverage of the trading window)
# ---------------------------------------------------------------------------
date_rows = []
d = START_DATE
while d <= END_DATE:
    date_rows.append({
        "DateKey": int(d.strftime("%Y%m%d")),
        "Date": d.strftime("%Y-%m-%d"),
        "Day": d.day,
        "DayName": d.strftime("%A"),
        "DayOfWeekNum": d.isoweekday(),
        "IsWeekend": d.isoweekday() in (5, 6),   # Fri/Sat treated as Tunisian weekend
        "Month": d.month,
        "MonthName": d.strftime("%B"),
        "MonthYear": d.strftime("%b %Y"),
        "Quarter": f"Q{(d.month - 1) // 3 + 1}",
        "Year": d.year,
    })
    d += timedelta(days=1)
dim_date_df = pd.DataFrame(date_rows)

# ---------------------------------------------------------------------------
# Dim_Time  (minute grain across the operating window, mapped to TimeSlot)
# ---------------------------------------------------------------------------
def time_slot_for(minute_of_day: int) -> str:
    for name, start, end in TIME_SLOTS:
        if start <= minute_of_day < end:
            return name
    return "Closed"


time_rows = []
for h in range(OPEN_HOUR, CLOSE_HOUR + 1):
    for m in range(0, 60):
        if h == CLOSE_HOUR and m > CLOSE_MIN:
            continue
        minute_of_day = h * 60 + m
        time_rows.append({
            "TimeKey": h * 100 + m,
            "Hour": h,
            "Minute": m,
            "TimeSlot": time_slot_for(minute_of_day),
        })
dim_time_df = pd.DataFrame(time_rows)

# ---------------------------------------------------------------------------
# Transaction / timestamp sampling helpers
# ---------------------------------------------------------------------------
# Minute-of-day sampling weights: heavy mass on the two named peaks, a lighter
# lunch bump, and thin background traffic elsewhere within opening hours.
open_minute = OPEN_HOUR * 60 + OPEN_MIN
close_minute = CLOSE_HOUR * 60 + CLOSE_MIN
all_minutes = np.arange(open_minute, close_minute + 1)


def minute_weight(m: int) -> float:
    if MORNING_PEAK[0] <= m < MORNING_PEAK[1]:
        return 5.0
    if AFTERNOON_PEAK[0] <= m < AFTERNOON_PEAK[1]:
        return 5.5
    if 10 * 60 + 30 <= m < 14 * 60:      # lunch bump
        return 2.0
    return 1.0


minute_probs = np.array([minute_weight(m) for m in all_minutes], dtype=float)
minute_probs = minute_probs / minute_probs.sum()

# Day-of-week weighting: Thursday-Saturday sociable evenings run busier
dow_weight = {1: 0.95, 2: 0.95, 3: 1.0, 4: 1.05, 5: 1.25, 6: 1.30, 7: 1.0}  # ISO 1=Mon..7=Sun
date_probs = np.array([dow_weight[datetime.strptime(r["Date"], "%Y-%m-%d").isoweekday()]
                        for r in date_rows], dtype=float)
date_probs = date_probs / date_probs.sum()
date_keys = dim_date_df["DateKey"].to_numpy()

# Basket size distribution: mostly 1-2 items, occasionally 3
BASKET_SIZE_CHOICES = [1, 2, 3]
BASKET_SIZE_WEIGHTS = [0.50, 0.35, 0.15]

# ---------------------------------------------------------------------------
# Generate Fact_Sales
# ---------------------------------------------------------------------------
fact_rows = []
transaction_id = 100000
line_id = 1

while len(fact_rows) < TARGET_LINE_ITEMS:
    transaction_id += 1

    date_key = int(np.random.choice(date_keys, p=date_probs))
    minute_of_day = int(np.random.choice(all_minutes, p=minute_probs))
    time_key = (minute_of_day // 60) * 100 + (minute_of_day % 60)
    store_key = int(np.random.choice([s["StoreKey"] for s in stores], p=store_weights))
    channel_key = pick_channel(minute_of_day)
    payment_key = int(np.random.choice([p["PaymentKey"] for p in payments], p=payment_weights))

    basket_size = int(np.random.choice(BASKET_SIZE_CHOICES, p=BASKET_SIZE_WEIGHTS))
    basket_size = min(basket_size, TARGET_LINE_ITEMS - len(fact_rows))  # don't overshoot target

    for _ in range(basket_size):
        product = pick_product(minute_of_day)
        quantity = int(np.random.choice([1, 2], p=[0.85, 0.15]))

        unit_price = float(product["UnitPriceTND"])
        unit_cost = float(product["UnitCostTND"])
        line_revenue = round(unit_price * quantity, 2)
        line_cost = round(unit_cost * quantity, 2)

        fact_rows.append({
            "SalesLineID": line_id,
            "TransactionID": transaction_id,
            "DateKey": date_key,
            "TimeKey": time_key,
            "StoreKey": store_key,
            "ProductKey": int(product["ProductKey"]),
            "PaymentKey": payment_key,
            "ChannelKey": channel_key,
            "Quantity": quantity,
            "UnitPriceTND": unit_price,
            "UnitCostTND": unit_cost,
            "LineRevenueTND": line_revenue,
            "LineCostTND": line_cost,
            "LineProfitTND": round(line_revenue - line_cost, 2),
        })
        line_id += 1

fact_sales_df = pd.DataFrame(fact_rows)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

fact_sales_df.to_csv(f"{OUTPUT_DIR}/fact_sales.csv", index=False)
dim_products_df.to_csv(f"{OUTPUT_DIR}/dim_products.csv", index=False)
dim_store_df.to_csv(f"{OUTPUT_DIR}/dim_store.csv", index=False)
dim_payment_df.to_csv(f"{OUTPUT_DIR}/dim_payment.csv", index=False)
dim_channel_df.to_csv(f"{OUTPUT_DIR}/dim_channel.csv", index=False)
# Bonus: full Dim_Date / Dim_Time so the model is importable as-is (Part 1 schema)
dim_date_df.to_csv(f"{OUTPUT_DIR}/dim_date.csv", index=False)
dim_time_df.to_csv(f"{OUTPUT_DIR}/dim_time.csv", index=False)

print("Baristas Coffee Shop - synthetic dataset generated")
print("Date range: {} to {}".format(START_DATE.date(), END_DATE.date()))
print("Fact_Sales rows: {}".format(len(fact_sales_df)))
print("Transactions: {}".format(fact_sales_df["TransactionID"].nunique()))
print("Total revenue (TND): {:,.2f}".format(fact_sales_df["LineRevenueTND"].sum()))
print("Output folder: {}".format(os.path.abspath(OUTPUT_DIR)))
