
import pandas as pd

def definir_cor(risco):
    if risco > 7:
        return [255, 0, 0, 160]  # Vermelho (risco alto)
    elif 1 < risco <= 6.99:
        return [255, 255, 0, 160]  # Amarelo (risco moderado)
    else:
        return [0, 255, 0, 160]  # Verde (risco baixo)

def exibir_analise_municipio(df, municipio_usuario):
    # Converter datas e preparar o dataframe
    df['data_week'] = pd.to_datetime(df['data_week'], errors='coerce')

    # Verificar se o município existe no dataframe
    if municipio_usuario not in df['municipio'].unique():
        raise ValueError(f"O município '{municipio_usuario}' não foi encontrado no dataset.")

    # Identificar o estado do município
    estado_usuario = df[df['municipio'] == municipio_usuario]['estado'].values[0]

    # Filtrar dados do estado
    df_estado = df[df['estado'] == estado_usuario]

    # Determinar o período de análise
    data_maxima = df_estado['data_week'].max()
    data_inicial = data_maxima - pd.DateOffset(months=1)  # Exemplo de último mês
    df_filtrado = df_estado[(df_estado['data_week'] >= data_inicial) & (df_estado['data_week'] <= data_maxima)].copy()

    # Calcular risco e aplicar cor
    df_filtrado.loc[:, 'risco_dengue'] = (
        df_filtrado['casos_est'] * 0.1 +
        df_filtrado['casos'] * 0.3 +
        df_filtrado['incidência_100khab'] * 0.1 +
        df_filtrado['disseminação'] * 5
    )
    df_filtrado.loc[:, 'cor'] = df_filtrado['risco_dengue'].apply(definir_cor)

    # Dados do município solicitado
    df_municipio = df_filtrado[df_filtrado['municipio'] == municipio_usuario]

    # Retorna informações necessárias
    return estado_usuario, municipio_usuario, df_municipio, df_filtrado
