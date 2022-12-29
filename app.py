import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import crypto_pair as cp

with st.sidebar:
    selected = option_menu(
        menu_title = "Menú",
        options = ["Aplicación", "Memoria"],
        icons = ["bar-chart-line-fill", "book"],
        menu_icon = "cast"
    )

if selected == "Aplicación":
    """
    # Aplicación 
    Esta herramienta permite seleccionar un par de monedas de Kraken y visualizar algunos indicadores técnicos.
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
    if(check_mediamovil or check_media_cotiz or check_rsi):
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

if selected == "Memoria":

    '''
    # Memoria del proyecto
    '''

    """
    Este proyecto ha sido creado por Francisco Javier Alías Carrascosa y Samuel Medina Gutiérrez para la asignatura _Python para el Análisis de Datos_ del **Máster en Big Data Science** de la Universidad de Navarra.
    
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    ________________________

    ## _**Índice**_
    #### 1. Introducción y planteamiento del proyecto
    #### 2. Descripción y estructura del código
    ##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.1. Módulo _crypto_pair.py_ 
    ###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.1.1. Clase _crypto_pair_
    ###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.1.2. Funciones auxiliares
    ##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.2. Ejecutable _app.py_
    #### 3. Ejecución y visualización en Streamlit
    
    ________________________
    
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;

    #### 1. Introducción y planteamiento del proyecto

    En esta memoria vamos a explicar cómo ha sido el proceso de creación de este proyecto. En un primer momento, lo objetivos fueron los siguientes: descargar la cotización de un par de monedas a través de la
     API de Kraken, calcular algunos indicadores técnicos de dicho par y realizar las representaciones gráficas 
     correspondientes a dichos indicadores. 

    Por ello, en un principio nos centramos en elaborar un código funcional que nos permitiera cumplir esos objetivos. En este sentido, pudimos obtener los datos 
    de Kraken mediante la API de Krakenex, calculamos los indicadores técnicos valiéndonos de algunas librerías como Pandas y Numpy, y finalmente 
    los graficamos mediante Plotly Express.

    Adicionalmente, experimentando con la librería Streamlit nos dimos cuenta de que podría ser una buena herramienta 
    con la que mostrar los resultados obtenidos. Es por ello que implementamos el código en una aplicación (la cual se puede encontrar en el menú de la izquierda) a través de esta plataforma.
     Esta aplicación nos permitió conseguir una ejecución interactiva y en tiempo real por parte del usuario, lo cual supone un gran valor añadido. Además, nos permitió obtener el par 
     como un input de usuario, que selecciona entre todos los disponibles.

    Por último, viendo las capacidades de Streamlit, hemos decidido también situar la memoria en esta plataforma, para una mayor practicidad y sencillez en su uso y lectura. 
     

    
    
    #### 2. Descripción y estructura del código
    En este apartado vamos a detallar el código que hemos creado para crear la aplicación. Se compone del módulo _crypto_pair.py_ y el ejecutable _app.py_.
     A continuación pasamos a describir su funcionamiento.

    
    #### &nbsp;&nbsp;&nbsp; 2.1. Módulo _crypto_pair.py_


    Este módulo contiene la mayor parte de la lógica del cálculo y visualización de este proyecto. Está compuesto por la clase
    *crypto_pair* y por algunas funciones auxiliares. En él se puede observar la utilización de la librería de Krakenex para la descarga de los datos, la implementación
     del código mediante la clase _crypto_pair_ junto con sus correspondientes atributos y métodos, la utilización de funciones auxiliares y el manejo de errores y excepciones.


    ##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.1.1. Clase _crypto_pair_


    Esta clase está compuesta por los siguientes atributos:

    - **k**: contiene la API de Kraken, a través de la cual se obtienen los datos del par. Se realiza la llamada mediante la librería Krakenex.
    - **pair**: contiene el par sobre el cual se van a visualizar los distintos indicadores técnicos.
    - **ohlc**: contiene el dataframe con la información obtenida sobre el par a través de la API de Kraken.

    Por tanto, el constructor de la clase es el siguiente:

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
    El objeto recibe como parámetro el par de monedas e intenta buscar el dataframe con la información de estas. En caso de error se almacenará un dataframe vacío,
    sin ninguna información.
    """
    
    """
    Esta clase está compuesta por dos métodos: 
    1. **show_moving_average(self, comparate = False, window=3)** : este método es el encargado de crear y visualizar la media móvil del par asociado a la clase. Recibe como parámetros el booleano *comparate*, se encarga de decidir si se visualiza la média móvil por si sola o si se hace junto con la cotización. Para la visualización se utiliza la librería *plotly.express*.
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

    2. **show_rsi(self)**: calcula y muestra el RSI del par. 
    """
    st.code(body= '''def show_rsi(self):
         
        self.ohlc['rsi'] = get_rsi(self.ohlc)

        fig = px.line(self.ohlc, x = 'dtime', y = 'rsi')
        fig.update_layout(title="RSI")
        return fig''', language = "python")
    
    """
    Para ello requiere el uso de la función auxiliar **get_rsi(df)**.
    """

    

    """
    Finalmente, este archivo contiene otra función auxiliar, **get_possible_pairs()**,  que recupera todos los posibles pares sobre los que se puede realizar peticiones en Kraken.
    
    ##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2.1.2. Funciones auxiliares

    A continuación se muestran las funciones auxiliares que se han mencionado en el apartado anterior, y que son necesarias para la correcta ejecución del código.

    1. **get_rsi(df)**
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
    2. **get_possible_pairs()**
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
    

    """
    #### &nbsp;&nbsp;&nbsp; 2.2. Ejecutable _app.py_
    El otro archivo principal de este proyecto es el ejecutable _app.py_. Consiste en una serie de instrucciones que 
    permiten que se vayan desplegando las funcionalidades del módulo _crypto_pair.py_ de una manera práctica en formato de aplicación. 

    Los elementos principales de este código son los siguientes:
    1. Menú principal: es el menú desplegable que aparece a la izquierda y permite al usuario moverse entre la pestaña de la Aplicación o la de la Memoria. El código implementado se observa a continuación. Los iconos fueron seleccionados a través de la biblioteca de https://icons.getbootstrap.com/.
    """

    st.code(body= '''with st.sidebar:
    selected = option_menu(
        menu_title = "Menú",
        options = ["Aplicación", "Memoria"],
        icons = ["bar-chart-line-fill", "book"],
        menu_icon = "cast"
    ) ''', language = 'python'
    )
    
    """
    2. Aplicación: contiene el código que permite ejecutar los comandos en la pestaña de Aplicación. Consiste simplemente en adaptar las funcionalidades de Streamlit a nuestro módulo principal para permitir al usuario una utilización sencilla del entorno de ejecución. El código se muestra a continuación.
    """

    st.code(body = '''if selected == "Aplicación":
    """
    # Aplicación 
    Esta herramienta permite seleccionar un par de monedas de Kraken y visualizar algunos indicadores técnicos.
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
    if(check_mediamovil or check_media_cotiz or check_rsi):
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
                    st.exception("No se han podido recuperar los datos") ''', language = 'python')
    
    """
    3. Memoria: finalmente, esta sección contiene las sentencias, tanto de código como de Markdown, que permiten la visualización de esta memoria. Para evitar aumentar la extensión de manera innecesaria, simplemente mostramos las primeras líneas.
    """
    st.code(body = '''if selected == "Memoria":

    """
    # Memoria del proyecto

    Este proyecto ha sido creado por Francisco Javier Alías Carrascosa y Samuel Medina Gutiérrez para la asignatura _Python para el Análisis de Datos_ del **Máster en Big Data Science** de la Universidad de Navarra.
    ...
    ...

    """ ''', language = 'python')
   
   
    """
    ### 3. Ejecución y visualización en Streamlit
    En este último apartado vamos a mostrar un pequeño tutorial de la Aplicación y vamos a comentar por encima 
    cómo hemos implementado el proyecto en Streamlit.

    Para realizar la ejecución desde la Aplicación, simplemente debemos acceder a la pestaña "Aplicación" del Menú, seleccionar en el primer desplegable el par de monedas que se desee, elegir el indicador o los indicadores que se quieran observar y activar la ejecución mediante el botón "Plot". Cabe destacar que, en caso
    de seleccionar la cotización y media móvil, aparece un slider con el que se puede elegir la ventana del cálculo de la media móvil.

    Por último, cabe destacar que durante todo el proyecto hemos utilizado la herramienta de control de versiones "Git", que no solo nos ha permitido trabajar de forma organizada y eficiente, sino que también
    nos ha sido de utilidad a la hora de realizar el Deploy de la aplicación en Streamlit. Para ello, además de los archivos ya mencionados, ha sido necesario incluir en el repositorio un archivo _requirements.txt_ con las versiones de las librerías utilizadas en el proyecto. Éstas se pueden observar a continuación.
    """

    st.code(body = '''streamlit==1.16.0
streamlit-option-menu==0.3.2
matplotlib==3.6.2
krakenex==2.1.0
pandas==1.5.2
plotly==5.11.0
numpy==1.24.1
pykrakenapi==0.3.1 ''', language = 'python')
