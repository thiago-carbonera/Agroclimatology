import pandas as pd

# Carregar as duas planilhas
df_clima_antigo = pd.read_csv('agroclimatology.csv')
df_clima_novo = pd.read_csv('agroclimatology_2021_2025.csv')

# Salvar a ordem das colunas da planilha nova
ordem_padrao = df_clima_novo.columns.tolist()

# Juntar as tabelas
df_clima_completo = pd.concat([df_clima_antigo, df_clima_novo], ignore_index=True)

# Reordenar o DataFrame
df_clima_completo = df_clima_completo[ordem_padrao]

# Consertar o formato da data
df_clima_completo['data'] = pd.to_datetime(df_clima_completo['data'].astype(str), format='%Y%m%d')

# Ordenar a tabela
df_clima_completo = df_clima_completo.sort_values(by=['data', 'codigo_ibge'])

# Remover duplicatas considerando data e município
df_clima_completo = df_clima_completo.drop_duplicates(subset=['data', 'codigo_ibge'], keep='last')

# Salvar o DataFrame unificado
df_clima_completo.to_csv('agroclimatologia_completa_2018_2025.csv', index=False)

print("Sucesso! Planilhas unificadas, datas ajustadas e todos os municípios preservados.")