#!/usr/bin/env python
"""
Chat NL↔SQL sobre qualquer CSV com interface Streamlit.

Uso:
    streamlit run challenge_llm.py
"""

import os, duckdb, pandas as pd, ast
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import streamlit as st
load_dotenv()

# ────────────────────────────────────────────────────────────────────────────────
# 1. CRIA TABELA EM DUCKDB (com coluna salario_rank pré‑calculada)
# ────────────────────────────────────────────────────────────────────────────────
def build_duckdb(csv_path: str, table: str, db_file: str = ":memory:") -> SQLDatabase:
    create_table_sql = f"""
    CREATE OR REPLACE TABLE {table} AS
    SELECT *,
        CASE
            WHEN faixa_salarial = 'Acima de R$ 40.001/mês'              THEN 45000.0
            WHEN faixa_salarial = 'de R$ 30.001/mês a R$ 40.000/mês'    THEN 35000.0
            WHEN faixa_salarial = 'de R$ 25.001/mês a R$ 30.000/mês'    THEN 27500.0
            WHEN faixa_salarial = 'de R$ 20.001/mês a R$ 25.000/mês'    THEN 22500.0
            WHEN faixa_salarial = 'de R$ 16.001/mês a R$ 20.000/mês'    THEN 18000.0
            WHEN faixa_salarial = 'de R$ 12.001/mês a R$ 16.000/mês'    THEN 14000.0
            WHEN faixa_salarial = 'de R$ 8.001/mês a R$ 12.000/mês'     THEN 10000.0
            WHEN faixa_salarial = 'de R$ 6.001/mês a R$ 8.000/mês'      THEN  7000.0
            WHEN faixa_salarial = 'de R$ 4.001/mês a R$ 6.000/mês'      THEN  5000.0
            WHEN faixa_salarial = 'de R$ 3.001/mês a R$ 4.000/mês'      THEN  3500.0
            WHEN faixa_salarial = 'de R$ 2.001/mês a R$ 3.000/mês'      THEN  2500.0
            WHEN faixa_salarial = 'de R$ 1.001/mês a R$ 2.000/mês'      THEN  1500.0
            WHEN faixa_salarial = 'Menos de R$ 1.000/mês'               THEN   500.0
            ELSE 0.0
        END AS salario_numerico
    FROM read_csv_auto('{csv_path}');
    """

    db_uri = f"duckdb:///{db_file}" if db_file != ":memory:" else "duckdb:///:memory:"
    db = SQLDatabase.from_uri(db_uri)
    db.run(create_table_sql)

    # Tenta diferentes formas de obter os dados da tabela
    try:
        query_result = db.run(f"SELECT COUNT(*), MAX(salario_numerico) FROM {table}")
        print(f"Query result raw: {repr(query_result)}")
        
        # Tenta parsear como string literal
        if isinstance(query_result, str):
            parsed = ast.literal_eval(query_result)
            total, max_salario = parsed[0]
        else:
            # Se já é uma lista/tupla
            total, max_salario = query_result[0] if isinstance(query_result, list) else query_result
            
    except Exception as e:
        print(f"Erro ao parsear resultado: {e}")
        # Fallback: apenas conta as linhas
        total = len(pd.read_csv(csv_path))
        max_salario = 45000.0
        
    print(f"✅ Tabela '{table}' criada ({total} linhas, max_salario=R$ {max_salario}).")
    return db

