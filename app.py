import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import crypto_pair as cp

with st.sidebar:
    selected = option_menu(
        menu_title = "Menú",
        options = ["Aplicación", "Informe"],
        icons = ["bar-chart-line-fill", "book"],
        menu_icon = "cast"
    )

if selected == "Aplicación":
    """
    # Aplicación 
    ##### Samuel Medina Gutiérrez y Francisco Javier Alías Carrascosa

    Esta aplicación permite seleccionar un par de monedas de Kraken y visualizar algunos indicadores técnicos.
    
    
    """
    possible_pairs = cp.get_possible_pairs()
    possible_indicators = ['Média movil', 'RSI', 'Cotización y media móvil']

    par_col, indicator_col, window_col = st.columns([5, 5, 5])

    with par_col:
        pair_label = st.selectbox('Seleccione el par que desee estudiar:', possible_pairs)
    
        if pair_label:
            par = cp.CryptoPair(pair_label)

    with indicator_col:

        indicators = st.multiselect('Seleccione los indicadores que desee:', options = possible_indicators)
        check_mediamovil = 'Média movil' in indicators
        check_rsi = 'RSI' in indicators
        check_media_cotiz = 'Cotización y media móvil' in indicators

    with window_col:
        if (check_mediamovil or check_media_cotiz):
            ventana = int(st.slider(
                "Seleccione la ventana media móvil:",
                min_value=3,
                max_value=14,
                step=1,
                value=3,
            ))
    
    if (check_mediamovil or check_media_cotiz or check_rsi ):
       if st.button('Plot'):

        if check_mediamovil:
            try:
                st.plotly_chart(par.show_moving_average(window=ventana), use_container_width=True)
            except ValueError:
                st.exception("No se han podido recuperar los datos")
        if check_rsi:
            try:
                st.plotly_chart(par.show_rsi(), use_container_width=True)
            except ValueError:
                st.exception("No se han podido recuperar los datos")
        if check_media_cotiz:
            try:
                st.plotly_chart(par.show_moving_average(comparate = True,
                    window = ventana), use_container_width=True)
            except ValueError:
                st.exception("No se han podido recuperar los datos")

if selected == "Informe":

    '''
    # Informe del proyecto

    ## Autores: Javier Alias Carrascosa, Samuel Medina Gutiérrez

    '''


    """
    ### crypto_pair.py

    Este módulo contiene la mayor parte de la lógica de visualización de este proyecto. Está compuesto por la clase
    *Crypto_pair* y por algunas funciones auxiliares.

    #### Clase crypto_pair

    Esta clase está compuesta por los siguientes atributos:

    - **k**: contiene la api de kraken
    - **pair**: contiene el par sobre el cual se vaan a visualizar los distintos indicadores
    - **ohlc**: dataframe con la información obtenida sobre el par a través de la api de kraken

    Por tanto, el constructor de esta clase es el siguiente:

    """

    st.code(body= '''
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
                raise ValueErrorg''', language = "python")

    """
    Recibe como parámetro el par de monedase intenta buscar el dataframe con la información de estas, en caso de error se almacenará un dataframe vacío,
    sin ninguna información.
    """
    
    """
    Esta clase está compuesta por dos métodos: 
    1. **show_moving_average(self, comparate = False, window=3)** : este método es el encargado de crear y visualizar la media móvil
    del par asociado a la clase. Recibe como parámetros el booleano *comparate*, se encarga de decidir si se visualiza la média móvil por
    si sola o si se hace junto con la cotización. Para la visualización se utiliza la librería *pyplot.express*.
    """
    

    st.code(body= '''def show_moving_average(self, comparate = False, window=3):
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
        return fig''', language = "python")
    
    """

    2. **show_rsi(self)**: calcula y muestra el rsi del par. 
    """
    st.code(body= '''def show_rsi(self):
         
        self.ohlc['rsi'] = get_rsi(self.ohlc)
        

        fig = px.line(self.ohlc, x = 'dtime', y = 'rsi')
        fig.update_layout(title="RSI")
        return fig''', language = "python")
    
    """
    Utiliza la función auxiliar **get_rsi(df)**
    """

    st.code(body= '''def get_rsi(df):
    close_serie = df['close'].diff(1)

    up = close_serie.clip(lower=0)
    down = close_serie.clip(upper=0)
    down*=-1

    ma_up = up.rolling(window = 14).mean()
    ma_down = down.rolling(window = 14).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))

    return rsi''', language = "python")

    """
    Finalmente este archivo contiene otra función auxiliar que recupera todos los posibles pares sobre los que se puede realizar peticiones en Kraken:
    """

    st.code(body= '''def get_possible_pairs():
    try:

        k = krakenex.API()
        response = k.query_public('AssetPairs')     
        pairs = np.array(list(response['result'].keys()))
    except:
        raise ValueError
    else:     
        return pairs''', language = "python")

    
    
    
#1. Puedo escribir enumeraciones
#2. Como esta

#* O simplemente listas
#* Como esta


#texto = st.text_input('Introduzca su texto')
#slider = st.slider('Mira qué slider guapo', min_value=23, max_value=73)
#checkbox = st.checkbox('Quiero vender mi alma al BBVA')

#desplegable = st.selectbox(
#    'También se pueden poner desplegable', 
#    ('uno', 'dos', 'tres'))
#st.write('elegiste:', desplegable)