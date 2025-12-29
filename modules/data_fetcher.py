
"""
DATA FETCHER MODULE
Handles fetching real-time stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class NiftyDataFetcher:
    """
    Fetches real-time stock data for Nifty 50 stocks from Yahoo Finance
    """
    
    # OFFICIAL Nifty 50 stocks - NSE verified tickers
    NIFTY_50 = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS', 'LT.NS',
        'BAJAJFINSV.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'TECHM.NS',
        'WIPRO.NS', 'POWERGRID.NS', 'TITAN.NS', 'BAJAJ-AUTO.NS', 'M&M.NS',
        'GAIL.NS', 'ONGC.NS', 'EICHERMOT.NS', 'ULTRACEMCO.NS', 'ADANIPORTS.NS',
        'ASIANPAINT.NS', 'DMART.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS',
        'NTPC.NS', 'HCLTECH.NS', 'DRREDDY.NS', 'INDIGO.NS', 'BPCL.NS',
        'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'GODREJCP.NS', 'INDUSTOWER.NS',
        'NATIONALUM.NS', 'NESTLEIND.NS', 'TATASTEEL.NS', 'TATAMOTORS.NS', 'UPL.NS',
        'APOLLOHOSP.NS', 'BIOCON.NS', 'INFY.NS'
    ]
    
    def __init__(self):
        """Initialize the data fetcher"""
        self.cache = {}
    
    def get_nifty_50_stocks(self):
        """
        Get list of Nifty 50 stocks
        
        Returns:
            list: Stock symbols without .NS suffix for display
        """
        return [stock.replace('.NS', '') for stock in self.NIFTY_50]
    
    def fetch_stock_data(self, stocks, period='1y'):
        """
        Fetch historical stock data from Yahoo Finance with robust rate limit handling
        
        Args:
            stocks (list): List of stock symbols (without .NS suffix)
            period (str): Data period ('1y', '3y', '5y', '10y')
        
        Returns:
            pd.DataFrame: Close prices for all stocks
        """
        import time
        
        # Add .NS suffix for Yahoo Finance
        stock_symbols = [f"{stock}.NS" if not stock.endswith('.NS') else stock for stock in stocks]
        
        try:
            # Retry logic with exponential backoff
            max_retries = 3
            base_wait = 10  # Start with 10 seconds
            
            for attempt in range(max_retries):
                try:
                    # Download data with extended timeout
                    data = yf.download(
                        stock_symbols,
                        period=period,
                        progress=False,
                        interval='1d',
                        timeout=60
                    )
                    
                    # Handle single stock case - ensure it's a DataFrame with proper index
                    if len(stock_symbols) == 1:
                        # yfinance returns different structures for single vs multiple stocks
                        if isinstance(data, pd.DataFrame) and 'Close' in data.columns:
                            # If it's already a DataFrame with Close column
                            close_data = data[['Close']].copy()
                            close_data.columns = [stocks[0]]
                        elif isinstance(data, pd.Series):
                            # If it's a Series (single column)
                            close_data = pd.DataFrame({stocks[0]: data}, index=data.index)
                        elif isinstance(data, pd.DataFrame):
                            # If it's a DataFrame without explicit Close column
                            close_data = pd.DataFrame({stocks[0]: data.iloc[:, 0]}, index=data.index)
                        else:
                            raise Exception(f"Unexpected data structure for {stocks[0]}")
                        
                        data = close_data
                    else:
                        # Multiple stocks - extract Close prices
                        if 'Close' in data.columns:
                            data = data[['Close']].copy()
                            data.columns = stocks
                        else:
                            # Fallback: assume first columns are Close
                            data = data.iloc[:, :len(stocks)].copy()
                            data.columns = stocks
                    
                    # Ensure index is DatetimeIndex
                    data.index = pd.to_datetime(data.index)
                    
                    # Drop NaN values
                    data = data.dropna()
                    
                    if data.empty:
                        raise Exception(f"No valid data retrieved for {stocks}")
                    
                    return data
                
                except Exception as e:
                    error_str = str(e).lower()
                    is_rate_limit = any(keyword in error_str for keyword in 
                                       ['rate', 'too many', 'throttle', '429', '503', 'timeout'])
                    
                    if is_rate_limit and attempt < max_retries - 1:
                        # Exponential backoff: 10s, 20s, 40s
                        wait_time = base_wait * (2 ** attempt)
                        print(f"⏳ Rate limited. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries - 1}...")
                        print(f"   Stocks: {', '.join(stock_symbols)}")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"Error fetching data for {stocks}: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Failed to fetch data for {stocks}: {str(e)}")
    
    def get_benchmark_data(self, period='1y'):
        """
        Fetch Nifty 50 benchmark data
        
        Args:
            period (str): Data period
        
        Returns:
            pd.DataFrame: Nifty 50 index close prices
        """
        try:
            data = yf.download(
                '^NSEI',  # Nifty 50 index
                period=period,
                progress=False,
                interval='1d'
            )
            
            return data[['Close']].rename(columns={'Close': 'NIFTY50'})
        
        except Exception as e:
            raise Exception(f"Error fetching benchmark data: {str(e)}")
    
    def validate_data(self, data):
        """
        Validate fetched data quality
        
        Args:
            data (pd.DataFrame): Stock price data
        
        Returns:
            bool: True if data is valid
        """
        if data.empty:
            return False
        
        # Check minimum data points
        if len(data) < 50:  # At least 50 trading days
            return False
        
        # Check for NaN values
        if data.isnull().sum().sum() > 0:
            return False
        
        return True
