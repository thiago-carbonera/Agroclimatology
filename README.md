# Agroclimatology

Repositório com os scripts do TCC em Ciência da Computação focado em predição de produtividade da soja no estado do Paraná, a partir de dados agroclimáticos e variáveis macroclimáticas (ENSO).

## Objetivo
Construir uma base consolidada para modelagem preditiva em séries temporais, cruzando:

- variáveis climáticas históricas (features);
- produtividade agrícola municipal (target);
- sinal climático de El Nino/La Nina (feature de contexto).

## Escopo dos Dados
O projeto trabalha com dados em nível municipal, com integração temporal entre diferentes fontes.

- Dados agroclimáticos diários (NASA POWER).
- Dados de produtividade de soja por município (IBGE/SIDRA - PAM).
- Classificação ENSO para enriquecer o conjunto de variáveis.

## Fontes de Dados

Os dados brutos foram extraídos de fontes públicas e bases abertas, garantindo transparência e reprodutibilidade:

- **Produtividade da Soja (Target — 2018-2024):** Dados anuais de rendimento médio (kg/ha) a nível municipal, obtidos através do Instituto Brasileiro de Geografia e Estatística (IBGE), via pesquisa Produção Agrícola Municipal (PAM). Extração feita através do sistema SIDRA, [Tabela 5457](https://sidra.ibge.gov.br/tabela/5457), com filtro para soja, área colhida em hectares, por município.
- **Dados Agroclimáticos (Features — 2021 em diante):** Séries temporais climáticas diárias do estado do Paraná, coletadas via API NASA POWER. O script `agroclimatologia.py` realiza a coleta automatizada.
- **Dataset Base Histórico (Features e Target — até 2017):** Dados históricos de agroclimatologia e produtividade, obtidos a partir de dataset público no Kaggle: [Agroclimatology Data of the State of Paraná, Brazil](https://www.kaggle.com/datasets/hugovallejo/agroclimatology-data-of-the-state-of-paran-br).

## Tecnologias
- Python
- pandas
- numpy
- requests

## Estrutura do Repositório
- `agroclimatologia.py`: coleta dados diários da API NASA POWER em lotes de variáveis e gera `agroclimatology_2021_2025.csv`.
- `concat_agroclimatologia.py`: concatena bases climáticas antiga e nova, padroniza data, ordena e remove duplicatas.
- `classificar_enso.py`: adiciona colunas de classificação ENSO categórica e numérica ao dataset climático.
- `limpeza_produtividade.py`: limpa os arquivos de produtividade de 2018 a 2024, renomeia colunas e filtra apenas municípios do Paraná.
- `concat_producao.py`: concatena em lote os dados anuais de produtividade e consolida no dataset histórico.

## Requisitos
- Python 3.10+
- Dependências:

```bash
pip install pandas numpy requests
```

## Como Executar

### Configurar Ambiente Virtual

Primeiro, crie e ative um ambiente virtual Python:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install pandas numpy requests
```

### Executar os Scripts

Abaixo está o fluxo sugerido. Ajuste nomes de arquivos conforme sua base local.

1. Coletar/atualizar dados climáticos:

```bash
python agroclimatologia.py
```

2. Concatenar histórico climático:

```bash
python concat_agroclimatologia.py
```

3. Enriquecer com ENSO:

```bash
python classificar_enso.py
```

4. Limpar a base anual de produtividade:

```bash
python limpeza_produtividade.py
```

5. Consolidar produtividade histórica:

```bash
python concat_producao.py
```

## Reprodutibilidade
Arquivos grandes de dados (`*.csv`, `*.xlsx`) podem ficar fora do repositório remoto para evitar limite de tamanho. O foco deste repositório é manter a lógica de coleta, limpeza e preparação dos dados.
