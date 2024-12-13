import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io

# Configurações da página
st.set_page_config(page_title="Simulador Tesouro Selic", layout="wide")

# Título e descrição
st.title("📈 Simulador Tesouro Selic")
st.markdown("Simule o rendimento do Tesouro Selic e acompanhe a evolução do seu investimento ao longo do tempo.")

# Entrada de dados do usuário
st.sidebar.header("Parâmetros do Investimento")

# Input do valor inicial
valor_inicial = st.sidebar.number_input("Valor Inicial (R$)", min_value=100.0, value=1000.0, step=50.0)

# Input da taxa Selic anual
taxa_selic_anual = st.sidebar.slider("Taxa Selic Anual (%)", min_value=0.0, max_value=20.0, value=12.75, step=0.25)

# Input do prazo do investimento
prazo_meses = st.sidebar.slider("Prazo do Investimento (meses)", min_value=1, max_value=360, value=12, step=1)

# Informações adicionais
with st.sidebar.expander("ℹ️ Informações sobre o simulador"):
    st.write("""
    - **Valor Inicial**: Quantia aplicada no início do investimento.
    - **Taxa Selic Anual**: Projeção da taxa básica de juros (Selic) ao ano.
    - **Prazo do Investimento**: Duração do investimento em meses.
    - O cálculo considera juros compostos mensais com base na taxa Selic.
    """)

# Cálculo da rentabilidade
taxa_mensal = (1 + taxa_selic_anual / 100) ** (1 / 12) - 1

# Gerar tabela de evolução do investimento
meses = np.arange(1, prazo_meses + 1)
valores = [valor_inicial * ((1 + taxa_mensal) ** mes) for mes in meses]

df = pd.DataFrame({
    "Mês": meses,
    "Saldo (R$)": valores
})

# Calculando o ganho total
ganho_total = valores[-1] - valor_inicial

# Exibindo resultados
st.markdown("### 🏦 Resumo do Investimento")
st.write(f"- **Saldo Final:** R${valores[-1]:,.2f}")
st.write(f"- **Ganho Total:** R${ganho_total:,.2f}")

# Gráfico customizado
chart = alt.Chart(df).mark_line().encode(
    x=alt.X("Mês", title="Meses"),
    y=alt.Y("Saldo (R$)", title="Saldo Acumulado (R$)"),
    tooltip=["Mês", alt.Tooltip("Saldo (R$)", format=".2f")]
).properties(
    title="Evolução do Saldo Acumulado"
).interactive()

st.altair_chart(chart, use_container_width=True)

# Comparação de cenários
if st.sidebar.checkbox("Comparar múltiplos cenários"):
    taxa_selic_anual_2 = st.sidebar.slider("Taxa Selic Anual (Cenário 2) (%)", min_value=0.0, max_value=20.0, value=10.0, step=0.25)
    taxa_mensal_2 = (1 + taxa_selic_anual_2 / 100) ** (1 / 12) - 1
    valores_2 = [valor_inicial * ((1 + taxa_mensal_2) ** mes) for mes in meses]

    df["Saldo (Cenário 2) (R$)"] = valores_2

    st.write("### Comparação de Cenários")
    st.line_chart(df.set_index("Mês"))

# Exibir a tabela completa
st.subheader("Tabela de Evolução Mensal")
st.dataframe(df.style.format({"Saldo (R$)": "R${:,.2f}"}))

# Botão para exportar a tabela como Excel usando openpyxl
try:
    import openpyxl
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Evolução Mensal")

    st.download_button(
        label="📥 Baixar Tabela de Evolução (Excel)",
        data=output.getvalue(),
        file_name="evolucao_tesouro_selic.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except ImportError:
    st.error("O módulo 'openpyxl' não está instalado. Por favor, instale-o usando 'pip install openpyxl'.")
