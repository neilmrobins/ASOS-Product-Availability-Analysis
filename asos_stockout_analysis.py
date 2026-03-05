# notebooks/asos_stockout_analysis.ipynb

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Setup folders ---
os.makedirs("visuals", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# --- 2. Load and clean data ---
df = pd.read_csv(r"C:\Users\neilm\OneDrive\Career\Python\products_asos.csv")

# Ensure numeric prices and drop invalid
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df = df.dropna(subset=['price'])
df['description'] = df['description'].astype(str)

print(f"Data Loaded: {len(df)} rows")

# --- 3. Extract brands ---
def get_brand(text):
    if 'by ' in text:
        try:
            return text.split('by ')[1].split(' ')[0]
        except:
            return "Unknown"
    return "Unknown"

df['brand_raw'] = df['description'].apply(get_brand)

# Map common brands
brand_map = {
    'New': 'New Look',
    'River': 'River Island',
    'TopshopWelcome': 'Topshop'
}
df['Brand'] = df['brand_raw'].map(brand_map).fillna(df['brand_raw'])

# Keep brands with >5 products
Brand_counts = df['Brand'].value_counts()
valid_brands = Brand_counts[Brand_counts > 5].index
df_clean = df[df['Brand'].isin(valid_brands)].copy()

print("Top brands after cleaning:")
print(df_clean['Brand'].value_counts().head(5))

# --- 4. Stockout metrics ---
def calculate_phantom_revenue(size_str):
    """Returns (out_of_stock_count, rate) for a product size string"""
    if not isinstance(size_str, str):
        return 0, 0.0
    sizes = size_str.split(',')
    total_sizes = len(sizes)
    out_of_stock_count = size_str.count('Out of stock')
    rate = out_of_stock_count / total_sizes if total_sizes > 0 else 0.0
    return out_of_stock_count, rate

metrics = df_clean['size'].apply(lambda x: calculate_phantom_revenue(x))
df_clean['OutOfStockCount'] = [x[0] for x in metrics]
df_clean['OutOfStockRate'] = [x[1] for x in metrics]
df_clean['Lost_Revenue'] = df_clean['price'] * df_clean['OutOfStockCount']

# Export cleaned data for GitHub / reuse
df_clean.to_csv("data/processed/asos_cleaned_data.csv", index=False)

# --- 5. Brand-level aggregation ---
brand_strategy = df_clean.groupby('Brand').agg({
    'price': 'mean',
    'OutOfStockRate': 'mean',
    'Lost_Revenue': 'sum',
    'name': 'count'
}).reset_index()

brand_strategy = brand_strategy[brand_strategy['name'] > 10]

# --- 6. Plotting ---
fig, ax = plt.subplots(figsize=(12,8))

sns.scatterplot(
    data=brand_strategy,
    x='price',
    y='OutOfStockRate',
    size='Lost_Revenue',
    sizes=(50, 500),
    alpha=0.7,
    palette='viridis',
    ax=ax
)

# Highlight top opportunity brands
winners = brand_strategy[(brand_strategy['price'] > 40) & (brand_strategy['OutOfStockRate'] > 0.4)]
for i in range(len(winners)):
    ax.text(
        winners.iloc[i]['price']+1,
        winners.iloc[i]['OutOfStockRate'],
        winners.iloc[i]['Brand'],
        fontsize=9,
        weight='bold'
    )

# Titles and reference lines
ax.set_title('Brand Performance Analysis', fontsize=16)
ax.set_xlabel('Average Price (£)', fontsize=12)
ax.set_ylabel('Out of Stock Rate', fontsize=12)
ax.axvline(x=40, color='red', linestyle='--')
ax.axhline(y=0.4, color='red', linestyle='--')

# Save figure BEFORE plt.show()
fig.savefig("visuals/brand_performance_scatter.png", dpi=300, bbox_inches='tight')
plt.show()