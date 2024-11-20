import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import streamlit as st

# Configurações para o Selenium com Firefox
def setup_selenium():
    options = Options()
    options.headless = True 
    driver = webdriver.Firefox(options=options)
    return driver

# Função para filtrar notícias relacionadas à gripe
def is_gripe_related(title, description):
    keywords = ['gripe', 'covid', 'refriado', 'influenza']
    return any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords)

# Função para organizar visualização das notícias
def show_news_column(news_data, column_title):
    with st.expander(column_title):
        for news in news_data:
            st.markdown(f"**[{news['title']}]({news['link']})**")
            st.write(news['date'])
            st.write(news['description'])


# Função para fazer scraping da página
def scrape_gripe_info():
    driver = setup_selenium()
    url = 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/g/gripe-influenza'
    
    # Acessar a página
    driver.get(url)
    
    # Esperar que a página carregue completamente
    time.sleep(5)  # Ajuste esse tempo de espera conforme necessário

    # Encontrar todos os parágrafos com informações
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    
    # Extrair o texto e armazenar em uma lista
    gripe_info = [p.text for p in paragraphs]
    
    # Fechar o driver
    driver.quit()
    
    # Retornar as informações coletadas
    return gripe_info

# Função para fazer scraping da CNN (notícias gerais)
def scrape_cnn_news():
    driver = setup_selenium()
    url = 'https://www.cnnbrasil.com.br/tudo-sobre/gripe/'
    driver.get(url)
    time.sleep(5)  # Ajuste esse tempo de espera conforme necessário
    
    news_elements = driver.find_elements(By.CLASS_NAME, 'home__list__item')
    news_data = []
    for element in news_elements:
        title = element.find_element(By.TAG_NAME, 'h3').text
        link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        date = element.find_element(By.CLASS_NAME, 'home__title__date').text
        description = element.find_element(By.TAG_NAME, 'a').get_attribute('title')
        if is_gripe_related(title, description):
            news_data.append({'title': title, 'link': link, 'date': date, 'description': description})
    
    driver.quit()
    return news_data

# Função para fazer scraping das notícias do estado e município (G1)
def scrape_g1_news(state, city=None):
    driver = setup_selenium()
    search_query = f"gripe {state}" + (f" {city}" if city else "")
    url = f"https://g1.globo.com/busca/?q={search_query}"
    driver.get(url)
    time.sleep(5)
    
    news_elements = driver.find_elements(By.CLASS_NAME, 'widget--info')
    news_data = []
    for element in news_elements:
        title = element.find_element(By.CLASS_NAME, 'widget--info__title').text
        link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        description = element.find_element(By.CLASS_NAME, 'widget--info__description').text
        date = element.find_element(By.CLASS_NAME, 'widget--info__meta').text
        if is_gripe_related(title, description):
            news_data.append({'title': title, 'link': link, 'date': date, 'description': description})
    
    driver.quit()
    return news_data

# Função para exibir as notícias no Streamlit
def display_news(news, title):
    st.write(f"### {title}")
    for item in news:
        st.write(f"**{item['title']}**")
        st.write(f"[Link]({item['link']})")
        st.write(f"*Publicado em: {item['date']}*")
        st.write("---")


def noticias_informacoes_gripe():

    # Exibir as notícias no Streamlit
    st.title("🔍Notícias e informações sobre gripe🔍")

    # Infomação
    if st.button("Informações sobre gripe"):
        try:
            informacoes = scrape_gripe_info()
            
            # Exibir as informações no Streamlit
            for info in informacoes:
                st.write(info)
    
        except Exception as e:
            st.error(f"Erro ao carregar informações: {e}") 
                

    # CNN: Notícias gerais
    if st.button("Carregar notícias gerais"):
        try:
            cnn_news = scrape_cnn_news()
            if cnn_news:
                show_news_column(cnn_news, "Notícias Gerais")
            else:
                st.write("Nenhuma notícia encontrada.")
        except Exception as e:
            st.error(f"Erro ao carregar notícias gerais: {e}")

    from user_global import MUNICIPIO_USUARIO_GRIPE

    if st.button("Carregar notícias por município"):

        try:
            # state_news = scrape_g1_news(ESTADO_USUARIO)
            city_news = scrape_g1_news(MUNICIPIO_USUARIO_GRIPE) if MUNICIPIO_USUARIO_GRIPE else []
            
            # if state_news:
            #     show_news_column(state_news, f"Notícias no estado: {ESTADO_USUARIO}")
            # else:
            #     st.write(f"Nenhuma notícia encontrada para o estado {ESTADO_USUARIO}.")
            
            if city_news:
                show_news_column(city_news, f"Notícias no município: {MUNICIPIO_USUARIO_GRIPE}")
            elif MUNICIPIO_USUARIO_GRIPE:
                st.write(f"Nenhuma notícia encontrada para o município {MUNICIPIO_USUARIO_GRIPE}.")
        
        except Exception as e:
            st.error(f"Erro ao carregar notícias do estado ou município: {e}")

