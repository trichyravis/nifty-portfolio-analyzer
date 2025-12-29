
"""
THE MOUNTAIN PATH - NIFTY PORTFOLIO ANALYZER
Advanced Portfolio Analysis Platform
Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence

Version: 2.0 (Professional Design)
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
# LINKEDIN INTEGRATION FUNCTIONS
# ============================================================================

def render_linkedin_sidebar():
    """Render LinkedIn profile in sidebar - SIMPLIFIED"""
    st.sidebar.markdown("---")
    
    # Profile Card
    st.sidebar.markdown('''
    <div style="
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05));
        border-radius: 10px;
        padding: 12px;
        border-left: 3px solid #FFD700;
    ">
    <h4 style="color: #FFD700; margin: 0 0 10px 0; font-size: 13px; font-weight: 600;">
    👨‍🏫 Prof. V. Ravichandran
    </h4>
    <p style="color: #E0E0E0; margin: 4px 0; font-size: 11px;">✓ 28+ Yrs Finance</p>
    <p style="color: #E0E0E0; margin: 4px 0; font-size: 11px;">✓ 10+ Yrs Academic</p>
    <p style="color: #E0E0E0; margin: 4px 0; font-size: 11px;">✓ Risk Expert</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # LinkedIn Button
    st.sidebar.markdown(
        '<a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="'
        'display: block; background: linear-gradient(135deg, #0077B5 0%, #005885 100%); '
        'color: white !important; padding: 8px 12px; border-radius: 5px; '
        'text-decoration: none; font-weight: 600; font-size: 11px; '
        'text-align: center; width: 100%; margin-top: 8px; '
        'box-shadow: 0 2px 8px rgba(0,119,181,0.3);">'
        '🔗 LinkedIn Profile</a>',
        unsafe_allow_html=True
    )


def render_five_lens_cards():
    """Render Five-Lens Framework cards"""
    st.markdown("""
    <h3 style="text-align: center; margin-top: 30px; color: #003366;">📊 Five-Lens Framework</h3>
    """, unsafe_allow_html=True)
    
    # Framework components
    components = [
        {"title": "Valuation", "pct": "20%", "icon": "📊", "metrics": "P/E, P/B, P/S ratios"},
        {"title": "Quality", "pct": "25%", "icon": "🏆", "metrics": "ROE, ROA metrics"},
        {"title": "Growth", "pct": "20%", "icon": "📈", "metrics": "Revenue growth"},
        {"title": "Financial Health", "pct": "20%", "icon": "💰", "metrics": "D/E, Interest Coverage"},
        {"title": "Risk & Momentum", "pct": "15%", "icon": "⚡", "metrics": "Beta, Volatility"}
    ]
    
    # Create columns for cards
    cols = st.columns(5)
    
    for idx, (col, component) in enumerate(zip(cols, components)):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #003366 0%, #004d99 100%);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                color: white;
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 4px 15px rgba(0, 51, 102, 0.3);
            ">
            <div style="font-size: 40px;">{component['icon']}</div>
            <div>
                <h4 style="margin: 10px 0; font-size: 14px; font-weight: 600;">
                {component['title']}
                </h4>
                <p style="margin: 5px 0; font-size: 12px; color: #FFD700;">
                ({component['pct']})
                </p>
            </div>
            <div style="font-size: 11px; color: #E0E0E0;">
            {component['metrics']}
            </div>
            </div>
            """, unsafe_allow_html=True)


