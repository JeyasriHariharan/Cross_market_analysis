import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Page 1 - Filters and Data Exploration", layout="wide")

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
    background-color: #fee2e2;
    color: #dc2626;
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
.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #1f2937;
    margin-top: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("cross_market.db")

st.markdown('<div class="page-badge">Page 1</div>', unsafe_allow_html=True)
st.markdown('<div class="big-title">📈 Filters and Data Exploration</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Explore Bitcoin, Oil, S&P 500, and NIFTY trends using filters and daily market snapshots.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-04-01"))
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("2026-03-01"))

query_btc_avg = f"""
SELECT AVG(price_usd) AS avg_btc_price
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND date BETWEEN '{start_date}' AND '{end_date}';
"""

query_oil_avg = f"""
SELECT AVG(price_usd) AS avg_oil_price
FROM oil_prices
WHERE date BETWEEN '{start_date}' AND '{end_date}';
"""

query_sp500_avg = f"""
SELECT AVG(close) AS avg_sp500_close
FROM stock_prices
WHERE ticker = '^GSPC'
AND date BETWEEN '{start_date}' AND '{end_date}';
"""

query_nifty_avg = f"""
SELECT AVG(close) AS avg_nifty_close
FROM stock_prices
WHERE ticker = '^NSEI'
AND date BETWEEN '{start_date}' AND '{end_date}';
"""

btc_avg = pd.read_sql_query(query_btc_avg, conn).iloc[0, 0]
oil_avg = pd.read_sql_query(query_oil_avg, conn).iloc[0, 0]
sp500_avg = pd.read_sql_query(query_sp500_avg, conn).iloc[0, 0]
nifty_avg = pd.read_sql_query(query_nifty_avg, conn).iloc[0, 0]

st.markdown('<div class="section-title">📌 Market Summary</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("🟡 Bitcoin Avg Price", f"{btc_avg:,.2f}" if pd.notna(btc_avg) else "No data")
with m2:
    st.metric("🛢 Oil Avg Price", f"{oil_avg:,.2f}" if pd.notna(oil_avg) else "No data")
with m3:
    st.metric("📊 S&P 500 Avg Close", f"{sp500_avg:,.2f}" if pd.notna(sp500_avg) else "No data")
with m4:
    st.metric("🇮🇳 NIFTY Avg Close", f"{nifty_avg:,.2f}" if pd.notna(nifty_avg) else "No data")

st.markdown('<div class="section-title">📉 Bitcoin vs Oil vs S&P 500</div>', unsafe_allow_html=True)

query_compare = f"""
SELECT c.date,
       c.price_usd AS bitcoin_price,
       o.price_usd AS oil_price,
       s.close AS sp500_price
FROM crypto_prices c
LEFT JOIN oil_prices o ON c.date = o.date
LEFT JOIN stock_prices s ON c.date = s.date AND s.ticker = '^GSPC'
WHERE c.coin_id = 'bitcoin'
AND c.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY c.date;
"""

df_compare = pd.read_sql_query(query_compare, conn)

if df_compare.empty:
    st.warning("No comparison data available.")
else:
    df_compare["date"] = pd.to_datetime(df_compare["date"])
    df_compare["bitcoin_price"] = pd.to_numeric(df_compare["bitcoin_price"], errors="coerce")
    df_compare["oil_price"] = pd.to_numeric(df_compare["oil_price"], errors="coerce")
    df_compare["sp500_price"] = pd.to_numeric(df_compare["sp500_price"], errors="coerce")
    st.line_chart(df_compare.set_index("date")[["bitcoin_price", "oil_price", "sp500_price"]])

st.markdown('<div class="section-title">📋 Daily Market Snapshot</div>', unsafe_allow_html=True)

query_snapshot = f"""
SELECT c.date,
       c.price_usd AS bitcoin_price,
       o.price_usd AS oil_price,
       s1.close AS sp500_price,
       s2.close AS nifty_price
FROM crypto_prices c
LEFT JOIN oil_prices o ON c.date = o.date
LEFT JOIN stock_prices s1 ON c.date = s1.date AND s1.ticker = '^GSPC'
LEFT JOIN stock_prices s2 ON c.date = s2.date AND s2.ticker = '^NSEI'
WHERE c.coin_id = 'bitcoin'
AND c.date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY c.date;
"""

df_snapshot = pd.read_sql_query(query_snapshot, conn)

if df_snapshot.empty:
    st.warning("No market snapshot data available.")
else:
    st.dataframe(df_snapshot, use_container_width=True)

conn.close()