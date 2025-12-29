
"""
THE MOUNTAIN PATH - NIFTY PORTFOLIO ANALYZER
Advanced Portfolio Analysis Platform
Prof. V. Ravichandran | 28+ Years Finance Experience | 10+ Years Academic Excellence

Version: 3.0 (Professional Sidebar & Footer)
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

# Custom CSS - Enhanced Design
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
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
    }
    
    /* Comprehensive radio button styling */
    /* Target all text in Streamlit radio */
    [role="radiogroup"] {
        color: #8B0000 !important;
    }
    
    [role="radiogroup"] label {
        color: #8B0000 !important;
        font-weight: 700 !important;
    }
    
    [role="radiogroup"] p,
    [role="radiogroup"] span {
        color: #8B0000 !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar specific styling */
    .stSidebar [role="radiogroup"] label,
    .stSidebar [role="radiogroup"] span,
    .stSidebar [role="radiogroup"] p {
        color: #8B0000 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* Target the entire radio group */
    .stRadio {
        color: #8B0000 !important;
    }
    
    .stRadio label span,
    .stRadio label p {
        color: #8B0000 !important;
        font-weight: 700 !important;
    }
    
    /* Force dark red on all text inside radio */
    [role="radiogroup"] {
        --text-color: #8B0000;
    }
    
    [role="radiogroup"] * {
        color: #8B0000 !important;
        font-weight: 700 !important;
    }
    
    /* Style the buttons in sidebar */
    .stSidebar button {
        color: #8B0000 !important;
        font-weight: 700 !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER FUNCTIONS
# ============================================================================

def render_professional_footer():
    """Render professional footer with disclaimer and buttons"""
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 20px;">
    <h3 style="color: #003366; margin: 0 0 15px 0; font-size: 18px; font-weight: 700; letter-spacing: 1px;">
    THE MOUNTAIN PATH - WORLD OF FINANCE
    </h3>
    <p style="color: #555; margin: 0 0 15px 0; font-size: 14px;">
    Advanced Portfolio Analysis Platform with Financial Metrics
    </p>
    <p style="color: #003366; font-weight: 600; margin: 0 0 20px 0;">
    Prof. V. Ravichandran | 28+ Years Finance Experience
    </p>
    <div style="display: flex; justify-content: center; gap: 12px; margin-bottom: 25px; flex-wrap: wrap;">
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="
            background: #0077B5 !important;
            color: #FFFFFF !important;
            padding: 14px 28px !important;
            border-radius: 6px !important;
            text-decoration: none !important;
            font-weight: 900 !important;
            font-size: 15px !important;
            box-shadow: 0 4px 12px rgba(0, 119, 181, 0.7) !important;
            border: none !important;
            cursor: pointer !important;
            display: inline-block !important;
            line-height: 1.2 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
        ">🔗 LinkedIn Profile</a>
        <a href="https://github.com/trichyravis/nifty-portfolio-analyzer" target="_blank" style="
            background: #333 !important;
            color: #FFFFFF !important;
            padding: 14px 28px !important;
            border-radius: 6px !important;
            text-decoration: none !important;
            font-weight: 900 !important;
            font-size: 15px !important;
            box-shadow: 0 4px 12px rgba(51, 51, 51, 0.7) !important;
            border: none !important;
            cursor: pointer !important;
            display: inline-block !important;
            line-height: 1.2 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
        ">🐙 GitHub</a>
    </div>
    <p style="color: #666; font-size: 12px; margin: 0 0 10px 0; line-height: 1.6;">
    <strong>Disclaimer:</strong> This tool is for educational purposes. Not financial advice. 
    Always consult with a qualified financial advisor before making investment decisions.
    </p>
    <p style="color: #999; font-size: 11px; margin: 0;">
    📊 Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SIDEBAR SETUP
# ============================================================================

def setup_sidebar():
    """Setup professional sidebar navigation with dark blue background"""
    
    # Professional Dark Blue Sidebar Header
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #003366 0%, #004d99 100%); color: white; padding: 20px 15px; border-radius: 8px; margin-bottom: 20px; text-align: left;">
        <h1 style="margin: 0; font-size: 18px; font-weight: 700;">📊 PORTFOLIO ANALYZER</h1>
        <p style="margin: 8px 0 0 0; font-size: 12px; color: #E0E0E0; font-weight: 500;">Advanced Financial Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode Selection Section
    st.sidebar.markdown("<h4 style='color: white; background: #003366; padding: 10px; margin: 0 -16px 10px -16px; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Select Mode:</h4>", unsafe_allow_html=True)
    
    # Add CSS for styled mode buttons
    st.sidebar.markdown("""
    <style>
        .mode-button-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin: 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create custom mode buttons with session state
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Home"
    
    modes = ["Home", "Portfolio Analysis", "Single Stock Analysis", "Learn Metrics"]
    cols = st.sidebar.columns(1)
    
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 10px;">
        """, unsafe_allow_html=True)
        
        for mode_option in modes:
            is_active = st.session_state.app_mode == mode_option
            button_color = "#8B0000" if is_active else "#E0E0E0"
            bg_color = "#8B0000" if is_active else "white"
            text_color = "white" if is_active else "#8B0000"
            border_color = "#8B0000"
            
            if st.button(
                f"🔴 {mode_option}" if is_active else f"○ {mode_option}",
                use_container_width=True,
                key=f"mode_btn_{mode_option}",
                help=f"Switch to {mode_option}"
            ):
                st.session_state.app_mode = mode_option
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Use the session state mode
    mode = st.session_state.app_mode
    
    # Settings Section
    st.sidebar.markdown("<h4 style='color: white; background: #003366; padding: 10px; margin: 10px -16px 10px -16px; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Settings:</h4>", unsafe_allow_html=True)
    
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
    
    # Creator Section
    st.sidebar.markdown("""
    <div style="background: #003366; color: white; padding: 15px; border-radius: 6px; text-align: center;">
        <h4 style="color: white; margin: 0 0 8px 0; font-size: 13px; font-weight: 600;">Prof. V. Ravichandran</h4>
        <p style="color: #E0E0E0; font-size: 11px; margin: 4px 0; line-height: 1.5;">28+ Years Finance Experience</p>
        <p style="color: #E0E0E0; font-size: 11px; margin: 4px 0 12px 0; line-height: 1.5;">10+ Years Academic Excellence</p>
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="display: inline-block; background: #0077B5; color: #FFFFFF !important; padding: 12px 20px; border-radius: 5px; text-decoration: none !important; font-weight: 900 !important; font-size: 14px !important; box-shadow: 0 4px 12px rgba(0, 119, 181, 0.7); line-height: 1.2; border: none; cursor: pointer; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">🔗 LinkedIn Profile</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2024 Prof. V. Ravichandran")
    
    return mode, period, risk_free_rate / 100

