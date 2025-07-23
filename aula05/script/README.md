# 🚀 Challenge State of Data 2024 - Chat NL↔SQL

Um aplicativo Streamlit que permite fazer perguntas em **português** sobre dados de salários da área de dados e receber respostas automáticas através de **Large Language Models (LLMs)**.

## 🎯 Funcionalidades

- **Chat Inteligente**: Faça perguntas em linguagem natural sobre salários, profissões e mercado de dados
- **Conversão Automática**: IA converte suas perguntas em consultas SQL otimizadas
- **Análise Instantânea**: Resultados tabulares + interpretação em português
- **Dados Reais**: Base do State of Data 2024 com informações salariais brasileiras

## 🛠️ Como Funciona

1. **Entrada**: Você digita uma pergunta em português (ex: "Qual a profissão mais bem paga?")
2. **IA**: GPT-4o-mini converte sua pergunta em SQL DuckDB
3. **Execução**: Query é executada no banco de dados em memória
4. **Saída**: Tabela com resultados + explicação em linguagem natural

## 📊 Dados Disponíveis

O sistema analisa informações sobre profissionais de dados incluindo:
- **Cargos**: Data Scientist, Data Analyst, Data Engineer, etc.
- **Salários**: Convertidos automaticamente para valores numéricos em R$
- **Demografia**: Gênero, etnia, faixa etária
- **Localização**: Estados brasileiros
- **Educação**: Níveis de ensino e experiência

## 🚀 Como Usar

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Configuração
1. Crie um arquivo `.env` com sua chave da OpenAI:
```env
OPENAI_API_KEY=sua_chave_aqui
```

2. Certifique-se que o arquivo de dados existe em:
```
data/processed/dataset_salarios_dados.csv
```

### Executar
```bash
streamlit run challenge_llm.py
```

## 💡 Exemplos de Perguntas

- "Qual a profissão mais bem paga na área de dados?"
- "Quanto ganha em média um Data Scientist no Brasil?"
- "Compare os salários entre homens e mulheres"
- "Quais estados pagam os melhores salários?"
- "Como o nível de ensino impacta no salário?"

## 🔧 Arquitetura Técnica

- **Frontend**: Streamlit para interface web
- **LLM**: OpenAI GPT-4o-mini para NL→SQL
- **Database**: DuckDB em memória para consultas rápidas
- **Dados**: CSV processado com coluna `salario_numerico` calculada
- **Framework**: LangChain para integração com LLM

## 📈 Recursos Especiais

- **Mapeamento Salarial**: Converte faixas textuais em valores numéricos automaticamente
- **Consultas Otimizadas**: Prompt especializado para gerar SQL eficiente
- **Interpretação IA**: Explicações automáticas dos resultados em português
- **Interface Amigável**: Sugestões de perguntas e visualização clara dos dados 