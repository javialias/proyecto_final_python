import krakenex
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas_ta as ta
import numpy as np

from pykrakenapi import KrakenAPI

class CryptoPair():

    def __init__(self, pair):
        self.pair=pair
        self.k = KrakenAPI(krakenex.API())
        try: 
            self.ohlc, _ = self.k.get_ohlc_data(self.pair, ascending=True, interval=30)
            self.ohlc['close'] = self.ohlc['close'].apply(lambda x: float(x))
            self.ohlc['dtime'] = pd.to_datetime(self.ohlc.index, format="%YYYY-%mmm-%dd")
        except:
            self.ohlc = pd.DataFrame()
            raise ValueError
        
    def return_dataframe(self):
        return self.ohlc
    
    def show_moving_average(self):
        self.ohlc['moving_average'] = self.ohlc.open.rolling(window=3).mean()
        
        fig = px.line(self.ohlc, x = 'dtime', y = 'moving_average')
        fig.update_layout(title="GDP per Capita vs. Life Expectancy")
        return fig

    def show_rsi(self, comparate = False):
         
        self.ohlc['rsi'] = ta.rsi(self.ohlc['close'], scalar=10)
        if comparate:
            show_y = ['rsi', 'close']
        else:
            show_y = 'rsi'

        fig = px.line(self.ohlc, x = 'dtime', y = show_y)
        fig.update_layout(title="GDP per Capita vs. Life Expectancy")
        return fig
        
    

def get_possible_pairs():
    try:

        k = krakenex.API()
        response = k.query_public('AssetPairs')     
        pairs = np.array(list(response['result'].keys()))
    except:
        raise ValueError
    else:     
        return pairs