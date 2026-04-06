import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("cross_market.db")
query_check = "PRAGMA table_info(stock_prices);"
print(pd.read_sql_query(query_check, conn))

# Query 1: Top 3 cryptocurrencies by market cap
query1 = """
SELECT id, symbol, name, market_cap, market_cap_rank
FROM cryptocurrencies
ORDER BY market_cap DESC
LIMIT 3;
"""

result1 = pd.read_sql_query(query1, conn)

print("Top 3 cryptocurrencies by market cap:")
print(result1)
print("-" * 50)

# Query 2: Highest daily price of Bitcoin in last 365 days
query2 = """
SELECT coin_id, MAX(price_usd) AS highest_price
FROM crypto_prices
WHERE coin_id = 'bitcoin';
"""

result2 = pd.read_sql_query(query2, conn)

print("Highest Bitcoin price:")
print(result2)
print("-" * 50)

# Query 3: Average oil price per year
query3 = """
SELECT strftime('%Y', date) AS year,
       AVG(price_usd) AS avg_oil_price
FROM oil_prices
GROUP BY year
ORDER BY year;
"""

result3 = pd.read_sql_query(query3, conn)

print("Average oil price per year:")
print(result3)
print("-" * 50)

# Query 4: Highest closing price for NASDAQ
query4 = """
SELECT MAX(close) AS highest_close
FROM stock_prices;
"""

result4 = pd.read_sql_query(query4, conn)

print("Highest NASDAQ closing price:")
print(result4)
print("-" * 50)

conn.close()