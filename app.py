# IMPOTAÇÕES DAS BIBILIOTECAS
import pandas as pd
import yfinance as yf
import plotly.express as px
import streamlit as st
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid


# Configuração do titulo do projeto
st.title('Análise de Investimento')


# FUNÇÕES
def build_sidebar():
    st.image("img\logo-250-100-transparente.png")

    # Ler o dataframe
    ticker_list = pd.read_csv('tickers_ibra.csv', index_col=0)
    tickers = st.multiselect(label="Selecione as Empresas", options=ticker_list)

    # Adicionando ".SA" aos tickers selecionados
    tickers = [t + ".SA" for t in tickers]
    
    # Definindo o intervalo de datas
    start_date = st.date_input("De", format="DD/MM/YYYY", value=datetime(2023, 1, 2))
    end_date = st.date_input("Até", format="DD/MM/YYYY", value=datetime.today())

    # Baixar os preços, se tickers forem selecionados
    prices = pd.DataFrame()  # Default empty dataframe
    if tickers:
        prices = yf.download(tickers, start=start_date, end=end_date)["Close"]
    
    return tickers, prices


def build_main(tickers, prices):
    # Exibir a tabela de preços
    if not prices.empty:
        st.dataframe(prices)
    else:
        st.warning("Nenhum dado disponível. Selecione ao menos uma empresa.")


# Criar um contexto para o SideBar
with st.sidebar:
    tickers, prices = build_sidebar()

# Chamar a função para a parte principal
build_main(tickers, prices)
