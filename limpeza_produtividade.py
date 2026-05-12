import pandas as pd

# Carrega o CSV
df_brasil = pd.read_csv('Produtividade_soja_2024.csv', sep=';', skiprows=4)

# Renomeia a coluna do IBGE para o padrão
df_brasil = df_brasil.rename(columns={'Cód.': 'codigo_ibge', 'Soja (em grão)': '2024'})

# Remove qualquer linha vazia ou inútil que não tenha o código do município
df_brasil = df_brasil.dropna(subset=['codigo_ibge'])

# Filtro para pegar apenas o Paraná
df_parana = df_brasil[df_brasil['codigo_ibge'].astype(str).str.startswith('41')]

# Salva o arquivo
df_parana.to_csv('producao_2024_parana.csv', index=False)

print(f"Limpeza concluída! De {len(df_brasil)} municípios no arquivo, sobraram {len(df_parana)} do Paraná.")