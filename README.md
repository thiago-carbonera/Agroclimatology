# Agroclimatology

Repositório com os scripts desenvolvidos no Trabalho de Conclusão de Curso (TCC) em Ciência da Computação, cujo objetivo é apoiar a atualização, a preparação e o enriquecimento de dados utilizados na predição da produtividade da soja no estado do Paraná.

O projeto utiliza dados agroclimáticos diários, séries históricas de produtividade agrícola municipal e informações macroclimáticas relacionadas ao fenômeno ENSO (*El Niño–Oscilação Sul*). O conjunto consolidado serve como base para a etapa de engenharia de atributos (*Feature Engineering*), aplicação de janelamento temporal e treinamento de modelos de aprendizado de máquina (*Machine Learning*).

A versão modificada e ampliada dos dados utilizada na pesquisa pode ser referenciada como **AgroClima-PR**.

## Objetivo

Atualizar e preparar um conjunto de dados público de agroclimatologia e produtividade agrícola, ampliando sua cobertura temporal e incorporando informações macroclimáticas para estudos de modelagem preditiva da produtividade da soja no Paraná.

As principais etapas contempladas são:
* Atualização das séries históricas de produtividade da soja (IBGE/PAM);
* Ampliação da cobertura temporal dos dados agroclimáticos diários (NASA POWER);
* Inclusão e mapeamento de anomalias oceânicas relacionadas ao fenômeno ENSO (índice ONI);
* Padronização, limpeza e alinhamento espaço-temporal das tabelas;
* Preparação da estrutura de dados para janelamento e modelagem preditiva supervisionada.

## Escopo dos Dados

O projeto opera em nível municipal e integra bases com diferentes granularidades temporais:

* **Tabela de Produtividade Agrícola (`target`):** Apresenta os valores anuais de produtividade da soja por município, expressos em quilogramas por hectare (kg/ha).
* **Tabela Agroclimática (`features`):** Reúne observações meteorológicas e ambientais diárias associadas aos municípios paranaenses.
* **Variáveis Macroclimáticas (ENSO):** Informação complementar às variáveis meteorológicas locais. No processo de previsão com janelamento, a condição mais recente no momento da predição é empregada como atributo de contexto.

As tabelas permanecem estruturalmente isoladas e são unificadas durante o pipeline por meio do código do município (`codigo_ibge`) e do ano de safra correspondente.

## Fontes de Dados

Os dados brutos provêm de fontes públicas e abertas, assegurando total transparência e reprodutibilidade:

* **Produtividade da Soja (Target — até 2024):** Extraída via [SIDRA / IBGE](https://sidra.ibge.gov.br/tabela/5457) a partir da Pesquisa Agrícola Municipal (PAM - Tabela 5457), considerando a área colhida e o rendimento médio da soja nos municípios do Paraná.
* **Dados Agroclimáticos (Features — até 2025):** Séries meteorológicas diárias obtidas através da API da plataforma [NASA POWER](https://power.larc.nasa.gov/data-access-viewer/) via script automatizado.
* **Dataset Base de Referência:** Ponto de partida disponível no Kaggle: [Agroclimatology Data of the State of Paraná, Brazil](https://www.kaggle.com/datasets/hugovallejo/agroclimatology-data-of-the-state-of-paran-br) (Vallejo et al.).
* **Índice ENSO:** Classificações obtidas com base nas anomalias do *Oceanic Niño Index* (ONI) disponibilizadas pela [NOAA](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php).

### Codificação ENSO

O fenômeno é integrado à tabela agroclimática sob duas representações (`fenomeno_enso` e `fenomeno_enso_numerico`):

| Condição ENSO | Valor Numérico |
| La Niña | `-1` |
| Neutro | `0` |
| El Niño | `1` |

## Estrutura do Repositório

```text
Agroclimatology/
├── Scripts/
│   ├── agroclimatologia.py        # Coleta de dados via API NASA POWER
│   ├── concat_agroclimatologia.py # Concatenação, ordenação e limpeza de duplicatas climáticas
│   ├── classificar_enso.py        # Integração e mapeamento do fenômeno ENSO
│   ├── limpeza_produtividade.py   # Limpeza e padronização das planilhas anuais do IBGE
│   └── concat_producao.py         # Consolidação da série histórica de produtividade
├── .gitignore                     # Filtro de arquivos binários, venv e datasets
├── README.md                      # Documentação do projeto
└── requirements.txt               # Dependências do projeto

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
python Scripts/agroclimatologia.py
```

2. Concatenar histórico climático:

```bash
python Scripts/concat_agroclimatologia.py
```

3. Enriquecer com ENSO:

```bash
python Scripts/classificar_enso.py
```

4. Limpar a base anual de produtividade:

```bash
python Scripts/limpeza_produtividade.py
```

5. Consolidar produtividade histórica:

```bash
python Scripts/concat_producao.py
```

## Reprodutibilidade
Arquivos grandes de dados (`*.csv`, `*.xlsx`)  ficar fora do repositório remoto para evitar limite de tamanho. O foco deste repositório é manter a lógica de coleta, limpeza e preparação dos dados.