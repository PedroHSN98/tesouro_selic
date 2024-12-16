import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import io
import sqlite3
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="Simulador Tesouro Selic", layout="wide")

# Título e descrição
st.title("📈 Simulador Tesouro Selic")
st.markdown("Simule o rendimento do Tesouro Selic e acompanhe a evolução do seu investimento ao longo do tempo.")

# Configuração do Banco de Dados SQLite
def init_db():
    conn = sqlite3.connect("investimentos.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    valor_inicial REAL,
                    taxa_selic REAL,
                    prazo_meses INTEGER,
                    saldo_final_bruto REAL,
                    imposto REAL,
                    saldo_final_liquido REAL
                 )''')
    conn.commit()
    return conn, c

conn, c = init_db()

# Entrada de dados do usuário
st.sidebar.header("Parâmetros do Investimento")

# Input do valor inicial
valor_inicial = st.sidebar.number_input("Valor Inicial (R$)", min_value=100.0, value=1000.0, step=50.0)

# Input da taxa Selic anual
taxa_selic_anual = st.sidebar.slider("Taxa Selic Anual (%)", min_value=0.0, max_value=20.0, value=12.75, step=0.25)

# Input do prazo do investimento
prazo_meses = st.sidebar.slider("Prazo do Investimento (meses)", min_value=1, max_value=360, value=12, step=1)

# Tabela regressiva do IR
def calcular_aliquota_ir(dias):
    if dias <= 180:
        return 0.225  # 22,5%
    elif dias <= 360:
        return 0.20  # 20%
    elif dias <= 720:
        return 0.175  # 17,5%
    else:
        return 0.15  # 15%

# Cálculo da rentabilidade
taxa_mensal = (1 + taxa_selic_anual / 100) ** (1 / 12) - 1
meses = np.arange(1, prazo_meses + 1)
valores = [valor_inicial * ((1 + taxa_mensal) ** mes) for mes in meses]

# Cálculo do imposto de renda
dias_investimento = prazo_meses * 30  # Assumindo 30 dias por mês
aliquota_ir = calcular_aliquota_ir(dias_investimento)

rendimento_bruto = valores[-1] - valor_inicial  # Rendimento antes do IR
imposto_devido = rendimento_bruto * aliquota_ir  # Valor do imposto
saldo_final_liquido = valores[-1] - imposto_devido  # Saldo final líquido

# Salvar no Banco de Dados
if st.sidebar.button("Salvar Resultado no Banco de Dados"):
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO historico (data, valor_inicial, taxa_selic, prazo_meses, saldo_final_bruto, imposto, saldo_final_liquido)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (data_atual, valor_inicial, taxa_selic_anual, prazo_meses, valores[-1], imposto_devido, saldo_final_liquido))
    conn.commit()
    st.success("Resultado salvo no banco de dados com sucesso!")

# Exibindo resultados
st.markdown("### 🏦 Resumo do Investimento")
st.write(f"- **Saldo Final Bruto:** R${valores[-1]:,.2f}")
st.write(f"- **Imposto de Renda (IR):** R${imposto_devido:,.2f} ({aliquota_ir * 100:.1f}%)")
st.write(f"- **Saldo Final Líquido:** R${saldo_final_liquido:,.2f}")

# Gráfico customizado
df = pd.DataFrame({
    "Mês": meses,
    "Saldo Bruto (R$)": valores,
})

chart = alt.Chart(df).mark_line().encode(
    x=alt.X("Mês", title="Meses"),
    y=alt.Y("Saldo Bruto (R$)", title="Saldo Bruto Acumulado (R$)"),
    tooltip=["Mês", alt.Tooltip("Saldo Bruto (R$)", format=".2f")]
).properties(
    title="Evolução do Saldo Bruto Acumulado"
).interactive()

st.altair_chart(chart, use_container_width=True)

# Exibir histórico salvo
st.markdown("### 📊 Histórico de Simulações Salvas")
historico = pd.read_sql_query("SELECT * FROM historico", conn)
if not historico.empty:
    historico_display = historico.drop(columns=["id"])  # Remove o ID para exibição
    st.dataframe(historico_display)
else:
    st.info("Nenhum histórico encontrado. Salve uma simulação para visualizar aqui.")

# Fechar conexão com o banco de dados
conn.close()

# Botão para exportar a tabela como Excel usando openpyxl
try:
    import openpyxl
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Evolução Mensal")

    st.download_button(
        label="💾 Baixar Tabela de Evolução (Excel)",
        data=output.getvalue(),
        file_name="evolucao_tesouro_selic.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except ImportError:
    st.error("O módulo 'openpyxl' não está instalado. Por favor, instale-o usando 'pip install openpyxl'.")
