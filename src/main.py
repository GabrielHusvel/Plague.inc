import streamlit as st
from api import APP  # Importar a API FastAPI
from gripe_mapa_regional import create_dashboard
# from gripe_mapa_capital import map_capital
from config import configure_page  # Configuração inicial do Streamlit
from noticias_gripe import noticias_informacoes_gripe
import streamlit as st
import google.generativeai as genai
import os
from analise_llm import exibir_analise_municipio
from dengue_data_processing import carregar_dataset
from dotenv import load_dotenv

# Configuração inicial
configure_page()
# Carregar as variáveis do .env
load_dotenv('../.env')

# Obtém a chave da API 
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Carregar o dataset
df = carregar_dataset()

# Definir as opções de navegação
menu = ["Tela Inicial", "Chat de Consulta", 'Mapa Interativo']
choice = st.sidebar.selectbox("Navegue pelo App", menu)

# Tela Inicial
if choice == "Tela Inicial":
    st.title("Bem-vindo ao Sistema de Consulta de Doenças Plague.inf☣️")
    st.markdown(
        """
        Este aplicativo permite consultar a situação da dengue e gripe(inlfuenza) em municípios brasileiros.
        Você pode:
        - Obter análises detalhadas com base nos dados disponíveis.
        - Interagir com um modelo de IA para resumir e interpretar informações.

        **Como usar**:
        - Navegue até o "Chat de Consulta" no menu lateral.
            - Insira o nome do município que deseja consultar.
            - Receba análises detalhadas e orientações baseadas nos dados.
        - Navegue até o "Mapa Interativo" no menu lateral.
            - Escolha seu municipio e veja no mapa a situação os municipios da região.
            - Descubra notícias sobre a região escolhida.
            - Obtenha análises interativas e personalizadas e acesso aos dados.
        **⚠️ Nota:** Os dados são atualizados periodicamente para refletir a situação mais recente.
        """
    )
    st.image("https://i.imgur.com/gygo72j.jpg", use_column_width=True)

# Chat de Consulta
elif choice == "Chat de Consulta":
    st.title("Chat de Consulta de Dengue")
    
    # Histórico de mensagens no Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada do usuário: nome do município
    if user_input := st.chat_input("Digite o nome do município que deseja consultar:"):
        # Normalizar a entrada do usuário
        user_input = user_input.strip().title()
        
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Executa a análise com base no município fornecido
        with st.chat_message("assistant"):
            with st.spinner("Analisando os dados..."):
                try:
                    # Executa a análise com a função customizada
                    estado_usuario, municipio_usuario, df_municipio, df_filtrado = exibir_analise_municipio(df, user_input)

                    # Cria o prompt dinâmico para o modelo LLM
                    prompt = f"""
                    O usuário consultou o município {municipio_usuario}, no estado {estado_usuario}.
                    Abaixo estão os dados relevantes sobre a situação da dengue na região:

                    Dados do município:
                    {df_municipio.to_dict()}

                    Dados filtrados do estado:
                    {df_filtrado[['municipio', 'risco_dengue', 'casos', 'casos_est']].head(5).to_dict()}

                    Com base nesses dados:
                    - Resuma a situação da dengue no município.
                    - Dê Dicas importantes sobre cuidados que o usuário pode tomar para se previnir da doença.
                    
                    """
                    # Gera a resposta com o modelo
                    response = model.generate_content(prompt)
                    resposta_modelo = response.text

                    # Exibe a resposta no chat
                    st.markdown(resposta_modelo)

                    # Salva a resposta no histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta_modelo})
                except ValueError as ve:
                    st.error(str(ve))  # Exibe a mensagem de erro amigável ao usuário
                    st.session_state.messages.append({"role": "assistant", "content": str(ve)})
                except Exception as e:
                    erro_msg = f"Houve um erro ao consultar o município: {e}"
                    st.error(erro_msg)
                    st.session_state.messages.append({"role": "assistant", "content": erro_msg})

elif choice == "Mapa Interativo":
    
    # Escolha de abas
    diase = st.sidebar.selectbox('Escolha a doença', ['Dengues', 'Gripes'])

    if diase == 'Gripes':
        
        abas = st.tabs(["Análise por Município", "Informações e Notícias", "Dados Epidemiológicos-Opção em desenvolvimento"])
        
        with abas[0]:
            create_dashboard()

        with abas[1]:
            noticias_informacoes_gripe()



    import streamlit as st
    from dengue_data_processing import carregar_dataset
    from analise_dengue import exibir_analise_municipio
    from noticias_dengue import exibir_noticias_informacoes
    from dados_dengue import exibir_dados_epidemiologicos


    if diase == "Dengues":
        df = carregar_dataset()

        if not df.empty:
            abas = st.tabs(["Análise por Município", "Informações e Notícias", "Dados Epidemiológicos"])
            
            with abas[0]:
                exibir_analise_municipio(df)

            with abas[1]:
                exibir_noticias_informacoes()

            with abas[2]:
                exibir_dados_epidemiologicos(df)

            
