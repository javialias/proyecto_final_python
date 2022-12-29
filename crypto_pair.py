import krakenex
import pandas as pd
import plotly.express as px
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
    
    def show_moving_average(self, comparate = False, window=3):
        self.ohlc['moving_average'] = self.ohlc.open.rolling(window=window).mean()
        
        if comparate:
            show_y = ['moving_average', 'close']
            labels = {'moving_average': 'Media ´Movil', 'close': 'Precio de cierre'}
            titulo = 'Media Móvil y cotización'
        else:
            show_y = 'moving_average'
            labels = {'moving_average': 'Media Móvil'}
            titulo = 'Media Móvil'

        fig = px.line(self.ohlc, x = 'dtime', y = show_y, labels=labels)
        fig.update_layout(title=titulo)
        return fig

    def show_rsi(self):
         
        self.ohlc['rsi'] = get_rsi(self.ohlc)
        

        fig = px.line(self.ohlc, x = 'dtime', y = 'rsi')
        fig.update_layout(title="RSI")
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

def get_rsi(df):
    close_serie = df['close'].diff(1)

    up = close_serie.clip(lower=0)
    down = close_serie.clip(upper=0)
    down*=-1

    ma_up = up.rolling(window = 14).mean()
    ma_down = down.rolling(window = 14).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))

    return rsi

