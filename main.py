import requests
import pandas as pd
import yfinance as yf
import sqlite3

# -----------------------------
# 1. TOP 3 CRYPTO COINS
# -----------------------------
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=10"
data = requests.get(url).json()
df = pd.DataFrame(data)

crypto_full = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'market_cap_rank',
                  'total_volume', 'circulating_supply', 'total_supply', 'ath', 'atl', 'last_updated']].copy()

# Fix date
crypto_full['date'] = pd.to_datetime(crypto_full['last_updated']).dt.strftime('%Y-%m-%d')
crypto_full = crypto_full.drop(columns=['last_updated'])

top_3 = crypto_full.sort_values('market_cap_rank').head(3)[['id', 'symbol', 'name', 'market_cap_rank']]

print("Top 3 coins:")
print(top_3)

# Save CSV
crypto_full.to_csv("crypto_data.csv", index=False)
top_3.to_csv("top_3_coins.csv", index=False)

# -----------------------------
# 2. HISTORICAL CRYPTO PRICES
# -----------------------------
all_data = []

for _, row in top_3.iterrows():
    coin = row['id']
    print(f"Fetching crypto history for {coin}...")

    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=inr&days=365"
    data = requests.get(url).json()

    prices = data['prices']

    for p in prices:
        date = pd.to_datetime(p[0], unit='ms').strftime('%Y-%m-%d')
        price = p[1]

        all_data.append({
            "coin_id": coin,
            "date": date,
            "price_usd": price
        })

price_df = pd.DataFrame(all_data)
price_df.to_csv("crypto_price_1year.csv", index=False)
print("Crypto history saved!")

# -----------------------------
# 3. OIL PRICE DATA
# -----------------------------
oil_url = "https://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv"
oil_df = pd.read_csv(oil_url)

# Fix date
oil_df['Date'] = pd.to_datetime(oil_df['Date']).dt.strftime('%Y-%m-%d')

# Filter date
oil_df = oil_df[
    (oil_df['Date'] >= '2020-01-01') &
    (oil_df['Date'] <= '2026-01-31')
]

oil_df = oil_df.rename(columns={
    'Date': 'date',
    'Price': 'price_usd'
})

oil_df.to_csv("oil_prices.csv", index=False)
print("Oil data saved!")

# -----------------------------
# 4. STOCK PRICE DATA
# -----------------------------
tickers = ["^GSPC", "^IXIC", "^NSEI"]
stock_list = []

for ticker in tickers:
    print(f"Fetching stock data for {ticker}...")

    stock_df = yf.download(ticker, start="2020-01-01", end="2025-09-30")

    stock_df = stock_df.reset_index()

    # FIX MultiIndex problem
    stock_df.columns = [col[0] if isinstance(col, tuple) else col for col in stock_df.columns]

    # Fix date
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.strftime('%Y-%m-%d')

    stock_df["ticker"] = ticker

    stock_df = stock_df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    stock_df = stock_df[['date', 'open', 'high', 'low', 'close', 'volume', 'ticker']]

    stock_list.append(stock_df)

final_stock_df = pd.concat(stock_list, ignore_index=True)
final_stock_df.to_csv("stock_prices.csv", index=False)

print("Stock data saved!")

# -----------------------------
# 5. CREATE SQLITE DATABASE
# -----------------------------
conn = sqlite3.connect("cross_market.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS cryptocurrencies (
    id TEXT PRIMARY KEY,
    symbol TEXT,
    name TEXT,
    current_price REAL,
    market_cap REAL,
    market_cap_rank INTEGER,
    total_volume REAL,
    circulating_supply REAL,
    total_supply REAL,
    ath REAL,
    atl REAL,
    date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    coin_id TEXT,
    date TEXT,
    price_usd REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS oil_prices (
    date TEXT PRIMARY KEY,
    price_usd REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices (
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    ticker TEXT
)
""")

conn.commit()

# Insert data
crypto_full.to_sql("cryptocurrencies", conn, if_exists="replace", index=False)
price_df.to_sql("crypto_prices", conn, if_exists="replace", index=False)
oil_df.to_sql("oil_prices", conn, if_exists="replace", index=False)
final_stock_df.to_sql("stock_prices", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database created successfully!")