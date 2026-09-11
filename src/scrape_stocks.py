import yfinance as yf
import pandas as pd

tickers = {
    "Nike": "NKE",
    "LVMH": "MC.PA",
    "Kering": "KER.PA",
    "Inditex": "ITX.MC",      # owns Zara
    "H&M": "HM-B.ST",
    "Adidas": "ADS.DE",
    "Ralph Lauren": "RL",
    "Capri Holdings": "CPRI", # owns Versace, Michael Kors
    "Tapestry": "TPR"

} 

all_data = []

for name, ticker in tickers.items():
    df = yf.download(ticker, period="5y", interval="1wk")
    
    # Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df = df.reset_index()
    df['brand'] = name
    df = df[['Date', 'brand', 'Close']]
    df = df.rename(columns={'Date': 'date', 'Close': 'close_price'})
    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv("data/raw/stock_prices.csv", index=False)

print("Done! Saved", len(final_df), "rows")
print(final_df.head())