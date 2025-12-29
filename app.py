
"""
THE MOUNTAIN PATH - NIFTY PORTFOLIO ANALYZER
Advanced Portfolio Analysis Platform
Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence

Version: 1.0 (Fresh Start)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import required packages with error handling
try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:
    st.error("❌ plotly not installed")
    st.stop()

try:
    import yfinance as yf
except ImportError:
    st.error("❌ yfinance not installed")
    st.stop()

# Import custom modules
try:
    from modules.data_fetcher import NiftyDataFetcher
    from modules.portfolio_analyzer import PortfolioAnalyzer
    from modules.metrics_calculator import MetricsCalculator
    from modules.visualizations import PortfolioVisualizer
except ImportError as e:
    st.error(f"❌ Module import error: {str(e)}")
    st.stop()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Nifty Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    * {
        font-family: 'Times New Roman', serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #004d99 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-box {
        background: linear-gradient(135deg, #ADD8E6 0%, #E0F4FF 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #003366;
        margin: 10px 0;
    }
    
    .section-header {
        color: #003366;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #ADD8E6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'portfolio_a' not in st.session_state:
    st.session_state.portfolio_a = {}
    st.session_state.portfolio_b = {}
    st.session_state.nifty_stocks = []

# ============================================================================
# SIDEBAR
# ============================================================================

def setup_sidebar():
    """Setup sidebar navigation"""
    
    st.sidebar.markdown("""
    <div style="background: #003366; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h2 style="margin: 0;">📊 Portfolio Analyzer</h2>
        <p style="margin: 10px 0 0 0;">Mountain Path</p>
    </div>
    """, unsafe_allow_html=True)
    
    mode = st.sidebar.radio(
        "Select Mode",
        ["Landing Page", "Portfolio Analysis", "Single Stock Analysis"],
        label_visibility="collapsed"
    )
    
    period = st.sidebar.selectbox(
        "Data Period",
        ["1y", "3y", "5y", "10y"],
        label_visibility="collapsed"
    )
    
    risk_free_rate = st.sidebar.slider(
        "Risk-Free Rate (%)",
        min_value=1.0,
        max_value=8.0,
        value=6.5,
        step=0.1
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2024 Prof. V. Ravichandran")
    
    return mode, period, risk_free_rate / 100

# ============================================================================
# LANDING PAGE
# ============================================================================

def show_landing_page():
    """Landing page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="main-header">
            <div style="text-align: center;">
                <h1 style="margin: 0;">📊 THE MOUNTAIN PATH</h1>
                <h2 style="margin: 10px 0 0 0;">Nifty Portfolio Analyzer</h2>
                <p style="font-size: 1em;">Advanced Financial Analysis Platform</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ✨ Features
        - 📊 Portfolio Analysis (A & B)
        - 📈 Single Stock Analysis
        - 💰 25+ Financial Metrics
        - 📊 Interactive Charts
        - ⚖️ Portfolio Comparison
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Metrics
        - CAGR & Returns
        - Sharpe Ratio
        - Sortino Ratio
        - Maximum Drawdown
        - Beta & Alpha
        - And 20+ more!
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 👨‍🏫 Creator
    **Prof. V. Ravichandran**  
    28+ Years Corporate Finance & Banking  
    10+ Years Academic Excellence
    """)

# ============================================================================
# PORTFOLIO ANALYSIS
# ============================================================================

def show_portfolio_analysis(period, risk_free_rate):
    """Portfolio analysis page"""
    
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">📊 Portfolio Analysis</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Rate limit warning
    st.warning("⚠️ **Note:** Yahoo Finance rate limits NSE stocks. First analysis may take 2-5 minutes. Subsequent analyses will be faster. Please be patient!")
    
    try:
        fetcher = NiftyDataFetcher()
        nifty_stocks = fetcher.get_nifty_50_stocks()
    except Exception as e:
        st.error(f"Error loading stocks: {str(e)}")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 class='section-header'>Portfolio A</h3>", unsafe_allow_html=True)
        stocks_a = st.multiselect(
            "Select stocks for Portfolio A",
            options=nifty_stocks,
            key="stocks_a"
        )
        
        weights_a = {}
        if stocks_a:
            cols = st.columns(len(stocks_a))
            for idx, stock in enumerate(stocks_a):
                with cols[idx]:
                    weights_a[stock] = st.number_input(
                        f"{stock}",
                        min_value=0.0,
                        max_value=100.0,
                        value=100.0/len(stocks_a),
                        step=0.5,
                        key=f"weight_a_{stock}"
                    )
    
    with col2:
        st.markdown("<h3 class='section-header'>Portfolio B</h3>", unsafe_allow_html=True)
        stocks_b = st.multiselect(
            "Select stocks for Portfolio B",
            options=nifty_stocks,
            key="stocks_b"
        )
        
        weights_b = {}
        if stocks_b:
            cols = st.columns(len(stocks_b))
            for idx, stock in enumerate(stocks_b):
                with cols[idx]:
                    weights_b[stock] = st.number_input(
                        f"{stock}",
                        min_value=0.0,
                        max_value=100.0,
                        value=100.0/len(stocks_b),
                        step=0.5,
                        key=f"weight_b_{stock}"
                    )
    
    st.markdown("---")
    
    # Validation function
    def validate_weights(weights, portfolio_name):
        if not weights:
            return True, None
        total = sum(weights.values())
        if abs(total - 100) > 0.01:  # Allow small rounding errors
            return False, f"❌ {portfolio_name}: Total weight is {total:.2f}%, must be exactly 100%"
        return True, None
    
    # Show weight validation in real-time
    if stocks_a:
        total_a = sum(weights_a.values())
        if abs(total_a - 100) > 0.01:
            st.warning(f"⚠️ Portfolio A weight: {total_a:.2f}% (should be 100%)")
        else:
            st.success(f"✅ Portfolio A weight: {total_a:.2f}%")
    
    if stocks_b:
        total_b = sum(weights_b.values())
        if abs(total_b - 100) > 0.01:
            st.warning(f"⚠️ Portfolio B weight: {total_b:.2f}% (should be 100%)")
        else:
            st.success(f"✅ Portfolio B weight: {total_b:.2f}%")
    
    st.markdown("---")
    
    if st.button("🔍 Analyze Portfolios", use_container_width=True):
        # Validate before analysis
        valid_a, error_a = validate_weights(weights_a, "Portfolio A")
        valid_b, error_b = validate_weights(weights_b, "Portfolio B")
        
        if stocks_a and not valid_a:
            st.error(error_a)
            st.stop()
        if stocks_b and not valid_b:
            st.error(error_b)
            st.stop()
        
        with st.spinner("📊 Analyzing portfolios...\n⏳ If rate limited, will auto-retry with delays\n(This may take 2-5 minutes)"):
            try:
                if stocks_a and weights_a:
                    st.markdown("<h2 class='section-header'>Portfolio A</h2>", unsafe_allow_html=True)
                    try:
                        data_a = fetcher.fetch_stock_data(stocks_a, period)
                        analyzer_a = PortfolioAnalyzer(stocks_a, weights_a, data_a)
                        metrics_a = MetricsCalculator(data_a, analyzer_a, risk_free_rate).calculate_all_metrics()
                        
                        display_metrics(metrics_a)
                        
                        visualizer = PortfolioVisualizer(data_a, analyzer_a, metrics_a)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(visualizer.plot_portfolio_value(), use_container_width=True)
                        with col2:
                            st.plotly_chart(visualizer.plot_allocation(), use_container_width=True)
                        
                        st.success("✅ Portfolio A analysis complete!")
                    except Exception as e:
                        st.error(f"❌ Error analyzing Portfolio A: {str(e)}")
                
                if stocks_b and weights_b:
                    st.markdown("<h2 class='section-header'>Portfolio B</h2>", unsafe_allow_html=True)
                    try:
                        data_b = fetcher.fetch_stock_data(stocks_b, period)
                        analyzer_b = PortfolioAnalyzer(stocks_b, weights_b, data_b)
                        metrics_b = MetricsCalculator(data_b, analyzer_b, risk_free_rate).calculate_all_metrics()
                        
                        display_metrics(metrics_b)
                        
                        visualizer = PortfolioVisualizer(data_b, analyzer_b, metrics_b)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(visualizer.plot_portfolio_value(), use_container_width=True)
                        with col2:
                            st.plotly_chart(visualizer.plot_allocation(), use_container_width=True)
                        
                        st.success("✅ Portfolio B analysis complete!")
                    except Exception as e:
                        st.error(f"❌ Error analyzing Portfolio B: {str(e)}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")

def display_metrics(metrics):
    """Display metrics"""
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CAGR", f"{metrics.get('CAGR', 0)*100:.2f}%")
    with col2:
        st.metric("Total Return", f"{metrics.get('Total Return', 0)*100:.2f}%")
    with col3:
        st.metric("Volatility", f"{metrics.get('Annual Volatility', 0)*100:.2f}%")
    with col4:
        st.metric("Max Drawdown", f"{metrics.get('Max Drawdown', 0)*100:.2f}%")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sharpe Ratio", f"{metrics.get('Sharpe Ratio', 0):.3f}")
    with col2:
        st.metric("Sortino Ratio", f"{metrics.get('Sortino Ratio', 0):.3f}")
    with col3:
        st.metric("Information Ratio", f"{metrics.get('Information Ratio', 0):.3f}")
    with col4:
        st.metric("Calmar Ratio", f"{metrics.get('Calmar Ratio', 0):.3f}")

# ============================================================================
# SINGLE STOCK ANALYSIS
# ============================================================================

def show_single_stock_analysis(period, risk_free_rate):
    """Single stock analysis"""
    
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">📈 Single Stock Analysis</h1>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        fetcher = NiftyDataFetcher()
        nifty_stocks = fetcher.get_nifty_50_stocks()
        
        selected_stock = st.selectbox("Select Stock", options=nifty_stocks)
        
        if st.button("🔍 Analyze", use_container_width=True):
            with st.spinner(f"Analyzing {selected_stock}..."):
                data = fetcher.fetch_stock_data([selected_stock], period)
                analyzer = PortfolioAnalyzer([selected_stock], {selected_stock: 100}, data)
                metrics = MetricsCalculator(data, analyzer, risk_free_rate).calculate_all_metrics()
                
                display_metrics(metrics)
                
                visualizer = PortfolioVisualizer(data, analyzer, metrics)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(visualizer.plot_portfolio_value(), use_container_width=True)
                with col2:
                    st.plotly_chart(visualizer.plot_cumulative_returns(), use_container_width=True)
                
                st.success("✅ Analysis complete!")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    mode, period, risk_free_rate = setup_sidebar()
    
    if mode == "Landing Page":
        show_landing_page()
    elif mode == "Portfolio Analysis":
        show_portfolio_analysis(period, risk_free_rate)
    elif mode == "Single Stock Analysis":
        show_single_stock_analysis(period, risk_free_rate)

if __name__ == "__main__":
    main()
