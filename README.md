# Challenge State of Data 2024-2025 🚀

Bem-vindos e bem-vindas padawans de todas as partes do BRÉZIU!! Este repositório contém as aulas e materiais da **Trilha Challenge State of Data 2024-2025** da DataHackers, um projeto educacional focado em análise de dados e ciência de dados usando Python e Pandas, com o objetivo de deixá-los preparados para participarem do Challenge State of Data e concorrer a prêmios muito maneiros!

### Dataset
- **Fonte**: [State of Data Brazil 2024-2025 - Kaggle](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)
- **Tamanho**: 5.217 respondentes com 403 colunas
- **Formato**: CSV
- **Período**: 2024-2025

### Seções do Questionário
O dataset é dividido em 8 seções principais:

1. **Dados demográficos** - Idade, gênero, localização, formação
2. **Dados sobre carreira** - Situação profissional, cargo, salário
3. **Desafios dos gestores** - Responsabilidades e desafios de liderança
4. **Conhecimentos na área de dados** - Ferramentas, linguagens, fontes de dados
5. **Objetivos na área de dados** - Metas e aspirações profissionais
6. **Conhecimentos em Engenharia de Dados/DE** - Pipelines, ETL, arquitetura
7. **Conhecimentos em Análise de Dados/DA** - Dashboards, BI, estatística
8. **Conhecimentos em Ciências de Dados/DS** - Machine Learning, modelos preditivos

## 🎯 Objetivos da Trilha

- Aprender **limpeza e organização de dados** com Pandas
- Desenvolver habilidades em **análise exploratória de dados (EDA)**
- Praticar **visualização de dados** com matplotlib, seaborn e plotly
- Aplicar Machine Learning nas suas análises
- Aproveitar o grande HYPE das llms para deixar suas análises matadoras
- Aplicar metodologias como **CRISP-DM** para projetos de dados
- Criar insights relevantes sobre o mercado brasileiro de dados

## 📁 Estrutura do Projeto

```
challenge-data-hackers-2025/
├── aula01/                                    # Aula 1 - Pandas e Organização do Dataset
│   ├── script/
│   │   ├── Aula 01 - Pandas - Organizacao do Dataset.ipynb
│   │   ├── data/
│   │   │   └── raw/                          # Dados originais
│   │   │       └── Final Dataset - State of Data 2024 - Kaggle - df_survey_2024.zip
│   │   ├── img/                              # Imagens dos notebooks
│   │   │   ├── header.png
│   │   │   ├── mamilos.jpg
│   │   │   └── para_tudo.png
│   │   └── requirements.txt                  # Dependências do projeto
│   └── Aula 01 - Pandas - Organizacao do Dataset.pdf
├── aula02/                                   # Aula 2 - Análise Exploratória de Dados
├── aula03/                                   # Aula 3 - 
├── aula04/                                   # Aula 4 - 
├── aula05/                                   # Aula 5 - 
└── README.md
```

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Jupyter Notebook ou JupyterLab

### Instalação das Dependências

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd challenge-data-hackers-2025
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
cd aula01/script
pip install -r requirements.txt
```

### Download do Dataset

Você pode baixar o dataset de duas formas:

#### Opção 1: Download Manual
1. Acesse o [dataset no Kaggle](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)
2. Baixe o arquivo e extraia em `aula01/script/data/raw/`

#### Opção 2: Usando KaggleHub (já incluído no requirements.txt)
```python
import kagglehub
path = kagglehub.dataset_download("datahackers/state-of-data-brazil-20242025")
```

## 🚀 Como Usar

1. Navegue até a pasta da aula desejada:
```bash
cd aula01/script
```

2. Inicie o Jupyter Notebook:
```bash
jupyter notebook
```

3. Abra o arquivo `.ipynb` correspondente à aula

4. Execute as células sequencialmente para acompanhar a aula

## 📚 Conteúdo das Aulas

### Aula 01 - Pandas e Organização do Dataset ✅
**Objetivos:**
- Introdução ao Pandas e estruturas de dados
- Carregamento e exploração inicial do dataset
- Limpeza e organização dos dados
- Renomeação de colunas para facilitar análises
- Separação de dados por seções do questionário
- Tratamento de valores faltantes (NaN)

**Principais Métodos Aprendidos:**
- `pd.read_csv()` - Carregamento de dados
- `.head()` - Visualização das primeiras linhas
- `.info()` - Informações sobre o DataFrame
- `.shape` - Dimensões do dataset
- `.columns` - Lista de colunas
- `.rename()` - Renomeação de colunas
- `.value_counts()` - Contagem de frequências

### Aula 02 - Análise Exploratória de Dados 🔄
*Em desenvolvimento*

### Aula 03 🔄
*Em desenvolvimento*

## 🛠️ Dependências Principais

- **pandas** >= 1.5.0 - Manipulação e análise de dados
- **numpy** >= 1.21.0 - Computação numérica
- **matplotlib** >= 3.5.0 - Visualização de dados
- **seaborn** >= 0.11.0 - Visualização estatística
- **plotly** >= 5.0.0 - Visualizações interativas
- **scipy** >= 1.7.0 - Computação científica
- **jupyter** >= 1.0.0 - Ambiente de notebooks
- **kagglehub** - Download de datasets do Kaggle

## 📈 Metodologia CRISP-DM

O projeto segue a metodologia CRISP-DM (Cross-Industry Standard Process for Data Mining):

1. **Business Understanding** - Compreender objetivos da análise
2. **Data Understanding** - Explorar e conhecer os dados
3. **Data Preparation** - Limpeza e preparação dos dados ← *Aula 01*
4. **Modeling** - Aplicação de técnicas de análise
5. **Evaluation** - Avaliação dos resultados
6. **Deployment** - Implementação e comunicação dos insights

## 🤝 Contribuições

Este é um projeto educacional da comunidade DataHackers. Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-analise`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova análise'`)
4. Push para a branch (`git push origin feature/nova-analise`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é mantido pela comunidade DataHackers para fins educacionais.

## 🔗 Links Úteis

- [Dataset no Kaggle](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-20242025)
- [Live DataHackers sobre CRISP-DM](https://www.youtube.com/live/kDTlX45VEUo?si=FKxn6UbLWgs9Bo1n)
- [Aula Let's Data sobre CRISP-DM](https://youtu.be/mhPATD8S6D0?si=2EDv6Iv_qw1t-j7C)
- [Comunidade DataHackers](https://datahackers.com.br/)

---

**Feito com ❤️ pela comunidade DataHackers**

*"Ganhem esse SWITCH DOIS!!!"* 🎮 