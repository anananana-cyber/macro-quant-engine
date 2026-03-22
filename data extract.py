import pandas as pd
from nselib import capital_market
from datetime import datetime, timedelta
import time
import os

# 1. Configuration for 3 Years
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)  # Data of 5 years
current_date = start_date
csv_filename = "nse_3year_history.csv"

print(f"Starting extraction: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")

# 2. Execution Loop
while current_date <= end_date:
    date_str = current_date.strftime('%d-%m-%Y')
    
    try:
        # Fetching the full market snapshot for the day
        day_data = capital_market.bhav_copy_with_delivery(date_str)
        
        if day_data is not None and not day_data.empty:
            day_data['Date'] = date_str
            
            # Save to CSV immediately (Append mode)
            file_exists = os.path.isfile(csv_filename)
            day_data.to_csv(csv_filename, mode='a', index=False, header=not file_exists)
            
            print(f"✅ Data saved for {date_str}")
        else:
            # This handles weekends and market holidays
            print(f"Skipping {date_str} (No trading data)")
            
        # 3. Rate Limiting (Crucial for 3-year fetches)
        # Waiting 2.5 seconds prevents the NSE from blocking your IP
        time.sleep(2.5) 
        
    except Exception as e:
        # Silent skip for errors (likely connection resets or weekends)
        pass
        
    current_date += timedelta(days=1)

print(f"\nExtraction complete! Your 5-year database is ready in: {csv_filename}")
