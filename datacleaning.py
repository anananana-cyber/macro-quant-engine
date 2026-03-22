import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv("nse_5year_history.csv", low_memory=False)

# 2. FORCE CLEANING (Removes hidden spaces and fixes case)
df.columns = df.columns.str.strip().str.upper()

# 3. AUTO-DETECT COLUMNS (The Fix)
# We look for common NSE variations for 'Close' and 'Volume'
possible_close = ['CLOSE', 'CLOSE_PRICE', 'LAST_PRICE']
possible_vol = ['TOTTRDQTY', 'TOTAL_TRADED_QUANTITY', 'DELIV_QTY', 'TRADED_QTY']

# Pick the first one that actually exists in your CSV
close_col = next((c for c in possible_close if c in df.columns), None)
vol_col = next((v for v in possible_vol if v in df.columns), None)

if not close_col or not vol_col:
    print("❌ ERROR: Could not find Price or Volume columns.")
    print(f"Available columns are: {df.columns.tolist()}")
else:
    print(f"✅ Found Columns -> Price: {close_col} | Volume: {vol_col}")

    # 4. PERFORM CALCULATIONS USING DETECTED NAMES
    df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True)
    df = df.sort_values(by=['SYMBOL', 'DATE'])

    # Convert to numeric
    df[close_col] = pd.to_numeric(df[close_col], errors='coerce')
    df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce')

    # Log Returns & Liquidity
    df['LOG_RET'] = df.groupby('SYMBOL')[close_col].transform(lambda x: np.log(x / x.shift(1)))
    df['DOLLAR_VOLUME'] = df[close_col] * df[vol_col] # No more KeyError!

    print("\n--- Preprocessing Success ---")
    print(df[['DATE', 'SYMBOL', close_col, 'DOLLAR_VOLUME']].tail())
