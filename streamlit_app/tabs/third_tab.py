import streamlit as st
import pandas as pd
import numpy as np
import os

from sqlalchemy import create_engine

try:
    engine = create_engine(config.DATABASE_URL)
    query = "select * from klines limit 1;"
    df = pd.read_sql(query, engine)
except Exception as e:
    print(e)
    print('Trying locally for dev')
    DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/crypto_db"
    engine = create_engine(DATABASE_URL)

title = "Data from Postgresql"
sidebar_name = title

INTERVALS = ["15m", "1h", "4h", "1d", "1w"]
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def run():

    st.title(title)

    st.markdown(
        """
        This is the data ingested in postgresql
        """
    )
    interval = st.selectbox("Choose the INTERVAL", INTERVALS)
    symbol = st.selectbox("Choose the SYMBOL", SYMBOLS)


    query = f"select count(*) from klines where interval_id=(select interval_id from intervals where interval_name='{interval}') AND symbol_id =(select symbol_id from symbol where symbol='{symbol}');"
    df = pd.read_sql(query, engine)
    st.markdown('Will display lines:')
    st.write(df.head())
    query = f"select * from klines where interval_id=(select interval_id from intervals where interval_name='{interval}') AND symbol_id =(select symbol_id from symbol where symbol='{symbol}');"
    df = pd.read_sql(query, engine)
    #st.write(pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")))
    #st.write(df.head())
        
    prices, dates = [],[]
    for index,kline in df.iterrows():
        prices.append(kline['close'])
        dates.append(kline['close_time'])
    chart_data = pd.DataFrame(prices, dates)
    st.line_chart(chart_data)
