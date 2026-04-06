import streamlit as st

st.set_page_config(
    page_title="Cross-Market Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #f6f7fb;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.big-title {
    font-size: 44px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 0.3rem;
}
.sub-title {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📊 Cross-Market Analysis: Crypto, Oil & Stocks</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SQL-powered financial analytics dashboard</div>', unsafe_allow_html=True)

st.write("Welcome to the dashboard.")
st.markdown("""
- **Page 1:** Filters and Data Exploration  
- **Page 2:** SQL Query Runner  
- **Page 3:** Top 3 Crypto Analysis
""")