# ────────────────────────────────────────────────────────────────────────────────
# 2. CARREGA LLM OpenAI
# ────────────────────────────────────────────────────────────────────────────────
def build_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ────────────────────────────────────────────────────────────────────────────────
# 3. PROMPT DE SISTEMA – garante que "mais bem pago" usa salario_numerico
# ────────────────────────────────────────────────────────────────────────────────
def create_system_prompt() -> str:
    return """
Você é UM TRADUTOR NL→SQL para DuckDB.
Gere apenas o comando SQL (sem nada além dele).

### REGRAS CRÍTICAS
1. Perguntas sobre "maior salário / mais bem paga / melhor remuneração / profissão que paga melhor"
   → SEMPRE calcule AVG(salario_numerico) e ordene DESC. Use valores em reais.
2. Use sempre a tabela `dados`.
3. Nunca devolva explicações, apenas o `SELECT … ;`.
4. Use aspas simples para strings: 'SP', 'Masculino', etc.

### ESQUEMA COMPLETO
- faixa_etaria TEXT (ex: '17-21', '22-25', '26-30', etc.)
- genero TEXT ('Masculino', 'Feminino', 'Prefiro não informar', 'Outro')
- etnia TEXT ('Branca', 'Parda', 'Preta', etc.)
- idade INTEGER
- uf_residencia TEXT ('SP', 'MG', 'PR', 'RJ', 'RS', 'SC', 'DF', 'CE', 'PE', 'BA', etc.)
- nivel_ensino TEXT ('Pós-graduação', 'Graduação/Bacharelado', 'Mestrado', 'Estudante de Graduação', 'Doutorado ou Phd', 'Não tenho graduação formal')
- cargo_atual TEXT (valores principais):
  * 'Analista de Dados/Data Analyst'
  * 'Cientista de Dados/Data Scientist'  
  * 'Engenheiro de Dados/Data Engineer/Data Architect'
  * 'Analista de BI/BI Analyst'
  * 'Analytics Engineer'
  * 'Analista de Negócios/Business Analyst'
  * 'Engenheiro de Machine Learning/ML Engineer/AI Engineer'
  * 'Data Product Manager/ Product Manager (PM/APM/DPM/GPM/PO)'
  * 'Arquiteto de Dados/Data Architect'
- tempo_experiencia_dados TEXT ('de 1 a 2 anos', 'de 3 a 4 anos', 'de 5 a 6 anos', 'Mais de 10 anos', 'Menos de 1 ano', 'Não tenho experiência na área de dados')
- salario_numerico REAL (valor em reais, ex: 10000.0 = R$ 10.000)

### EXEMPLOS
Usuário: Qual a profissão mais bem paga?
SQL:
SELECT cargo_atual,
       AVG(salario_numerico) AS salario_medio
FROM dados
WHERE cargo_atual IS NOT NULL
GROUP BY cargo_atual
ORDER BY salario_medio DESC
LIMIT 5;

Usuário: Mulheres Data Scientists em SP ganham quanto?
SQL:
SELECT AVG(salario_numerico) AS salario_medio
FROM dados
WHERE cargo_atual = 'Cientista de Dados/Data Scientist' 
  AND uf_residencia = 'SP' 
  AND genero = 'Feminino';

Usuário: Compare salários por gênero
SQL:
SELECT genero,
       AVG(salario_numerico) AS salario_medio,
       COUNT(*) AS total
FROM dados
WHERE genero IN ('Masculino', 'Feminino')
GROUP BY genero
ORDER BY salario_medio DESC;
"""

# ────────────────────────────────────────────────────────────────────────────────
# 4. GERA A QUERY SQL
# ────────────────────────────────────────────────────────────────────────────────
def generate_sql_query(llm, user_question: str) -> str:
    # ChatOpenAI → lista de mensagens
    raw = llm.invoke([
        {"role": "system", "content": create_system_prompt()},
        {"role": "user",   "content": user_question}
    ])
    sql_text = raw.content

    # limpa markdown ou lixo eventual
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()
    # pega apenas até o primeiro ';'
    p = sql_text.find(';')
    return sql_text[:p+1] if p != -1 else sql_text

