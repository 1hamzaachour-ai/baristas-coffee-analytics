Built a full sales analytics case study for a Tunisian specialty coffee
chain: "Baristas Coffee Shop" — from raw data model to a 3-page Power BI
dashboard.

The goal was to answer the questions a real café operator in Tunisia would
actually ask:

☕ When do we really peak — and is staffing matching it? Morning Rush
(08:00-10:30) and an Afternoon Coffee Peak (16:30-19:30) turned out to have
very different product mixes: espresso + pastries in the morning, cold
brews and frappés in the afternoon.

💳 How fast is digital payment adoption moving? Cash still leads at ~55%,
but Carte Bancaire, Flouci and D17 together already account for a real,
trackable share of revenue — worth watching quarter over quarter.

🛵 What's delivery actually worth? Glovo and Jumia Food volume roughly
doubles inside that same afternoon peak window versus the rest of the day —
a clear signal for when packaging and courier readiness matter most.

🥐 Which menu items are Stars vs. Volume Drivers vs. High-Margin Niche
plays? A margin-vs-volume scatter plot made the menu profitability story
obvious in a way a flat sales table never does.

🛠️ Tools: Power BI | DAX | Power Query | Star Schema | Time Intelligence

Technical build:
- Star schema data model (1 fact table, 6 dimensions) designed for
  transaction-line grain
- Python (pandas/NumPy) synthetic data generator modeling realistic
  Tunisian café traffic, TND pricing, and local payment habits
- Power Query for transformation, DAX for time intelligence and business
  KPIs (MoM growth, YTD, Peak Sales Hour, Pastry Attachment Rate)
- A 3-page Power BI report: Executive Overview, Menu & Product Performance,
  and a searchable Transaction Audit page

Full project (star schema, generator script, DAX library, and wireframes)
is on GitHub — link in comments.

#PowerBI #DataAnalytics #DAX #BusinessIntelligence #Tunisia #DataEngineering
