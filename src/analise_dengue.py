import streamlit as st
import pandas as pd
from dengue_data_processing import carregar_dataset
import pydeck as pdk
import plotly.graph_objects as go
import streamlit as st

def definir_cor(risco):
    if risco > 7:
        return [255, 0, 0, 160]  # Vermelho (risco alto)
    elif 1 < risco <= 6.99:
        return [255, 255, 0, 160]  # Amarelo (risco moderado)
    else:
        return [0, 255, 0, 160]  # Verde (risco baixo)

def plotar_mapa(df):
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[longitude, latitude]',
        get_radius='5000',
        get_fill_color='cor',
        pickable=True,
        auto_highlight=True,
    )
    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=6
    )
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={
        'html': '<b>Município:</b> {municipio}<br><b>Casos:</b> {casos}<br><b>Est. Casos:</b> {casos_est}<br><b>Disseminação:</b> {disseminação}<br><b>Temperatura:</b> {tempmed}°C<br><b>Umidade:</b> {umidmed}%',
        'style': {'color': 'white'}
    })
    st.pydeck_chart(r)

# Função para plotar gráficos interativos
def plotar_graficos(df_municipio, df_min_max, municipio_usuario, estado_usuario):
    fig = go.Figure()
        # Verificar se há dados para o município
    if not df_municipio.empty:
        # Adiciona a linha do município selecionado
        fig.add_trace(go.Scatter(x=df_municipio['data_week'], y=df_municipio['casos'],
                                mode='lines+markers', name=f'{municipio_usuario} - Casos', line=dict(color='blue', width=4)))
    else:
        # Mensagem se não houver dados para o município
        st.warning(f'Não há dados disponíveis para o município {municipio_usuario} no período selecionado.')

    # Linha dos casos mínimos do estado
    fig.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('casos', 'min')],
                            mode='lines', name='Casos Mínimos (Estado)', line=dict(color='green', dash='dash')))
    # Linha dos casos máximos do estado
    fig.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('casos', 'max')],
                            mode='lines', name='Casos Máximos (Estado)', line=dict(color='red', dash='dash')))
    # Configurações do layout
    fig.update_layout(title=f'Comparação de Incidência de Casos {estado_usuario}', xaxis_title='Semana',
                    yaxis_title='Número de Casos', legend_title='Municípios')
    st.plotly_chart(fig)


    # Gráfico de linha para Temperatura Média (tempmed)
    fig_tempmed = go.Figure()

    # Adicionar a linha do município selecionado
    fig_tempmed.add_trace(go.Scatter(x=df_municipio['data_week'], y=df_municipio['tempmed'],
                                    mode='lines+markers', name=f'{municipio_usuario} - Temperatura Média', line=dict(color='blue', width=4)))

    # Adicionar a linha da temperatura mínima do estado
    fig_tempmed.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('tempmin', 'min')],
                                    mode='lines', name='Temperatura Mínima (Estado)', line=dict(color='green', dash='dash')))

    # Adicionar a linha da temperatura máxima do estado
    fig_tempmed.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('tempmax', 'max')],
                                    mode='lines', name='Temperatura Máxima (Estado)', line=dict(color='red', dash='dash')))

    # Adicionar título e rótulos
    fig_tempmed.update_layout(title=f'Comparação de Temperatura Média no Estado {estado_usuario}',
                            xaxis_title='Semana',
                            yaxis_title='Temperatura Média (°C)',
                            legend_title='Municípios')

    st.plotly_chart(fig_tempmed)


    # Gráfico de linha para Umidade Média (umidmed)
    fig_umidmed = go.Figure()

    # Adicionar a linha do município selecionado
    fig_umidmed.add_trace(go.Scatter(x=df_municipio['data_week'], y=df_municipio['umidmed'],
                                    mode='lines+markers', name=f'{municipio_usuario} - Umidade Média', line=dict(color='blue', width=4)))

    # Adicionar a linha da umidade mínima do estado
    fig_umidmed.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('umidmin', 'min')],
                                    mode='lines', name='Umidade Mínima (Estado)', line=dict(color='green', dash='dash')))

    # Adicionar a linha da umidade máxima do estado
    fig_umidmed.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('umidmax', 'max')],
                                    mode='lines', name='Umidade Máxima (Estado)', line=dict(color='red', dash='dash')))

    # Adicionar título e rótulos
    fig_umidmed.update_layout(title=f'Comparação de Umidade Média no Estado {estado_usuario}',
                            xaxis_title='Semana',
                            yaxis_title='Umidade Média (%)',
                            legend_title='Municípios')

    st.plotly_chart(fig_umidmed)


    # Gráfico de linha para Disseminação (disseminação)
    fig_disseminacao = go.Figure()

    # Adicionar a linha do município selecionado
    fig_disseminacao.add_trace(go.Scatter(x=df_municipio['data_week'], y=df_municipio['disseminação'],
                                        mode='lines+markers', name=f'{municipio_usuario} - Disseminação', line=dict(color='blue', width=4)))

    # Adicionar a linha da disseminação mínima do estado
    fig_disseminacao.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('disseminação', 'min')],
                                        mode='lines', name='Disseminação Mínima (Estado)', line=dict(color='green', dash='dash')))

    # Adicionar a linha da disseminação máxima do estado
    fig_disseminacao.add_trace(go.Scatter(x=df_min_max['data_week'], y=df_min_max[('disseminação', 'max')],
                                        mode='lines', name='Disseminação Máxima (Estado)', line=dict(color='red', dash='dash')))

    # Adicionar título e rótulos
    fig_disseminacao.update_layout(title=f'Comparação de Disseminação no Estado {estado_usuario}',
                                xaxis_title='Semana',
                                yaxis_title='Disseminação',
                                legend_title='Municípios')

    st.plotly_chart(fig_disseminacao)

