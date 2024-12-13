# Simulador Tesouro Selic

## 📖 Descrição
Este é um simulador de investimento para o **Tesouro Selic** desenvolvido em Python utilizando o **Streamlit**. Ele permite calcular e visualizar a evolução de um investimento com base em:
- Valor inicial investido
- Taxa Selic anual
- Prazo do investimento (em meses)

O simulador também possibilita a comparação entre diferentes cenários e exporta os resultados para Excel.

---

## 🚀 Funcionalidades
- Simulação de rendimento baseado em juros compostos.
- Comparação entre múltiplos cenários de taxas Selic.
- Gráfico interativo para visualização do saldo acumulado ao longo do tempo.
- Tabela detalhada com a evolução mensal do investimento.
- Download dos resultados em formato Excel.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.8+**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Altair**
- **OpenPyXL** (para exportação de Excel)

---

## 📦 Instalação e Execução

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina. Recomendamos utilizar uma versão igual ou superior a 3.8. Além disso, instale o gerenciador de pacotes `pip`.

### Passos para execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/simulador-tesouro-selic.git
   cd simulador-tesouro-selic
   ```

2. Crie e ative um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

5. Acesse o simulador no navegador no endereço:
   ```
   http://localhost:8501
   ```

---

## 📂 Estrutura do Projeto
```plaintext
simulador-tesouro-selic/
├── app.py              # Código principal do simulador
├── requirements.txt    # Lista de dependências do projeto
└── README.md           # Documentação do projeto
```

---

## 🖼️ Demonstração
### Tela Inicial
![image](https://github.com/user-attachments/assets/d092bfc8-e1a2-4499-b535-8cb8ff891f7e)


---

## 🛠️ Como Contribuir
1. Faça um fork do projeto.
2. Crie uma nova branch para a sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Commit suas alterações:
   ```bash
   git commit -m 'Adicionando nova feature'
   ```
4. Faça o push para a sua branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## 📜 Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

## 👤 Autor
**Pedro Henrique Santana Nascimento**  
[LinkedIn](https://www.linkedin.com/in/pedro-henrique-santana-nascimento-1591aa24b/) • [GitHub](https://github.com/PedroHSN98)
