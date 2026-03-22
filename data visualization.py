import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. FIX COLUMN NAMES AGAIN (To be safe)
df.columns = df.columns.str.strip().str.upper()

# 2. DYNAMIC DETECTION (Finds 'CLOSE' or 'CLOSE_PRICE' automatically)
close_col = next((c for c in ['CLOSE', 'CLOSE_PRICE', 'LAST_PRICE'] if c in df.columns), None)
date_col = 'DATE' 
vol_col = next((v for v in ['TOTTRDQTY', 'TOTAL_TRADED_QUANTITY', 'DELIV_QTY'] if v in df.columns), None)

if not close_col:
    print(f"❌ Still can't find Close column. Columns available are: {df.columns.tolist()}")
else:
    print(f"✅ Using '{close_col}' for plotting.")

    # --- 1. MARKET TREND ---
    plt.figure(figsize=(12, 6))
    # We use the detected close_col here instead of 'CLOSE'
    df.groupby(date_col)[close_col].median().plot(color='royalblue', lw=2)
    plt.title('NSE Market Trend (Median Price of All Stocks)', fontsize=14)
    plt.ylabel('Price (INR)')
    plt.grid(True, alpha=0.3)
    plt.show()

    # --- 2. VOLATILITY DISTRIBUTION ---
    if 'LOG_RET' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['LOG_RET'].dropna(), bins=100, kde=True, color='purple')
        plt.title('Market-Wide Return Distribution', fontsize=14)
        plt.xlabel('Log Returns')
        plt.xlim(-0.1, 0.1) 
        plt.show()

    # --- 3. LIQUIDITY LEADERS ---
    # Using the detected vol_col
    if vol_col:
        plt.figure(figsize=(10, 6))
        df['DOLLAR_VOLUME'] = df[close_col] * df[vol_col]
        top_liquid = df.groupby('SYMBOL')['DOLLAR_VOLUME'].mean().sort_values(ascending=False).head(15)
        top_liquid.plot(kind='barh', color='teal')
        plt.title('Top 15 Most Liquid Stocks', fontsize=14)
        plt.gca().invert_yaxis()
        plt.show()
