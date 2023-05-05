import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import ta
import io
import csv
import plotly

tickers_cedears = ['MELI', 'BABA', 'KO', 'GOLD', 'TSLA',
                     'AAPL', 'AMD', 'VALE', 'META', 'PBR',
                     'AMZN', 'GOOGL', 'VIST', 'TX', 'MSFT',
                     'NVDA', 'WMT', 'BRK-B', 'DIS', 'JNJ',
                     'XOM', 'PG', 'TS', 'X', 'JD', 'MA', 'MCD',
                     'NFLX', 'NKE', 'NIO', 'PYPL', 'QCOM',
                     'RBLX', 'SHOP', 'SNAP', 'SPOT', 'SQ',
                     'SBUX', 'GS', 'UBER', 'V', 'GLOB', 'DE',
                     'DESP', 'EBAY', 'BIDU', 'BAC', 'ADBE',
                     'ABNB', 'ARKK', 'DIA', 'EEM', 'EWZ',
                     'IWM', 'QQQ', 'SPY', 'XLE', 'XLF']

tickers_arg_stocks = ['ALUA.BA', 'BBAR.BA', 'BMA.BA',
                    'BYMA.BA', 'CEPU.BA', 'COME.BA',
                    'CRES.BA', 'CVH.BA', 'EDN.BA',
                    'GGAL.BA', 'HARG.BA', 'LOMA.BA',
                    'MIRG.BA', 'PAMP.BA', 'SUPV.BA',
                    'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
                    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA']

tickers_crypto = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD',
                  'STETH-USD', 'DOGE-USD', 'HEX-USD', 'MATIC-USD', 'SOL-USD',
                  'DOT-USD', 'WTRX-USD', 'LTC-USD', 'SHIB-USD', 'AVAX-USD',
                  'TRX-USD', 'LINK-USD', 'HIFI-USD']

@st.cache_data()
def downloadData(dropdown, start, end):
    """Download price data for a list of tickers from Yahoo Finance.

    Args:
        dropdown (list): List of tickers.
        start (datetime): Start date.
        end (datetime): End date.

    Returns:
        DataFrame: A Pandas DataFrame with the price data.
    """

    df = yf.download(dropdown, start=start, end=end)
    return df

def normalizePrices(df):
    """Normalize price data by dividing each value by the first value in the series.

    Args:
        df (DataFrame): A Pandas DataFrame with price data.

    Returns:
        DataFrame: A Pandas DataFrame with the normalized price data.
    """
    return df.divide(df.iloc[0])

def add_indicators(df, sma_period, ema_period):
    """Add Simple Moving Average (SMA) and Exponential Moving Average (EMA) indicators to the price data.

        Args:
            df (DataFrame): A Pandas DataFrame with price data.
            sma_period (int): The period for the Simple Moving Average calculation.
            ema_period (int): The period for the Exponential Moving Average calculation.

        Returns:
            DataFrame: A Pandas DataFrame with the price data and added SMA and EMA indicators.
        """
    df['SMA'] = ta.trend.sma_indicator(df['Adj Close'], window = sma_period)
    df['EMA'] = ta.trend.ema_indicator(df['Adj Close'], window = ema_period)
    return df

def render(tickers, start, end):
    """Display normalized stock prices and percentage change for selected tickers.

        Args:
            tickers (list): List of tickers.
            start (datetime): Start date.
            end (datetime): End date.
        """
    if len(dropdown) > 0:
        df = downloadData(dropdown, start, end)
        if not df.empty:
            adj_close_df = df['Adj Close']
            st.subheader('Price by date')
            normalize_df = normalizePrices(adj_close_df)
            st.dataframe(adj_close_df, use_container_width=True)
            title = f"Normalized Stock Prices for Selected Tickers from {start} to {end}"
            fig = px.line(normalize_df, title=title)
            st.plotly_chart(fig)

            st.subheader('Percentage Change for Selected Tickers')

            for ticker in dropdown:
                if len(dropdown) == 1:
                    if not (pd.isnull(adj_close_df[-1]) or pd.isnull(adj_close_df[0])):
                        pct_change = (adj_close_df[-1] - adj_close_df[0]) / adj_close_df[0] * 100
                        st.metric(label=f"Percentage change for {ticker}", value=f"{pct_change:.2f}%", delta=None)
                    else:
                        st.write(f"Percentage change for {ticker}: Data not available")
                else:
                    if not (pd.isnull(adj_close_df[ticker][-1]) or pd.isnull(adj_close_df[ticker][0])):
                        pct_change = (adj_close_df[ticker][-1] - adj_close_df[ticker][0]) / adj_close_df[ticker][
                            0] * 100
                        st.metric(label=f"Percentage change for {ticker}", value=f"{pct_change:.2f}%", delta=None)
                    else:
                        st.write(f"Percentage change for {ticker}: Data not available")
        else:
            st.warning("No data available for the selected tickers and date range.")

