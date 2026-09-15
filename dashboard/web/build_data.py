"""
Builds data.js for the Baristas Coffee Shop interactive web dashboard from the
CSVs produced by data_generator/generate_baristas_data.py. Encodes Fact_Sales
as compact numeric-coded rows (dimension lookups kept separately) so the
dataset stays small in the browser while remaining the real generated data.

Run from this folder:
    python build_data.py
"""

import json
import os

import pandas as pd

SRC = os.path.join("..", "..", "data_generator", "output")

fact = pd.read_csv(os.path.join(SRC, "fact_sales.csv"))
stores = pd.read_csv(os.path.join(SRC, "dim_stores.csv"))
products = pd.read_csv(os.path.join(SRC, "dim_products.csv"))
payment = pd.read_csv(os.path.join(SRC, "dim_payment.csv"))
channel = pd.read_csv(os.path.join(SRC, "dim_channel.csv"))

stores_lookup = {
    int(r.StoreKey): {"name": r.StoreName, "city": r.City, "region": r.Region, "type": r.StoreType}
    for r in stores.itertuples()
}
products_lookup = {
    int(r.ProductKey): {
        "name": r.ProductName,
        "category": r.Category,
        "cost": float(r.UnitCostTND),
        "price": float(r.UnitPriceTND),
        "margin": float(r.MarginTND),
    }
    for r in products.itertuples()
}
payment_lookup = {
    int(r.PaymentKey): {"method": r.PaymentMethod, "type": r.PaymentType}
    for r in payment.itertuples()
}
channel_lookup = {
    int(r.ChannelKey): {"name": r.ChannelName, "group": r.ChannelGroup}
    for r in channel.itertuples()
}

rows = []
for r in fact.itertuples():
    hour = int(r.TimeKey) // 100
    minute = int(r.TimeKey) % 100
    rows.append([
        int(r.TransactionID),
        int(r.DateKey),
        hour,
        minute,
        int(r.StoreKey),
        int(r.ChannelKey),
        int(r.PaymentKey),
        int(r.ProductKey),
        int(r.Quantity),
        round(float(r.LineRevenueTND), 2),
        round(float(r.LineCostTND), 2),
    ])

payload = {
    "meta": {
        "rowCount": len(rows),
        "transactionCount": int(fact["TransactionID"].nunique()),
        "minDateKey": int(fact["DateKey"].min()),
        "maxDateKey": int(fact["DateKey"].max()),
        "columns": ["transactionId", "dateKey", "hour", "minute", "storeKey",
                    "channelKey", "paymentKey", "productKey", "quantity",
                    "revenue", "cost"],
    },
    "stores": stores_lookup,
    "products": products_lookup,
    "payments": payment_lookup,
    "channels": channel_lookup,
    "rows": rows,
}

out_path = "data.js"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("window.BARISTAS_DATA = ")
    json.dump(payload, f, separators=(",", ":"))
    f.write(";\n")

size_kb = os.path.getsize(out_path) / 1024
print("Wrote {} ({} rows, {:.1f} KB)".format(out_path, len(rows), size_kb))
