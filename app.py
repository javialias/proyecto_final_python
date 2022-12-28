import streamlit as st
from streamlit_option_menu import option_menu
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
    # Proyecto final Python
    ##### Samuel Medina Gutiérrez y Francisco Javier Alías Carrascosa

    Este es el informe sobre el proyecto de la asignatura _Python para el análisis de Datos_ del
    Máster en Big Data Science de la Universidad de Navarra. 
    """
    par = cp.initialize()
    if par:
        st.write(f'Par seleccionado: {par.pair}')

    """
    Escoja los indicadores técnicos que desea graficar:
    """
    check_mediamovil = st.checkbox('Media Móvil')
    check_rsi = st.checkbox('RSI')
    check_media_cotiz = st.checkbox('Media Móvil junto con la cotización del par')

    if st.button('Plot'):
        if check_mediamovil:
            st.write('media movil')
        if check_rsi:
            st.write('rsi')
        if check_media_cotiz:
            st.write('media cotizacion')

if selected == "Informe":
    st.write("esto es un informe to guapo")
    
    
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