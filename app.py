import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime as dt
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
    df = yf.download(dropdown, start=start, end=end)
    return df


def render(tickers, start, end):
    dropdown = st.multiselect('Choose tickers', tickers, key='render')



    if len(dropdown) > 0:
        df = downloadData(dropdown, start, end)
        if not df.empty:
            adj_close_df = df['Adj Close']
            st.subheader('Price by date')
            normalize_df = normalizePrices(adj_close_df)
            st.dataframe(adj_close_df, use_container_width=True)
            title = "Normalized Stock Prices for Selected Tickers"
            fig = px.line(normalize_df, title=title)
            st.plotly_chart(fig)

            st.subheader('Percentage Change for Selected Tickers')

            for ticker in dropdown:
                if len(dropdown) == 1:
                    if not (pd.isnull(adj_close_df[-1]) or pd.isnull(adj_close_df[0])):
                        pct_change = (adj_close_df[-1] - adj_close_df[0]) / adj_close_df[0] * 100
                        st.write(f"Percentage change for {ticker}: {pct_change:.2f}%")
                    else:
                        st.write(f"Percentage change for {ticker}: Data not available")
                else:
                    if not (pd.isnull(adj_close_df[ticker][-1]) or pd.isnull(adj_close_df[ticker][0])):
                        pct_change = (adj_close_df[ticker][-1] - adj_close_df[ticker][0]) / adj_close_df[ticker][
                            0] * 100
                        st.write(f"Percentage change for {ticker}: {pct_change:.2f}%")
                    else:
                        st.write(f"Percentage change for {ticker}: Data not available")




        else:
            st.warning("No data available for the selected tickers and date range.")

def normalizePrices(df):
    return df.divide(df.iloc[0])

def render_candlestick(tickers):
    start = st.date_input('Start Date for Candlestick Chart', value=pd.to_datetime('2022-01-01'), key='candle_start')
    end = st.date_input('End Date for Candlestick Chart', value=pd.to_datetime('today'), key='candle_end')






# MAIN APP


st.sidebar.title("What do you want to analyze?")
section = st.sidebar.selectbox("", ["Argentinian Stocks", "CEDEARs", "Crypto"])
start = st.date_input('Start Date', value=pd.to_datetime('2022-01-01'), key='start')
end = st.date_input('End Date', value=pd.to_datetime('today'), key='end')

if section == 'Argentinian Stocks':
    st.subheader('Argentinian Stocks')
    st.markdown('Results are in ARS')
    render(tickers_arg_stocks)

if section == 'CEDEARs':
    st.subheader('CEDEARs')
    st.markdown('Results are in USD')
    render(tickers_cedears)

if section == "Crypto":
    st.subheader('Crypto')
    st.markdown('Results are in USD')
    render(tickers_crypto)


