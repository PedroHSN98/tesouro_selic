import streamlit as st
import pandas as pd
import numpy as np

# Configurações da página
st.set_page_config(page_title="Simulador Tesouro Selic", layout="centered")

# Título do aplicativo
st.title("Simulador Tesouro Selic")

# Entrada de dados do usuário
st.sidebar.header("Parâmetros do Investimento")

# Input do valor inicial
valor_inicial = st.sidebar.number_input("Valor Inicial (R$)", min_value=100.0, value=1000.0, step=50.0)

# Input da taxa Selic anual
taxa_selic_anual = st.sidebar.slider("Taxa Selic Anual (%)", min_value=0.0, max_value=20.0, value=12.75, step=0.25)

# Input do prazo do investimento
prazo_meses = st.sidebar.slider("Prazo do Investimento (meses)", min_value=1, max_value=360, value=12, step=1)

# Cálculo da rentabilidade
taxa_mensal = (1 + taxa_selic_anual / 100) ** (1 / 12) - 1

# Gerar tabela de evolução do investimento
meses = np.arange(1, prazo_meses + 1)
valores = [valor_inicial * ((1 + taxa_mensal) ** mes) for mes in meses]

df = pd.DataFrame({
    "Mês": meses,
    "Saldo (R$)": valores
})

# Exibir os resultados
st.subheader("Resultado do Investimento")
st.write(f"Com base em um investimento inicial de **R${valor_inicial:,.2f}**, a uma taxa Selic anual de **{taxa_selic_anual}%**, o saldo ao final de **{prazo_meses} meses** será de:")
st.write(f"**R${valores[-1]:,.2f}**")

# Gráfico de evolução do investimento
st.line_chart(df.set_index("Mês"))

# Exibir a tabela completa
st.subheader("Tabela de Evolução Mensal")
st.dataframe(df.style.format({"Saldo (R$)": "R${:,.2f}"}))