# ────────────────────────────────────────────────────────────────────────────────
# 5. APP STREAMLIT
# ────────────────────────────────────────────────────────────────────────────────
def main():
    # Configurações padrão
    table_name = "dados"
    csv_path = os.path.join("data", "processed", "dataset_salarios_dados.csv")

    st.title("🚀 Challenge State of Data 2024")
    st.markdown("### 💬 Chat Inteligente com Dados de Salários")
    
    st.markdown("""
    **Explore o mercado de trabalho em dados com IA! 🤖📊**
    
    Este sistema utiliza **Large Language Models (LLMs)** para transformar suas perguntas em português 
    em consultas SQL automáticas, analisando dados reais do **State of Data 2024**.
    
    ✨ **Como funciona:** Digite sua pergunta → IA gera SQL → Resultados + Interpretação automática
    """)
    
    st.divider()

    # Lista de perguntas sugeridas
    with st.expander("💡 Exemplos de perguntas que você pode fazer"):
        st.markdown("""
        **🏆 Análises de Salários:**
        1. Qual a profissão mais bem paga na área de dados?
        2. Quanto ganha em média um Data Scientist no Brasil?
        3. Compare os salários entre homens e mulheres na área de dados
        
        **📍 Análises por Região:**
        4. Quais estados pagam os melhores salários para profissionais de dados?
        5. Qual a diferença salarial entre SP e RJ para analistas de dados?
        
        **🎓 Educação e Experiência:**
        6. Como o nível de ensino impacta no salário dos profissionais?
        7. Quanto ganha alguém com mais de 10 anos de experiência em dados?
        
        **👥 Demografia:**
        8. Qual a distribuição salarial por faixa etária?
        9. Como a etnia influencia nos salários da área de dados?
        
        **🔍 Análises Específicas:**
        10. Quantos Engenheiros de Machine Learning ganham acima de R$ 20.000?
        """)

    if not os.path.exists(csv_path):
        st.error(f"❌ Arquivo {csv_path} não encontrado.")
        st.stop()

    with st.spinner("🔄 Carregando dados…"):
        db = build_duckdb(csv_path, table_name)

    llm = build_llm()

    if prompt := st.chat_input("Sua pergunta em PT‑BR…"):
        with st.spinner("🎲 Gerando SQL…"):
            sql = generate_sql_query(llm, prompt)

        with st.expander("🔍 Ver SQL gerado"):
            st.code(sql, language="sql")

        try:
            result = db.run(sql)
        except Exception as e:
            st.error("❌ Erro ao executar SQL: " + str(e))
            return

        # Parse o resultado de forma robusta
        try:
            if isinstance(result, str):
                parsed_result = ast.literal_eval(result)
            else:
                # Se já é uma lista/tupla
                parsed_result = result if isinstance(result, list) else [result]
        except Exception as e:
            st.error(f"❌ Erro ao parsear resultado: {e}")
            st.write(f"Resultado bruto: {repr(result)}")
            return
        
        # Cria DataFrame a partir das tuplas
        if parsed_result:
            # Extrai nomes das colunas do SQL (método simples)
            # Para consultas SELECT, pega tudo entre SELECT e FROM
            sql_upper = sql.upper()
            select_part = sql_upper.split('SELECT')[1].split('FROM')[0]
            # Remove aliases (AS ...) e limpa
            columns = []
            for col in select_part.split(','):
                col = col.strip()
                if ' AS ' in col:
                    col = col.split(' AS ')[1]
                elif '.' in col and ' ' not in col.split('.')[-1]:
                    col = col.split('.')[-1]
                columns.append(col.strip())
            
            df = pd.DataFrame(parsed_result, columns=columns)
        else:
            df = pd.DataFrame()
            
        st.dataframe(df, use_container_width=True)

        # interpretação amigável
        with st.spinner("💡 Interpretando…"):
            interp_prompt = f"""
Explique para um leigo o resultado abaixo, respondendo à pergunta "{prompt}".

Os valores de salário estão em reais (R$). Por exemplo: 10000.0 = R$ 10.000,00 por mês.

Resultado:
{df.to_string(index=False)}

Interprete os valores salariais e explique de forma clara e em português, formatando os valores monetários adequadamente.
"""
            interp = llm.invoke(interp_prompt)
            st.write(interp.content if hasattr(interp, "content") else interp)

# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
