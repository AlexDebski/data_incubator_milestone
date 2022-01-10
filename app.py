import os
from boto.S3.connection import S3Connection
import requests as rs
import pandas as pd
import json
import streamlit as st
import plotly.express as px


st.sidebar.subheader('Select ticker symbol')
ticker = st.sidebar.text_input('Ticker symbol e.g TSLA')

s3 = S3Connection(os.environ['KEY'])

if ticker != '':

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={s3}'

    r = rs.get(url)
    data = r.json()


    def createDF(x):
        advdict = {}
        #advdict['Symbol'] = {}
        advdict['Date'] = {}
        advdict['Closing'] = {}
        #symbol = x['Meta Data']['2. Symbol'] 
        date = list(d['Time Series (Daily)'].keys()) 
        closing = []
        for y in d['Time Series (Daily)'].keys(): 
            closing.append(d['Time Series (Daily)'][y]['4. close'])
        for y in range(len(closing)):
            #advdict['Symbol'].update({y:symbol})
            advdict['Date'].update({y:date[y]})
            advdict['Closing'].update({y:closing[y]})
        return pd.DataFrame(advdict)

    d = data
    df = createDF(d)

    df['Closing'] = pd.to_numeric(df['Closing'])

    start_date, end_date = '2021-01-01', '2021-01-31'
    df = df.query('Date >= @start_date and Date <= @end_date')


    st.subheader(f'Unadjusted closing price for {ticker} Jan 2021')

    fig = px.line(df, x='Date', y='Closing')
    st.write(fig)

else:
    st.subheader(f'Unadjusted closing price for --- Jan 2021')
