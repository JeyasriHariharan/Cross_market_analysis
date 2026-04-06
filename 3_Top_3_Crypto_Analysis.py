import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Page 3 - Top 3 Crypto Analysis", layout="wide")

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
    background-color: #ecfccb;
    color: #65a30d;
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

st.markdown('<div class="page-badge">Page 3</div>', unsafe_allow_html=True)
st.markdown('<div class="big-title">🪙 Top 3 Crypto Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Analyze daily price trends of the top 3 cryptocurrencies with filters and charts.</div>', unsafe_allow_html=True)

conn = sqlite3.connect("cross_market.db")

coin = st.selectbox("Select Coin", ["bitcoin", "ethereum", "tether"])

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2025-04-01"), key="crypto_start")
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("2026-03-01"), key="crypto_end")

st.markdown('<div class="section-title">📈 Crypto Price Trend</div>', unsafe_allow_html=True)

query = f"""
SELECT date, price_usd
FROM crypto_prices
WHERE coin_id = '{coin}'
AND date BETWEEN '{start_date}' AND '{end_date}'
ORDER BY date;
"""

df = pd.read_sql_query(query, conn)

if df.empty:
    st.warning("No data available.")
else:
    df["date"] = pd.to_datetime(df["date"])
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    st.line_chart(df.set_index("date")[["price_usd"]])

st.markdown('<div class="section-title">📋 Daily Price Table</div>', unsafe_allow_html=True)

if df.empty:
    st.warning("No table data available.")
else:
    st.dataframe(df, use_container_width=True)

conn.close()