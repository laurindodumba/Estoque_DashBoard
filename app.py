# IMPOTAÇÕES DAS BIBILIOTECAS
import pandas as pd
import yfinance as yf
import plotly.express as px
import numpy as np
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

    weights = np.ones(len(tickers))/len(tickers)
    prices['portifolio'] = prices @ weights
    norm_prices = 100 * prices / prices.iloc[0]
    returns = prices.pct_change()[1:]
    vols = returns.std()*np.sqrt(252)
    rets = (norm_prices.iloc[-1] * 100) / 100

    # Criaçã do primeiro gráfico
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.subheader("Desempenho Relativo")
        st.line_chart(norm_prices, height=600)


    # Criação do segundo gráfico
    with col2:
        st.subheader("Risco Retorno")
        fig = px.scatter(
            x=vols,
            y=rets,
            color=rets/vols,
            color_continuous_scale=px.colors.sequential.Bluered_r
        )
        fig.update_traces(
            textfont_color='white',
            marker=dict(size=45),
            textfont_size=10,
        )
        fig.layout.yaxis.title = 'Retorno Total'
        fig.layout.xaxis.title = 'Volatilidade (Anual)'
        fig.layout.height = 600
        fig.layout.yaxis.tickformat = ".0%"
        fig.layout.xaxis.tickformat = ".0%"

        fig.layout.coloraxis.colorbar.title = 'Sharpe'
        st.plotly_chart(fig, use_container_width=True)
# Criar um contexto para o SideBar
with st.sidebar:
    tickers, prices = build_sidebar()

# Chamar a função para a parte principal
build_main(tickers, prices)