def render_candlestick(tickers, start, end, indicators):
    """Display candlestick charts with SMA and EMA indicators for selected tickers.

        Args:
            tickers (list): List of tickers.
            start (datetime): Start date.
            end (datetime): End date.
            indicators (list): List of indicator names (e.g., ['SMA', 'EMA']).
        """
    for ticker in tickers:
        df = downloadData(ticker, start, end)
        if not df.empty:
            df = add_indicators(df, sma_period, ema_period)
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index,
                                                 open=df['Open'],
                                                 high=df['High'],
                                                 low=df['Low'],
                                                 close=df['Adj Close'],
                                                 name='Candlestick'))
            if 'SMA' in indicators:
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], name='SMA', line=dict(color='orange')))
            if 'EMA' in indicators:
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], name='EMA', line=dict(color='purple')))
            fig.update_layout(title=f'{ticker} Candlestick Chart with indicators (SMA & EMA)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig)
        else:
            st.warning(f"No data available for {ticker} in the selected date range.")


# MAIN APP

# Display a title and a select box in the sidebar to choose the section
st.sidebar.title("What do you want to analyze?")
section = st.sidebar.selectbox("", ["Argentinian Stocks", "CEDEARs", "Crypto"])

# Display date inputs in the sidebar to select the start and end dates for analysis
start = st.date_input('Start Date', value=pd.to_datetime('2022-01-01'), key='start')
end = st.date_input('End Date', value=pd.to_datetime('today'), key='end')

# Initialize an empty list to store the selected indicators later
indicators = []

# If the selected section is 'Argentinian Stocks'
if section == 'Argentinian Stocks':
    st.subheader('Argentinian Stocks')
    st.markdown('Results are in ARS')

    # Display a multi-select input to choose tickers
    dropdown = st.multiselect('Choose tickers', tickers_arg_stocks, key='render')

    # Call the render function to display the data and charts for the selected tickers
    render(dropdown, start, end)

    # If at least one ticker is selected, display a checkbox to show candlestick charts
    if dropdown:
        show_candlestick = st.checkbox("Show candlestick charts")
        if show_candlestick:
            # Display inputs for SMA and EMA periods
            sma_period = st.number_input('SMA period (days)', min_value=1, value=20, step=1)
            ema_period = st.number_input('EMA period (days)', min_value=1, value=20, step=1)
            indicators = ['SMA', 'EMA']

            # Call the render_candlestick function to display the candlestick charts with the selected indicators
            render_candlestick(dropdown, start, end, indicators)

if section == 'CEDEARs':
    st.subheader('CEDEARs')
    st.markdown('Results are in USD')
    dropdown = st.multiselect('Choose tickers', tickers_cedears, key='render')
    render(dropdown, start, end)
    if dropdown:
        show_candlestick = st.checkbox("Show candlestick charts")
        if show_candlestick:
            sma_period = st.number_input('SMA period (days)', min_value=1, value=20, step=1)
            ema_period = st.number_input('EMA period (days)', min_value=1, value=20, step=1)
            indicators = ['SMA', 'EMA']
            render_candlestick(dropdown, start, end, indicators)


if section == "Crypto":
    st.subheader('Crypto')
    st.markdown('Results are in USD')
    dropdown = st.multiselect('Choose tickers', tickers_crypto, key='render')
    render(dropdown, start, end)
    if dropdown:
        show_candlestick = st.checkbox("Show candlestick charts")
        if show_candlestick:
            sma_period = st.number_input('SMA period (days)', min_value=1, value=20, step=1)
            ema_period = st.number_input('EMA period (days)', min_value=1, value=20, step=1)
            indicators = ['SMA', 'EMA']
            render_candlestick(dropdown, start, end, indicators)