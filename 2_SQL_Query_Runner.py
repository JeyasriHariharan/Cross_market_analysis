import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Page 2 - SQL Query Runner", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #f6f7fb;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.page-badge {
    display: inline-block;
    background-color: #dbeafe;
    color: #2563eb;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
}
.big-title {
    font-size: 38px;
    font-weight: 800;
    color: #1f2937;
}
.sub-text {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-badge">Page 2</div>', unsafe_allow_html=True)
st.markdown('<div class="big-title">🗄 SQL Query Runner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Run predefined SQL queries and view results directly from the database.</div>', unsafe_allow_html=True)

conn = sqlite3.connect("cross_market.db")

query_options = {
    "1. Top 3 cryptocurrencies by market cap": """
        SELECT id, symbol, name, market_cap, market_cap_rank
        FROM cryptocurrencies
        ORDER BY market_cap DESC
        LIMIT 3;
    """,

    "2. Coins where circulating supply exceeds 90% of total supply": """
        SELECT id, symbol, name, circulating_supply, total_supply
        FROM cryptocurrencies
        WHERE total_supply IS NOT NULL
          AND total_supply > 0
          AND circulating_supply >= 0.9 * total_supply;
    """,

    "3. Coins within 10% of ATH": """
        SELECT id, symbol, name, current_price, ath
        FROM cryptocurrencies
        WHERE ath IS NOT NULL
          AND ath > 0
          AND current_price >= 0.9 * ath;
    """,

    "4. Average market cap rank of coins with volume above 1B": """
        SELECT AVG(market_cap_rank) AS avg_market_cap_rank
        FROM cryptocurrencies
        WHERE total_volume > 1000000000;
    """,

    "5. Most recently updated coin": """
        SELECT id, symbol, name, date
        FROM cryptocurrencies
        ORDER BY date DESC
        LIMIT 1;
    """,

    "6. Highest daily price of Bitcoin in last 365 days": """
        SELECT coin_id, MAX(price_usd) AS highest_price
        FROM crypto_prices
        WHERE coin_id = 'bitcoin';
    """,

    "7. Average daily price of Ethereum in past 1 year": """
        SELECT coin_id, AVG(price_usd) AS avg_price
        FROM crypto_prices
        WHERE coin_id = 'ethereum';
    """,

    "8. Bitcoin daily price trend in January 2025": """
        SELECT date, price_usd
        FROM crypto_prices
        WHERE coin_id = 'bitcoin'
          AND date BETWEEN '2025-01-01' AND '2025-01-31'
        ORDER BY date;
    """,

    "9. Coin with highest average price over 1 year": """
        SELECT coin_id, AVG(price_usd) AS avg_price
        FROM crypto_prices
        GROUP BY coin_id
        ORDER BY avg_price DESC
        LIMIT 1;
    """,

    "10. % change in Bitcoin price between Sep 2024 and Sep 2025": """
        SELECT
            ROUND(
                (
                    (
                        SELECT AVG(price_usd)
                        FROM crypto_prices
                        WHERE coin_id = 'bitcoin'
                          AND date BETWEEN '2025-09-01' AND '2025-09-30'
                    )
                    -
                    (
                        SELECT AVG(price_usd)
                        FROM crypto_prices
                        WHERE coin_id = 'bitcoin'
                          AND date BETWEEN '2024-09-01' AND '2024-09-30'
                    )
                ) * 100.0 /
                (
                    SELECT AVG(price_usd)
                    FROM crypto_prices
                    WHERE coin_id = 'bitcoin'
                      AND date BETWEEN '2024-09-01' AND '2024-09-30'
                ),
                2
            ) AS pct_change;
    """,

    "11. Highest oil price in last 5 years": """
        SELECT MAX(price_usd) AS highest_oil_price
        FROM oil_prices
        WHERE date >= date('now', '-5 years');
    """,

    "12. Average oil price per year": """
        SELECT strftime('%Y', date) AS year,
               AVG(price_usd) AS avg_oil_price
        FROM oil_prices
        GROUP BY year
        ORDER BY year;
    """,

    "13. Oil prices during COVID crash (March-April 2020)": """
        SELECT date, price_usd
        FROM oil_prices
        WHERE date BETWEEN '2020-03-01' AND '2020-04-30'
        ORDER BY date;
    """,

    "14. Lowest oil price in last 10 years": """
        SELECT MIN(price_usd) AS lowest_oil_price
        FROM oil_prices
        WHERE date >= date('now', '-10 years');
    """,

    "15. Oil price volatility per year (max-min)": """
        SELECT strftime('%Y', date) AS year,
               MAX(price_usd) AS max_price,
               MIN(price_usd) AS min_price,
               MAX(price_usd) - MIN(price_usd) AS volatility
        FROM oil_prices
        GROUP BY year
        ORDER BY year;
    """,

    "16. All stock prices for ticker ^GSPC": """
        SELECT *
        FROM stock_prices
        WHERE ticker = '^GSPC'
        ORDER BY date;
    """,

    "17. Highest closing price for NASDAQ (^IXIC)": """
        SELECT ticker, MAX(close) AS highest_close
        FROM stock_prices
        WHERE ticker = '^IXIC';
    """,

    "18. Top 5 days with highest price difference for S&P 500 (^GSPC)": """
        SELECT date, high, low, (high - low) AS price_diff
        FROM stock_prices
        WHERE ticker = '^GSPC'
        ORDER BY price_diff DESC
        LIMIT 5;
    """,

    "19. Monthly average closing price for each ticker": """
        SELECT ticker,
               strftime('%Y-%m', date) AS month,
               AVG(close) AS avg_close
        FROM stock_prices
        GROUP BY ticker, month
        ORDER BY ticker, month;
    """,

    "20. Average trading volume of NSEI in 2024": """
        SELECT ticker, AVG(volume) AS avg_volume
        FROM stock_prices
        WHERE ticker = '^NSEI'
          AND date BETWEEN '2024-01-01' AND '2024-12-31';
    """,

    "21. Compare Bitcoin vs Oil average price in 2025": """
        SELECT
            (SELECT AVG(price_usd)
             FROM crypto_prices
             WHERE coin_id = 'bitcoin'
               AND date BETWEEN '2025-01-01' AND '2025-12-31') AS avg_bitcoin_price,
            (SELECT AVG(price_usd)
             FROM oil_prices
             WHERE date BETWEEN '2025-01-01' AND '2025-12-31') AS avg_oil_price;
    """,

    "22. Bitcoin vs S&P 500 on same dates": """
        SELECT c.date,
               c.price_usd AS bitcoin_price,
               s.close AS sp500_close
        FROM crypto_prices c
        JOIN stock_prices s
          ON c.date = s.date
        WHERE c.coin_id = 'bitcoin'
          AND s.ticker = '^GSPC'
        ORDER BY c.date;
    """,

    "23. Ethereum and NASDAQ daily prices for 2025": """
        SELECT c.date,
               c.price_usd AS ethereum_price,
               s.close AS nasdaq_close
        FROM crypto_prices c
        JOIN stock_prices s
          ON c.date = s.date
        WHERE c.coin_id = 'ethereum'
          AND s.ticker = '^IXIC'
          AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
        ORDER BY c.date;
    """,

    "24. Days when oil price spiked and Bitcoin price change": """
        SELECT o.date,
               o.price_usd AS oil_price,
               c.price_usd AS bitcoin_price,
               c.price_usd - LAG(c.price_usd) OVER (ORDER BY c.date) AS btc_price_change
        FROM oil_prices o
        JOIN crypto_prices c
          ON o.date = c.date
        WHERE c.coin_id = 'bitcoin'
        ORDER BY o.price_usd DESC
        LIMIT 20;
    """,

    "25. Top 3 coins daily trend vs NIFTY (^NSEI)": """
        SELECT c.date,
               c.coin_id,
               c.price_usd AS crypto_price,
               s.close AS nifty_close
        FROM crypto_prices c
        JOIN stock_prices s
          ON c.date = s.date
        WHERE c.coin_id IN ('bitcoin', 'ethereum', 'tether')
          AND s.ticker = '^NSEI'
        ORDER BY c.date, c.coin_id;
    """,

    "26. S&P 500 with crude oil on same dates": """
        SELECT s.date,
               s.close AS sp500_close,
               o.price_usd AS oil_price
        FROM stock_prices s
        JOIN oil_prices o
          ON s.date = o.date
        WHERE s.ticker = '^GSPC'
        ORDER BY s.date;
    """,

    "27. Bitcoin with crude oil on same dates": """
        SELECT c.date,
               c.price_usd AS bitcoin_price,
               o.price_usd AS oil_price
        FROM crypto_prices c
        JOIN oil_prices o
          ON c.date = o.date
        WHERE c.coin_id = 'bitcoin'
        ORDER BY c.date;
    """,

    "28. NASDAQ (^IXIC) with Ethereum trend": """
        SELECT s.date,
               s.close AS nasdaq_close,
               c.price_usd AS ethereum_price
        FROM stock_prices s
        JOIN crypto_prices c
          ON s.date = c.date
        WHERE s.ticker = '^IXIC'
          AND c.coin_id = 'ethereum'
        ORDER BY s.date;
    """,

    "29. Top 3 crypto coins with stock indices for 2025": """
        SELECT c.date,
               c.coin_id,
               c.price_usd,
               s.ticker,
               s.close
        FROM crypto_prices c
        JOIN stock_prices s
          ON c.date = s.date
        WHERE c.coin_id IN ('bitcoin', 'ethereum', 'tether')
          AND s.ticker IN ('^GSPC', '^IXIC', '^NSEI')
          AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
        ORDER BY c.date, c.coin_id, s.ticker;
    """,

    "30. Multi-join: stock, oil, and Bitcoin daily comparison": """
        SELECT c.date,
               c.price_usd AS bitcoin_price,
               o.price_usd AS oil_price,
               s1.close AS sp500_close,
               s2.close AS nasdaq_close,
               s3.close AS nifty_close
        FROM crypto_prices c
        LEFT JOIN oil_prices o
               ON c.date = o.date
        LEFT JOIN stock_prices s1
               ON c.date = s1.date AND s1.ticker = '^GSPC'
        LEFT JOIN stock_prices s2
               ON c.date = s2.date AND s2.ticker = '^IXIC'
        LEFT JOIN stock_prices s3
               ON c.date = s3.date AND s3.ticker = '^NSEI'
        WHERE c.coin_id = 'bitcoin'
        ORDER BY c.date;
    """
}

selected_query = st.selectbox("Choose a SQL query", list(query_options.keys()))

if st.button("▶ Run Query"):
    try:
        result_df = pd.read_sql_query(query_options[selected_query], conn)
        if result_df.empty:
            st.warning("No data returned for this query.")
        else:
            st.success("Query executed successfully.")
            st.dataframe(result_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error running query: {e}")

conn.close()