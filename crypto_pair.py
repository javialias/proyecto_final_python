import krakenex
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

class CryptoPair():

    def _init_(self, pair):
        self.pair=pair
        self.api = k = krakenex.API()
        self.ohlc = pd.DataFrame (self.api.query_public('OHLC',
         data = {'pair': self.pair, 'interval' : 1,'since': None})['result'][pair])
        self.ohlc.columns = [
                'time', 'open', 'high', 'low', 'close',
                'vwap', 'volume', 'count',]
    
    def show_moving_average(self):
        self.ohlc['moving_average'] = self.ohlc.open.rolling(window=3).mean()

        self.ohlc.plot(x = 'time', y = 'moving_average')
        plt.show()

def initialize():
    k = krakenex.API()
    response = k.query_public('AssetPairs')     
    pairs = np.array(list(response['result'].keys()))
    pair_label = st.selectbox('Seleccione el par que desee estudiar:', pairs)
    if pair_label:
        pair = CryptoPair()
        pair.pair = pair_label
        return pair
