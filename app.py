import streamlit as st

"""
# Proyecto final Python
##### Samuel Medina Gutiérrez y Francisco Javier Alías Carrascosa

Este es el informe sobre el proyecto de la asignatura _Python para el análisis de Datos_ del
Máster en Big Data Science de la Universidad de Navarra. 

1. Puedo escribir enumeraciones
2. Como esta

* O simplemente listas
* Como esta

"""

texto = st.text_input('Introduzca su texto')
slider = st.slider('Mira qué slider guapo', min_value=23, max_value=73)
checkbox = st.checkbox('Quiero vender mi alma al BBVA')

desplegable = st.selectbox(
    'También se pueden poner desplegable', 
    ('uno', 'dos', 'tres'))
st.write('elegiste:', desplegable)
