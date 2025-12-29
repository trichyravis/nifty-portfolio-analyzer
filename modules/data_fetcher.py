
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
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFOSYS.NS', 'ICICIBANK.NS',
        'HINDUNILVR.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS', 'LT.NS',
        'BAJAJFINSV.NS', 'AXISBANK.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'TECHM.NS',
        'WIPRO.NS', 'POWERGRID.NS', 'TITAN.NS', 'BAJAJ-AUTO.NS', 'M&M.NS',
        'GAIL.NS', 'ONGC.NS', 'EICHERMOT.NS', 'ULTRACEMCO.NS', 'ADANIPORTS.NS',
        'ASIANPAINT.NS', 'DMART.NS', 'HEROMOTOCO.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS',
        'NTPC.NS', 'HCLTECH.NS', 'DRREDDY.NS', 'INDIGO.NS', 'BPCL.NS',
        'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'GODREJCP.NS', 'INDUSTOWER.NS',
        'NATIONALUM.NS', 'NESTLEIND.NS', 'TATASTEEL.NS', 'TATAMOTORS.NS', 'UPL.NS',
        'APOLLOHOSP.NS', 'BIOCON.NS'
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
        Fetch historical stock data from Yahoo Finance
        
        Args:
            stocks (list): List of stock symbols (without .NS suffix)
            period (str): Data period ('1y', '3y', '5y', '10y')
        
        Returns:
            pd.DataFrame: Close prices for all stocks
        """
        # Add .NS suffix for Yahoo Finance
        stock_symbols = [f"{stock}.NS" if not stock.endswith('.NS') else stock for stock in stocks]
        
        try:
            # Download data
            data = yf.download(
                stock_symbols,
                period=period,
                progress=False,
                interval='1d'
            )
            
            # Handle single stock case
            if len(stock_symbols) == 1:
                # For single stock, yfinance returns a Series for 'Close'
                if isinstance(data, pd.DataFrame):
                    close_data = data['Close']
                else:
                    close_data = data
                
                # Create DataFrame with stock name
                data = pd.DataFrame({stocks[0]: close_data})
            else:
                # Extract closing prices for multiple stocks
                data = data['Close']
                # Rename columns to remove .NS suffix
                data.columns = stocks
            
            # Drop NaN values
            data = data.dropna()
            
            if data.empty:
                raise Exception(f"No valid data retrieved for {stocks}")
            
            return data
        
        except Exception as e:
            raise Exception(f"Error fetching data for {stocks}: {str(e)}")
    
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
