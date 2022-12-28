import streamlit as st
import crypto_pair as cp

"""
# Proyecto final Python
##### Samuel Medina Gutiérrez y Francisco Javier Alías Carrascosa

Este es el informe sobre el proyecto de la asignatura _Python para el análisis de Datos_ del
Máster en Big Data Science de la Universidad de Navarra. 
"""


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

par = cp.initialize()
if par:
    st.write(f'Par seleccionado: {par.pair}')

"""
Escoja los indicadores técnicos que desea graficar:
"""
check_mediamovil = st.checkbox('Media Móvil')
check_rsi = st.checkbox('RSI')
check_media_cotiz = st.checkbox('Media Móvil junto con la cotización del par')
check_media_cotisdfz = st.checkbox('Media Móvil junfsdfsdfn la cotización del par')

if st.button('Plot'):
    #funciones que llaman a las gráficas
    suma = 2+2
    
    
    
