import pandas as pd
import numpy as np

# Carregar a planilha base antiga (2004 a 2017)
df_principal = pd.read_csv('produtividade_soja.csv')

# Lista com as novas produções
anos_novos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Loop para processar e juntar cada arquivo anualmente
for ano in anos_novos:
    nome_arquivo = f'producao_{ano}_parana.csv'
    
    try:
        # Lê o CSV do ano específico
        df_ano = pd.read_csv(nome_arquivo)
        
        # Substitui o '-' por NaN e converte para decimal
        df_ano[str(ano)] = df_ano[str(ano)].replace('-', np.nan).astype(float)
        
        # Remove a coluna 'Município' para não duplicar, mantendo apenas o 'name'
        if 'Município' in df_ano.columns:
            df_ano = df_ano.drop(columns=['Município'])
            
        # Cola a nova coluna de ano usando o codigo_ibge como âncora
        # how='left' garante que a tabela final mantenha a mesma estrutura da original
        df_principal = pd.merge(df_principal, df_ano, on='codigo_ibge', how='left')
        
        print(f"Sucesso: Dados de {ano} adicionados!")
        
    except FileNotFoundError:
        print(f"Aviso: O arquivo {nome_arquivo} não foi encontrado na pasta. Pulando...")

# Salva o Dataset
df_principal.to_csv('produtividade_soja_2004_2024.csv', index=False)

print("\nSensacional! Planilha de produtividade unificada de 2004 a 2024 pronta para uso.")