# ============================================================================
# LANDING PAGE
# ============================================================================

def show_landing_page():
    """Professional Home Page"""
    
    # Main Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #003366 0%, #004d99 100%);
        padding: 50px;
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
        - 📚 **Learn Metrics** (Educational Guide)
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
        
        # Initialize tracking for portfolio A
        if 'last_stocks_a_count' not in st.session_state:
            st.session_state.last_stocks_a_count = 0
        if 'last_stocks_b_count' not in st.session_state:
            st.session_state.last_stocks_b_count = 0
        
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
                num_stocks_a = len(stocks_a)
                equal_weight_a = 100.0 / num_stocks_a
                
                # Reset weights if number of stocks changed
                if num_stocks_a != st.session_state.last_stocks_a_count:
                    # Clear old weights
                    keys_to_delete = [k for k in st.session_state.keys() if k.startswith("weight_a_")]
                    for k in keys_to_delete:
                        del st.session_state[k]
                    
                    # Initialize new weights
                    for stock in stocks_a:
                        st.session_state[f"weight_a_{stock}"] = equal_weight_a
                    
                    st.session_state.last_stocks_a_count = num_stocks_a
                
                # Display info
                st.info(f"📊 {num_stocks_a} stocks selected → Equal weight: {equal_weight_a:.2f}% each")
                
                # Display weight inputs
                cols = st.columns(num_stocks_a)
                for idx, stock in enumerate(stocks_a):
                    with cols[idx]:
                        weight_key = f"weight_a_{stock}"
                        # Get value from session state
                        current_value = st.session_state.get(weight_key, equal_weight_a)
                        weights_a[stock] = st.number_input(
                            f"{stock}",
                            min_value=0.0,
                            max_value=100.0,
                            value=current_value,
                            step=0.1,
                            key=weight_key,
                            format="%.2f"
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
                num_stocks_b = len(stocks_b)
                equal_weight_b = 100.0 / num_stocks_b
                
                # Reset weights if number of stocks changed
                if num_stocks_b != st.session_state.last_stocks_b_count:
                    # Clear old weights
                    keys_to_delete = [k for k in st.session_state.keys() if k.startswith("weight_b_")]
                    for k in keys_to_delete:
                        del st.session_state[k]
                    
                    # Initialize new weights
                    for stock in stocks_b:
                        st.session_state[f"weight_b_{stock}"] = equal_weight_b
                    
                    st.session_state.last_stocks_b_count = num_stocks_b
                
                # Display info
                st.info(f"📊 {num_stocks_b} stocks selected → Equal weight: {equal_weight_b:.2f}% each")
                
                # Display weight inputs
                cols = st.columns(num_stocks_b)
                for idx, stock in enumerate(stocks_b):
                    with cols[idx]:
                        weight_key = f"weight_b_{stock}"
                        # Get value from session state
                        current_value = st.session_state.get(weight_key, equal_weight_b)
                        weights_b[stock] = st.number_input(
                            f"{stock}",
                            min_value=0.0,
                            max_value=100.0,
                            value=current_value,
                            step=0.1,
                            key=weight_key,
                            format="%.2f"
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
        val_col1, val_col2 = st.columns(2)
        
        with val_col1:
            if stocks_a:
                total_a = sum(weights_a.values())
                if abs(total_a - 100) > 0.01:
                    st.warning(f"⚠️ Portfolio A weight: {total_a:.2f}% (should be 100%)")
                else:
                    st.success(f"✅ Portfolio A weight: {total_a:.2f}%")
        
        with val_col2:
            if stocks_b:
                total_b = sum(weights_b.values())
                if abs(total_b - 100) > 0.01:
                    st.warning(f"⚠️ Portfolio B weight: {total_b:.2f}% (should be 100%)")
                else:
                    st.success(f"✅ Portfolio B weight: {total_b:.2f}%")
        
        st.markdown("---")
        
        if st.button("🔍 Analyze Portfolios", use_container_width=True, key="analyze_portfolios"):
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
                                        st.plotly_chart(visualizer.plot_portfolio_value(chart_id="portfolio_a_value"), use_container_width=True, key="portfolio_a_value")
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                with col2:
                                    try:
                                        st.plotly_chart(visualizer.plot_allocation(chart_id="portfolio_a_allocation"), use_container_width=True, key="portfolio_a_allocation")
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
                                        st.plotly_chart(visualizer.plot_portfolio_value(chart_id="portfolio_b_value"), use_container_width=True, key="portfolio_b_value")
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                with col2:
                                    try:
                                        st.plotly_chart(visualizer.plot_allocation(chart_id="portfolio_b_allocation"), use_container_width=True, key="portfolio_b_allocation")
                                    except Exception as e:
                                        st.warning(f"⚠️ Chart error: {str(e)}")
                                
                                st.success("✅ Portfolio B analysis complete!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    
                    # Portfolio Comparison Analysis
                    if stocks_a and weights_a and stocks_b and weights_b:
                        try:
                            st.markdown("---")
                            st.markdown("<h2 class='section-header'>📊 Portfolio Comparison Analysis</h2>", unsafe_allow_html=True)
                            
                            # Create comparison dataframe
                            comparison_data = {
                                'Metric': [
                                    'CAGR',
                                    'Total Return',
                                    'Annual Volatility',
                                    'Sharpe Ratio',
                                    'Sortino Ratio',
                                    'Information Ratio',
                                    'Calmar Ratio',
                                    'Max Drawdown',
                                    'Value at Risk (VaR)',
                                    'Skewness'
                                ],
                                'Portfolio A': [
                                    f"{metrics_a.get('CAGR', 0)*100:.2f}%",
                                    f"{metrics_a.get('Total Return', 0)*100:.2f}%",
                                    f"{metrics_a.get('Annual Volatility', 0)*100:.2f}%",
                                    f"{metrics_a.get('Sharpe Ratio', 0):.3f}",
                                    f"{metrics_a.get('Sortino Ratio', 0):.3f}",
                                    f"{metrics_a.get('Information Ratio', 0):.3f}",
                                    f"{metrics_a.get('Calmar Ratio', 0):.3f}",
                                    f"{metrics_a.get('Max Drawdown', 0)*100:.2f}%",
                                    f"{metrics_a.get('Value at Risk', 0)*100:.2f}%",
                                    f"{metrics_a.get('Skewness', 0):.3f}"
                                ],
                                'Portfolio B': [
                                    f"{metrics_b.get('CAGR', 0)*100:.2f}%",
                                    f"{metrics_b.get('Total Return', 0)*100:.2f}%",
                                    f"{metrics_b.get('Annual Volatility', 0)*100:.2f}%",
                                    f"{metrics_b.get('Sharpe Ratio', 0):.3f}",
                                    f"{metrics_b.get('Sortino Ratio', 0):.3f}",
                                    f"{metrics_b.get('Information Ratio', 0):.3f}",
                                    f"{metrics_b.get('Calmar Ratio', 0):.3f}",
                                    f"{metrics_b.get('Max Drawdown', 0)*100:.2f}%",
                                    f"{metrics_b.get('Value at Risk', 0)*100:.2f}%",
                                    f"{metrics_b.get('Skewness', 0):.3f}"
                                ]
                            }
                            
                            comparison_df = pd.DataFrame(comparison_data)
                            st.subheader("📈 Metrics Comparison")
                            st.dataframe(comparison_df, use_container_width=True)
                            
                            # Quick comparison
                            st.subheader("📋 Quick Analysis")
                            cagr_a = metrics_a.get('CAGR', 0)
                            cagr_b = metrics_b.get('CAGR', 0)
                            sharpe_a = metrics_a.get('Sharpe Ratio', 0)
                            sharpe_b = metrics_b.get('Sharpe Ratio', 0)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"""
                                **Portfolio A**
                                - CAGR: {cagr_a*100:.2f}%
                                - Sharpe: {sharpe_a:.3f}
                                """)
                            
                            with col2:
                                st.markdown(f"""
                                **Portfolio B**
                                - CAGR: {cagr_b*100:.2f}%
                                - Sharpe: {sharpe_b:.3f}
                                """)
                            
                            # Winner determination
                            if cagr_a > cagr_b and sharpe_a > sharpe_b:
                                st.success("✅ Portfolio A: Better on both growth and risk-adjusted returns")
                            elif cagr_b > cagr_a and sharpe_b > sharpe_a:
                                st.success("✅ Portfolio B: Better on both growth and risk-adjusted returns")
                            elif cagr_a > cagr_b:
                                st.info("📊 Portfolio A: Higher returns (but check volatility)")
                            elif cagr_b > cagr_a:
                                st.info("📊 Portfolio B: Higher returns (but check volatility)")
                            else:
                                st.info("⚖️ Comparable performance - choose based on your preference")
                        
                        except Exception as e:
                            st.error(f"❌ Comparison error: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Analysis Error: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

def display_metrics(metrics):
    """Display metrics"""
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CAGR", f"{metrics.get('CAGR', 0)*100:.2f}%")
    with col2:
        st.metric("Annual Return", f"{metrics.get('Annual Return', 0)*100:.2f}%")
    with col3:
        st.metric("Volatility", f"{metrics.get('Annual Volatility', 0)*100:.2f}%")
    with col4:
        st.metric("Sharpe Ratio", f"{metrics.get('Sharpe Ratio', 0):.3f}")
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Sortino Ratio", f"{metrics.get('Sortino Ratio', 0):.3f}")
    with col6:
        st.metric("Max Drawdown", f"{metrics.get('Max Drawdown', 0)*100:.2f}%")
    with col7:
        st.metric("Calmar Ratio", f"{metrics.get('Calmar Ratio', 0):.3f}")
    with col8:
        st.metric("Information Ratio", f"{metrics.get('Information Ratio', 0):.3f}")

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
        
        if st.button("🔍 Analyze", use_container_width=True, key="analyze_single_stock"):
            with st.spinner(f"Analyzing {selected_stock}..."):
                data = fetcher.fetch_stock_data([selected_stock], period)
                analyzer = PortfolioAnalyzer([selected_stock], {selected_stock: 100}, data)
                metrics = MetricsCalculator(data, analyzer, risk_free_rate).calculate_all_metrics()
                
                display_metrics(metrics)
                
                visualizer = PortfolioVisualizer(data, analyzer, metrics)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(visualizer.plot_portfolio_value(chart_id=f"single_stock_{selected_stock}_value"), use_container_width=True, key=f"single_stock_{selected_stock}_value")
                with col2:
                    st.plotly_chart(visualizer.plot_cumulative_returns(chart_id=f"single_stock_{selected_stock}_returns"), use_container_width=True, key=f"single_stock_{selected_stock}_returns")
                
                st.success("✅ Analysis complete!")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================================================
# METRICS EDUCATION
# ============================================================================

def show_metrics_education():
    """Show educational content about financial metrics"""
    
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0;">📚 Learn Financial Metrics</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size: 16px; color: #666; margin-top: 10px;">
    Understand the key metrics used in portfolio analysis. Click on any metric to expand and learn more.
    </p>
    """, unsafe_allow_html=True)
    
    # Create expandable sections for each metric
    with st.expander("📈 **CAGR (Compound Annual Growth Rate)**", expanded=False):
        st.markdown("""
        **What It Is:**
        CAGR represents the average annual return of an investment over a specific period, assuming profits are reinvested.
        
        **Formula:**
        ```
        CAGR = (Ending Value / Beginning Value)^(1/Number of Years) - 1
        ```
        
        **Example:**
        - Investment: ₹100 → ₹400 over 10 years
        - CAGR = (400/100)^(1/10) - 1 = 14.87% per year
        
        **What's Good?**
        - 0-5%: Conservative
        - 5-10%: Moderate
        - 10-15%: Good
        - 15%+: Excellent
        
        **Why It Matters:**
        Helps you understand long-term investment growth, accounting for compounding effects.
        """)
    
    with st.expander("📊 **Total Return**", expanded=False):
        st.markdown("""
        **What It Is:**
        The total profit or loss from your investment over the entire analysis period, expressed as a percentage.
        
        **Formula:**
        ```
        Total Return = (Ending Value - Beginning Value) / Beginning Value × 100%
        ```
        
        **Example:**
        - Invested: ₹100,000
        - Current Value: ₹148,600
        - Total Return = (148,600 - 100,000) / 100,000 × 100% = 48.6%
        
        **What's Good?**
        - Positive return: Profit ✅
        - 20-50% over 5 years: Good
        - 50%+: Excellent
        
        **Why It Matters:**
        Shows your actual profit or loss in simple percentage terms.
        """)
    
    with st.expander("📉 **Annual Volatility (Standard Deviation)**", expanded=False):
        st.markdown("""
        **What It Is:**
        Measures how much your portfolio's returns fluctuate day-to-day. Higher volatility = more unpredictable.
        
        **Interpretation:**
        - Shows the "risk" of your investment
        - Calculated from daily return variations
        - Annualized to show yearly risk
        
        **Example:**
        - 15% volatility: Daily returns vary slightly, stable investment
        - 30% volatility: Large daily swings, risky investment
        
        **What's Good?**
        - 10-15%: Low risk, stable returns
        - 15-20%: Moderate risk
        - 20-30%: Higher risk
        - 30%+: Very high risk
        
        **Why It Matters:**
        Helps you understand how much your portfolio value will bounce around.
        """)
    
    with st.expander("⚖️ **Sharpe Ratio**", expanded=False):
        st.markdown("""
        **What It Is:**
        Measures how much return you get for each unit of risk taken. Higher = better!
        
        **Formula:**
        ```
        Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Volatility
        ```
        
        **Interpretation:**
        - How efficiently your portfolio uses risk to generate returns
        - Compares return to risk taken
        
        **What's Good?**
        - < 0: Losing money
        - 0 - 0.5: Poor
        - 0.5 - 1.0: Acceptable
        - 1.0 - 2.0: Excellent ⭐
        - 2.0+: Outstanding ⭐⭐
        
        **Example:**
        - Portfolio A: 0.8 Sharpe = Good efficiency
        - Portfolio B: 0.5 Sharpe = Average efficiency
        - Choose Portfolio A
        
        **Why It Matters:**
        Helps compare portfolios fairly by considering both return and risk.
        """)
    
    with st.expander("🎯 **Sortino Ratio**", expanded=False):
        st.markdown("""
        **What It Is:**
        Similar to Sharpe Ratio, but only considers "downside" risk (negative returns).
        Ignores positive volatility, focusing on actual losses.
        
        **Formula:**
        ```
        Sortino Ratio = (Portfolio Return - Risk-Free Rate) / Downside Deviation
        ```
        
        **Why Different from Sharpe?**
        - Sharpe: Considers all volatility (both up and down)
        - Sortino: Only considers downside volatility (losses)
        - More practical for risk-averse investors
        
        **What's Good?**
        - > 1.0: Good downside protection
        - > 2.0: Excellent downside protection
        - > 3.0: Outstanding
        
        **Why It Matters:**
        Better measure for investors who care more about avoiding losses than celebrating gains.
        """)
    
    with st.expander("🏆 **Information Ratio**", expanded=False):
        st.markdown("""
        **What It Is:**
        Measures how much your portfolio outperforms a benchmark (like Nifty 50), adjusted for risk.
        
        **Formula:**
        ```
        Information Ratio = (Portfolio Return - Benchmark Return) / Tracking Error
        ```
        
        **Interpretation:**
        - Shows how well you beat the market
        - Positive = beating the benchmark
        - Negative = underperforming
        
        **What's Good?**
        - > 0: Beating the benchmark ✅
        - 0.5: Good outperformance
        - > 1.0: Excellent outperformance ⭐
        
        **Why It Matters:**
        Helps you see if your stock-picking skill is adding value beyond just buying the index.
        """)
    
    with st.expander("🎪 **Calmar Ratio**", expanded=False):
        st.markdown("""
        **What It Is:**
        Measures return per unit of maximum drawdown. Shows recovery capability.
        
        **Formula:**
        ```
        Calmar Ratio = Annual Return / Absolute Value of Max Drawdown
        ```
        
        **Example:**
        - Annual Return: 15%
        - Max Drawdown: -20%
        - Calmar = 15 / 20 = 0.75
        
        **What's Good?**
        - > 1.0: Good recovery capability ✅
        - > 2.0: Excellent recovery ⭐
        - > 3.0: Outstanding ⭐⭐
        
        **Why It Matters:**
        Shows how well your portfolio recovers from bad periods.
        """)
    
    with st.expander("📉 **Maximum Drawdown**", expanded=False):
        st.markdown("""
        **What It Is:**
        The largest peak-to-trough decline. Your worst-case loss scenario.
        
        **Example:**
        - Peak Value: ₹100,000
        - Trough Value: ₹80,000 (worst point)
        - Max Drawdown = -20%
        
        **Interpretation:**
        - How much you lost at the absolute worst time
        - Historical worst-case loss
        
        **What's Good?**
        - 0 to -10%: Low risk ✅
        - -10% to -20%: Moderate risk
        - -20% to -30%: Higher risk
        - Below -30%: Very risky
        
        **Real World:**
        - 2008 Market Crash: -57% drawdown
        - Average Market: -20% to -30%
        - Conservative Portfolio: -10% to -15%
        
        **Why It Matters:**
        Prepares you mentally for the worst case. "Can I handle a -20% loss?"
        """)
    
    with st.expander("⚠️ **Value at Risk (VaR)**", expanded=False):
        st.markdown("""
        **What It Is:**
        Statistical estimate of maximum loss you might face on 95% of trading days.
        The 5% worst-case loss.
        
        **Example:**
        - Daily VaR: -1.5%
        - Meaning: On 95% of days, you lose less than 1.5%
        - On 5% of days, you might lose more
        
        **Interpretation:**
        - Shows typical daily risk
        - Used in risk management
        
        **What's Good?**
        - -1% to -2%: Low risk ✅
        - -2% to -3%: Moderate risk
        - Below -3%: Higher risk
        
        **Why It Matters:**
        Gives you a statistical edge of daily losses. Helps with position sizing.
        """)
    
    with st.expander("📊 **Skewness**", expanded=False):
        st.markdown("""
        **What It Is:**
        Measures the shape of return distribution. Are returns symmetric or skewed?
        
        **Interpretation:**
        - Positive Skew: More big wins than big losses (GOOD) 😊
        - Zero Skew: Symmetric wins and losses
        - Negative Skew: More big losses than big wins (BAD) 😞
        
        **Example:**
        - Skew = +0.5: Good! More upside surprises
        - Skew = -0.5: Bad! More downside surprises
        - Skew = 0: Neutral
        
        **What's Good?**
        - > 0: Positive skewness (more wins) ✅
        - > 1.0: Strong positive skewness ⭐
        - < 0: Avoid (more losses)
        
        **Why It Matters:**
        Shows if your portfolio tends to have pleasant or unpleasant surprises.
        """)
    
    # Quick Reference Table
    st.markdown("---")
    st.markdown("<h2 class='section-header'>📋 Quick Reference Guide</h2>", unsafe_allow_html=True)
    
    metrics_table = """
    | Metric | What It Measures | Better Value | Key Points |
    |--------|------------------|--------------|-----------|
    | **CAGR** | Avg annual growth | Higher | Main return metric |
    | **Total Return** | Overall profit/loss | Higher | Simple percentage |
    | **Volatility** | Risk/fluctuation | Lower | More stable is safer |
    | **Sharpe Ratio** | Return per risk unit | Higher (>1 good) | Efficiency metric |
    | **Sortino Ratio** | Return per downside risk | Higher (>1 good) | Focus on losses only |
    | **Information Ratio** | Outperformance vs benchmark | Higher (>0.5 good) | Beat the market? |
    | **Calmar Ratio** | Return per max drawdown | Higher (>1 good) | Recovery ability |
    | **Max Drawdown** | Worst-case loss | Higher/less negative | Prepare for worst |
    | **Value at Risk** | 95% daily loss limit | Higher/less negative | Statistical risk |
    | **Skewness** | Return distribution shape | Positive | More wins than losses |
    """
    
    st.markdown(metrics_table)
    
    # Best Practices
    st.markdown("---")
    st.markdown("<h2 class='section-header'>🎯 How to Use These Metrics</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ For Conservative Investors
        - Focus: **Low Volatility, High Sharpe**
        - Check: Max Drawdown (should be small)
        - Goal: Steady returns with low risk
        
        ### ✅ For Growth Investors
        - Focus: **High CAGR, Good Sharpe**
        - Check: Sortino Ratio (downside protection)
        - Goal: Maximum returns with acceptable risk
        """)
    
    with col2:
        st.markdown("""
        ### ✅ When Comparing Portfolios
        1. Look at CAGR first (returns)
        2. Check Volatility (risk)
        3. Compare Sharpe Ratio (efficiency)
        4. Verify Max Drawdown (worst case)
        5. Consider Information Ratio (skill)
        
        ### ✅ Red Flags
        - ❌ High returns + High volatility
        - ❌ Negative Information Ratio
        - ❌ Very large Max Drawdown
        - ❌ Negative Skewness
        """)
    
    # Key Takeaways
    st.markdown("---")
    st.markdown("<h2 class='section-header'>🌟 Key Takeaways</h2>", unsafe_allow_html=True)
    
    st.success("""
    ✅ **CAGR** tells you average yearly growth
    
    ✅ **Volatility** tells you how bumpy the ride is
    
    ✅ **Sharpe Ratio** tells you if return compensates for risk
    
    ✅ **Max Drawdown** tells you the worst-case loss to prepare for
    
    ✅ **Information Ratio** tells you if you're beating the market
    
    ✅ **Calmar Ratio** tells you how well you recover from losses
    
    ✅ Use multiple metrics together for complete picture!
    """)

# ============================================================================
# MAIN
# ============================================================================

def main():
    mode, period, risk_free_rate = setup_sidebar()
    
    if mode == "Home":
        show_landing_page()
    elif mode == "Portfolio Analysis":
        show_portfolio_analysis(period, risk_free_rate)
    elif mode == "Single Stock Analysis":
        show_single_stock_analysis(period, risk_free_rate)
    elif mode == "Learn Metrics":
        show_metrics_education()

if __name__ == "__main__":
    main()
