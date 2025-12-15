import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from pymongo import MongoClient
import plotly.graph_objs as go

title = "Data from Mongo"
sidebar_name = "Data from Mongo"


def run():

    st.title(title)

    mongo_client = MongoClient(
        host = os.getenv('MONGO_HOST'),
        port = int(os.getenv('MONGO_PORT')),
        username = os.getenv('MONGO_USER'),
        password = os.getenv('MONGO_PASSWORD')
    )
    db = mongo_client[os.getenv('MONGO_DB')]
    collection = db['klines']
    for s in collection.distinct('symbol'):
        st.markdown(f'### {s}')
        klines = collection.find({'symbol': s})
        
        prices,dates = [],[]
        for kline in klines:
            prices.append(kline['close'])
            dates.append(kline['close_time'])

       # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=list("abc"))
        chart_data = pd.DataFrame(prices, dates,columns=[s])

        st.line_chart(chart_data)

    for s in collection.distinct('symbol'):
        st.markdown(f'### {s}')
        klines = collection.find({'symbol': s})

        df = pd.DataFrame(list(klines))
        #st.dataframe(df)
        if len(df) == 0:
            st.markdown('Empty dataframe')
            continue

        candlestick = go.Candlestick(x=df['close_time'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'])

        layout = go.Layout(title=f'Candlestick Chart for {s}',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'))

        fig = go.Figure(data=[candlestick], layout=layout)

        # Display the chart using Streamlit
        st.plotly_chart(fig)
    #import os
    #st.write(os.listdir('.'))
    #st.image(Image.open("streamlit_app/assets/sample-image.jpg"))
