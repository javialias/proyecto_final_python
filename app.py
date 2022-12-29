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
    st.write("esto es un informe to guapo")

    st.code(body= '''def show_rsi(self):
         
        self.ohlc['rsi'] = get_rsi(self.ohlc)
        

        fig = px.line(self.ohlc, x = 'dtime', y = 'rsi')
        fig.update_layout(title="RSI")
        return fig''', language = "python")
    
    
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