import user_global

def exibir_analise_municipio(df):
    
    st.title("🦟Análise da Situação do Município - Dengue🦟")
    
    # Conversão e tratamento dos dados
    df['data_week'] = pd.to_datetime(df['data_week'], errors='coerce')
    municipio_usuario = st.sidebar.selectbox("Selecione seu município", sorted(df['municipio'].unique()))
    estado_usuario = df[df['municipio'] == municipio_usuario]['estado'].values[0]
    df_estado = df[df['estado'] == estado_usuario]
    data_maxima = df_estado['data_week'].max()
    filtro_periodo = st.radio("Filtrar por", ('Último Mês', 'Último Ano'))
    user_global.MUNICIPIO_USUARIO = municipio_usuario
    user_global.ESTADO_USUARIO = estado_usuario
    # Definir o período de filtragem
    data_inicial = data_maxima - pd.DateOffset(months=1) if filtro_periodo == 'Último Mês' else data_maxima - pd.DateOffset(years=1)
    df_filtrado = df_estado[(df_estado['data_week'] >= data_inicial) & (df_estado['data_week'] <= data_maxima)].copy()

    
    # Calcular risco e aplicar cor
    df_filtrado.loc[:, 'risco_dengue'] = df_filtrado['casos_est'] * 0.1 + df_filtrado['casos'] * 0.3 + df_filtrado['incidência_100khab'] * 0.1 + df_filtrado['disseminação'] * 5
    df_filtrado.loc[:, 'cor'] = df_filtrado['risco_dengue'].apply(definir_cor)
    
    # Mostrar mapa interativo
    st.write("O mapa corresponde à opção de um mês.")
    plotar_mapa(df_filtrado)
    
    # Criar e exibir gráficos
    df_min_max = df_filtrado.groupby('data_week').agg({
        'casos': ['min', 'max'],
        'incidência_100khab': ['min', 'max'],
        'disseminação': ['min', 'max'],
        'umidmed': ['min', 'max'],
        'umidmin': ['min', 'max'],
        'umidmax': ['min', 'max'],
        'tempmed': ['min', 'max'],
        'tempmin': ['min', 'max'],
        'tempmax': ['min', 'max']
    }).reset_index()

    df_municipio = df_filtrado[df_filtrado['municipio'] == municipio_usuario]
    plotar_graficos(df_municipio, df_min_max, municipio_usuario, estado_usuario)

    return estado_usuario, municipio_usuario, df_municipio, df_filtrado 