def render_professional_footer():
    """Render professional footer with buttons"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h3 style="color: #003366; margin-bottom: 10px;">
        THE MOUNTAIN PATH - WORLD OF FINANCE
        </h3>
        <p style="color: #666; margin-bottom: 20px;">
        Advanced Portfolio Analysis Platform with Financial Metrics
        </p>
        <p style="color: #003366; font-weight: 600; margin-bottom: 20px;">
        Prof. V. Ravichandran | 28+ Years Finance Experience
        </p>
        
        <div style="display: flex; justify-content: center; gap: 10px;">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="
                background: linear-gradient(135deg, #0077B5 0%, #005885 100%);
                color: white !important;
                padding: 10px 20px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                font-size: 13px;
            ">🔗 LinkedIn Profile</a>
            
            <a href="https://github.com/trichydavis/nifty-portfolio-analyzer" target="_blank" style="
                background: #333;
                color: white !important;
                padding: 10px 20px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                font-size: 13px;
            ">🐙 GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        text-align: center;
    }
    
    .section-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
    }
    
    .sidebar-header {
        background: #003366;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR SETUP
# ============================================================================

def setup_sidebar():
    """Setup sidebar navigation - Professional Design"""
    
    # Sidebar Header
    st.sidebar.markdown("""
    <div style="background: #003366; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
        <h3 style="margin: 0; font-size: 16px; font-weight: 700;">📊 PORTFOLIO ANALYZER</h3>
        <p style="margin: 8px 0 0 0; font-size: 12px;">The Mountain Path</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode Selection
    st.sidebar.markdown("<h4 style='color: #003366;'>Select Mode:</h4>", unsafe_allow_html=True)
    mode = st.sidebar.radio(
        "Mode",
        ["Landing Page", "Portfolio Analysis", "Single Stock Analysis"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Settings
    st.sidebar.markdown("<h4 style='color: #003366;'>Settings:</h4>", unsafe_allow_html=True)
    
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
    
    # LinkedIn Profile
    render_linkedin_sidebar()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2024 Prof. V. Ravichandran")
    
    return mode, period, risk_free_rate / 100

# ============================================================================
# LANDING PAGE
# ============================================================================

def show_landing_page():
    """Professional Landing Page"""
    
    # Main Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #003366 0%, #004d99 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
    ">
    <h1 style="margin: 0; font-size: 40px; font-weight: 700;">📊 THE MOUNTAIN PATH</h1>
    <h2 style="margin: 10px 0 0 0; font-size: 28px; font-weight: 600;">Nifty Portfolio Analyzer</h2>
    <p style="margin: 15px 0 0 0; font-size: 16px; color: #E0E0E0;">
    Advanced Financial Analysis Platform
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✨ Core Features
        
        - 📊 **Portfolio Analysis** (A & B Comparison)
        - 📈 **Single Stock Analysis** 
        - 💰 **25+ Financial Metrics**
        - 📊 **Interactive Charts & Visualizations**
        - ⚖️ **Portfolio Comparison & Risk Assessment**
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Key Metrics
        
        - **Returns:** CAGR, Total Return, Annual/Monthly Return
        - **Risk:** Volatility, Max Drawdown, VaR
        - **Risk-Adjusted:** Sharpe Ratio, Sortino Ratio
        - **Advanced:** Beta, Alpha, Calmar Ratio
        - **And 15+ More Metrics!**
        """)
    
    st.markdown("---")
    
    # Framework Display
    render_five_lens_cards()
    
    st.markdown("---")
    
    # About Creator
    st.markdown("""
    ### 👨‍🏫 Creator
    
    **Prof. V. Ravichandran**
    
    28+ Years Corporate Finance & Banking Experience  
    10+ Years Academic Excellence  
    Expert in Financial Risk Management & Derivatives
    """)
    
    # Professional Footer
    render_professional_footer()

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
    
    try:
        fetcher = NiftyDataFetcher()
        nifty_stocks = fetcher.get_nifty_50_stocks()
        
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
            if abs(total - 100) > 0.01:
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
            valid_a, error_a = validate_weights(weights_a, "Portfolio A")
            valid_b, error_b = validate_weights(weights_b, "Portfolio B")
            
            if stocks_a and not valid_a:
                st.error(error_a)
                st.stop()
            if stocks_b and not valid_b:
                st.error(error_b)
                st.stop()
            
            with st.spinner("📊 Analyzing portfolios...\n⏳ If rate limited, will auto-retry\n(This may take 2-5 minutes)"):
                try:
                    if stocks_a and weights_a:
                        st.markdown("<h2 class='section-header'>Portfolio A</h2>", unsafe_allow_html=True)
                        try:
                            data_a = fetcher.fetch_stock_data(stocks_a, period)
                            
                            if data_a.empty:
                                st.error(f"❌ No data available for {', '.join(stocks_a)}")
                            else:
                                analyzer_a = PortfolioAnalyzer(stocks_a, weights_a, data_a)
                                metrics_a = MetricsCalculator(data_a, analyzer_a, risk_free_rate).calculate_all_metrics()
                                
                                display_metrics(metrics_a)
                                
                                visualizer = PortfolioVisualizer(data_a, analyzer_a, metrics_a)
                                col1, col2 = st.columns(2)
                                with col1:
                                    try:
                                        st.plotly_chart(visualizer.plot_portfolio_value(), use_container_width=True)
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                with col2:
                                    try:
                                        st.plotly_chart(visualizer.plot_allocation(), use_container_width=True)
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                st.success("✅ Portfolio A analysis complete!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    
                    if stocks_b and weights_b:
                        st.markdown("<h2 class='section-header'>Portfolio B</h2>", unsafe_allow_html=True)
                        try:
                            data_b = fetcher.fetch_stock_data(stocks_b, period)
                            
                            if data_b.empty:
                                st.error(f"❌ No data available for {', '.join(stocks_b)}")
                            else:
                                analyzer_b = PortfolioAnalyzer(stocks_b, weights_b, data_b)
                                metrics_b = MetricsCalculator(data_b, analyzer_b, risk_free_rate).calculate_all_metrics()
                                
                                display_metrics(metrics_b)
                                
                                visualizer = PortfolioVisualizer(data_b, analyzer_b, metrics_b)
                                col1, col2 = st.columns(2)
                                with col1:
                                    try:
                                        st.plotly_chart(visualizer.plot_portfolio_value(), use_container_width=True)
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                with col2:
                                    try:
                                        st.plotly_chart(visualizer.plot_allocation(), use_container_width=True)
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                st.success("✅ Portfolio B analysis complete!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

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
