import pandas as pd
import numpy as np

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/Nassau_Candy_Distributor.csv")

# ── STEP 1: Parse date columns ─────────────────────────────────────────────────
# Dates are in DD-MM-YYYY format, so we use dayfirst=True
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
df['Ship Date']  = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')

# ── STEP 2: Calculate Lead Time (most important KPI) ──────────────────────────
# Lead Time = number of days between order placed and order shipped
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# ── STEP 3: Remove invalid rows ────────────────────────────────────────────────
# Negative lead time means ship date is before order date — that's impossible
df = df[df['Lead Time'] >= 0].reset_index(drop=True)

# ── STEP 4: Map each product to its source factory ────────────────────────────
# This tells us WHERE each order was manufactured (factory = origin of shipment)
factory_map = {
    "Wonka Bar - Nutty Crunch Surprise"  : "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows"          : "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious"     : "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate"         : "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel"  : "Wicked Choccy's",
    "Laffy Taffy"                        : "Sugar Shack",
    "SweeTARTS"                          : "Sugar Shack",
    "Nerds"                              : "Sugar Shack",
    "Fun Dip"                            : "Sugar Shack",
    "Fizzy Lifting Drinks"               : "Sugar Shack",
    "Everlasting Gobstopper"             : "Secret Factory",
    "Lickable Wallpaper"                 : "Secret Factory",
    "Wonka Gum"                          : "Secret Factory",
    "Hair Toffee"                        : "The Other Factory",
    "Kazookles"                          : "The Other Factory",
}
df['Factory'] = df['Product Name'].map(factory_map)

# ── STEP 5: Build Route column ────────────────────────────────────────────────
# Route = Factory → Customer Region  e.g.  "Sugar Shack → Pacific"
df['Route'] = df['Factory'] + " → " + df['Region']

# ── STEP 6: Flag delayed shipments ────────────────────────────────────────────
# A shipment is "delayed" if its lead time exceeds mean + 1 standard deviation
threshold = df['Lead Time'].mean() + df['Lead Time'].std()
df['Is Delayed'] = df['Lead Time'] > threshold


# ── ANALYSIS FUNCTIONS ─────────────────────────────────────────────────────────

def get_route_summary(data):
    """
    For every Factory → Region route, calculate:
    - Total shipments
    - Average lead time
    - Lead time variability (std dev)
    - Delay rate (% of shipments that were delayed)
    - Efficiency score (100 = fastest, 0 = slowest)
    """
    summary = data.groupby('Route').agg(
        Total_Shipments=('Row ID',      'count'),
        Avg_Lead_Time  =('Lead Time',   'mean'),
        Std_Lead_Time  =('Lead Time',   'std'),
        Delay_Rate     =('Is Delayed',  'mean')
    ).reset_index()

    summary['Avg_Lead_Time'] = summary['Avg_Lead_Time'].round(1)
    summary['Std_Lead_Time'] = summary['Std_Lead_Time'].round(1)
    summary['Delay_Rate']    = (summary['Delay_Rate'] * 100).round(1)  # as %

    # Efficiency Score: higher = better (faster route)
    max_lt = summary['Avg_Lead_Time'].max()
    min_lt = summary['Avg_Lead_Time'].min()
    summary['Efficiency_Score'] = (
        (max_lt - summary['Avg_Lead_Time']) / (max_lt - min_lt) * 100
    ).round(1)

    return summary.sort_values('Avg_Lead_Time')


def get_shipmode_summary(data):
    """
    Compare shipping methods: Standard Class, First Class, Second Class, Same Day
    Shows trade-off between cost and speed
    """
    return data.groupby('Ship Mode').agg(
        Orders        =('Row ID',    'count'),
        Avg_Lead_Time =('Lead Time', 'mean'),
        Delay_Rate    =('Is Delayed','mean'),
        Avg_Cost      =('Cost',      'mean'),
        Total_Sales   =('Sales',     'sum')
    ).round(2).reset_index()


def get_region_summary(data):
    """
    Regional performance: Interior, Atlantic, Gulf, Pacific
    Helps identify which delivery zones are problematic
    """
    return data.groupby('Region').agg(
        Orders        =('Row ID',    'count'),
        Avg_Lead_Time =('Lead Time', 'mean'),
        Delay_Rate    =('Is Delayed','mean'),
        Total_Sales   =('Sales',     'sum')
    ).round(2).reset_index()


def get_state_summary(data):
    """
    State-level bottleneck detection
    Used for the US choropleth map — darker = slower delivery
    """
    return data.groupby('State/Province').agg(
        Orders        =('Row ID',    'count'),
        Avg_Lead_Time =('Lead Time', 'mean'),
        Delay_Rate    =('Is Delayed','mean')
    ).round(2).reset_index()
 