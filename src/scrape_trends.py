import time
from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)

brands = ["Gucci", "Nike", "Zara", "Balenciaga", "H&M", "Valentino", "Christian Dior", "Louis Vuitton"]

all_data = []

for brand in brands:
    for attempt in range(3):  # retry up to 3 times
        try:
            pytrends.build_payload([brand], timeframe='today 5-y', geo='')
            df = pytrends.interest_over_time()
            df = df.reset_index()
            df['brand'] = brand
            df = df.rename(columns={brand: 'search_interest'})
            df = df[['date', 'brand', 'search_interest']]
            all_data.append(df)
            break  # success, move to next brand
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {brand}: {e}")
            time.sleep(30)  # wait longer before retrying
    time.sleep(10)  # normal delay between brands

final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv("data/raw/google_trends_brands.csv", index=False)

print("Done! Saved", len(final_df), "rows")
print(final_df.head())