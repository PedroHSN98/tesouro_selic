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

    # Criação inicial da tabela se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT,
                    valor_inicial REAL,
                    valor_mensal REAL,
                    taxa_selic REAL,
                    prazo_meses INTEGER,
                    saldo_final_bruto REAL,
                    imposto REAL,
                    saldo_final_liquido REAL
                 )''')

    # Verificar se a coluna 'valor_mensal' existe, caso contrário, adicionar
    c.execute("PRAGMA table_info(historico)")
    colunas = [col[1] for col in c.fetchall()]
    if "valor_mensal" not in colunas:
        c.execute("ALTER TABLE historico ADD COLUMN valor_mensal REAL")
        conn.commit()
    
    return conn, c

conn, c = init_db()

# Entrada de dados do usuário
st.sidebar.header("Parâmetros do Investimento")

# Input do valor inicial
valor_inicial = st.sidebar.number_input("Valor Inicial (R$)", min_value=100.0, value=1000.0, step=50.0)

# Input de valores mensais adicionais
valor_mensal = st.sidebar.number_input("Aporte Mensal (R$)", min_value=0.0, value=0.0, step=50.0)

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
valores = []
saldo = valor_inicial
for mes in meses:
    saldo = saldo * (1 + taxa_mensal) + valor_mensal
    valores.append(saldo)

# Cálculo do imposto de renda
dias_investimento = prazo_meses * 30  # Assumindo 30 dias por mês
aliquota_ir = calcular_aliquota_ir(dias_investimento)

rendimento_bruto = valores[-1] - valor_inicial - (valor_mensal * (prazo_meses - 1))  # Rendimento antes do IR
imposto_devido = rendimento_bruto * aliquota_ir  # Valor do imposto
saldo_final_liquido = valores[-1] - imposto_devido  # Saldo final líquido

# Salvar no Banco de Dados
if st.sidebar.button("Salvar Resultado no Banco de Dados"):
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO historico (data, valor_inicial, valor_mensal, taxa_selic, prazo_meses, saldo_final_bruto, imposto, saldo_final_liquido)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (data_atual, valor_inicial, valor_mensal, taxa_selic_anual, prazo_meses, valores[-1], imposto_devido, saldo_final_liquido))
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

# Comparação de cenários
if st.sidebar.checkbox("Comparar múltiplos cenários"):
    num_cenarios = st.sidebar.number_input("Quantos cenários deseja comparar?", min_value=1, max_value=5, value=1, step=1)
    
    cenarios = {}  # Dicionário para armazenar dados de cada cenário
    for i in range(1, num_cenarios + 1):
        st.sidebar.subheader(f"Cenário {i}")
        taxa_selic_anual_cenario = st.sidebar.slider(f"Taxa Selic Anual (Cenário {i}) (%)", 
                                                     min_value=0.0, max_value=20.0, value=10.0, step=0.25, key=f"taxa_{i}")
        taxa_mensal_cenario = (1 + taxa_selic_anual_cenario / 100) ** (1 / 12) - 1

        # Cálculo dos valores do cenário
        valores_cenario = []
        saldo_cenario = valor_inicial
        for mes in meses:
            saldo_cenario = saldo_cenario * (1 + taxa_mensal_cenario) + valor_mensal
            valores_cenario.append(saldo_cenario)
        cenarios[f"Saldo (Cenário {i})"] = valores_cenario

    # Adicionar os valores ao DataFrame
    for i, (coluna, valores_cenario) in enumerate(cenarios.items(), start=1):
        df[coluna] = valores_cenario

    # Exibir o gráfico
    st.write("### Comparação de Cenários")
    df_grafico = df.melt(id_vars=["Mês"], value_vars=list(cenarios.keys()) + ["Saldo Bruto (R$)"],
                         var_name="Cenário", value_name="Saldo")
    
    chart = alt.Chart(df_grafico).mark_line().encode(
        x="Mês",
        y=alt.Y("Saldo", title="Saldo Acumulado (R$)"),
        color="Cenário",
        tooltip=["Mês", "Cenário", alt.Tooltip("Saldo", format=".2f")]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# Exibir tabela com resultados
st.subheader("Tabela de Evolução Mensal")
st.dataframe(df.style.format({coluna: "R${:,.2f}" for coluna in df.columns if "Saldo" in coluna}))

# Exibir histórico salvo
st.markdown("### 📊 Histórico de Simulações Salvas")
historico = pd.read_sql_query("SELECT * FROM historico", conn)
if not historico.empty:
    st.dataframe(historico.drop(columns=["id"]))
else:
    st.info("Nenhum histórico encontrado. Salve uma simulação para visualizar aqui.")

# Fechar conexão com o banco de dados
conn.close()
