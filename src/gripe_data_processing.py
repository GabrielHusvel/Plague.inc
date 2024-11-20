import pandas as pd
import streamlit as st


# Função para carregar os dados
@st.cache_data
def carregar_dados():
    
    df_municipios = pd.read_csv('data_sus/infogripe-master/Dados/InfoGripe/2020-2024/macrorregiao_municipios_fx_etaria_casos_2024.csv')
    
    return df_municipios
