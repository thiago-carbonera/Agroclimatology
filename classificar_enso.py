import pandas as pd

# Carregar planilha de clima
df_clima = pd.read_csv('agroclimatologia_completa.csv')

# Garantir que data seja formato de tempo
df_clima['data'] = pd.to_datetime(df_clima['data'])

# Criar função que mapeia o histórico oficial da NOAA
def classificar_enso(data):
    ano = data.year
    mes = data.month
    
    # Classificação baseada no Oceanic Niño Index
    if ano == 2018:
        if mes <= 3: return 'La Nina'
        elif mes <= 8: return 'Neutro'
        else: return 'El Nino'
        
    elif ano == 2019:
        if mes <= 6: return 'El Nino'
        else: return 'Neutro'
        
    elif ano == 2020:
        if mes <= 7: return 'Neutro'
        else: return 'La Nina'
        
    elif ano == 2021:
        if mes <= 4: return 'La Nina'
        elif mes <= 7: return 'Neutro'
        else: return 'La Nina'
        
    elif ano == 2022:
        return 'La Nina' # 2022 foi um ano inteiro de La Niña
        
    elif ano == 2023:
        if mes <= 2: return 'La Nina'
        elif mes <= 4: return 'Neutro'
        else: return 'El Nino'
        
    elif ano == 2024:
        if mes <= 4: return 'El Nino'
        elif mes <= 7: return 'Neutro'
        else: return 'La Nina' 
        
    elif ano == 2025:
        # Previsão atual dos modelos climáticos aponta para La Niña
        return 'La Nina' 
        
    return 'Neutro' # Padrão caso algo saia da faixa

# Aplicar a função para criar a nova coluna
print("Analisando o histórico da NOAA e classificando os dias...")
df_clima['fenomeno_enso'] = df_clima['data'].apply(classificar_enso)

# Transformar em números
mapeamento_numerico = {'La Nina': -1, 'Neutro': 0, 'El Nino': 1}
df_clima['fenomeno_enso_numerico'] = df_clima['fenomeno_enso'].map(mapeamento_numerico)

# Salvar a nova versão da planilha
df_clima.to_csv('agroclimatologia_enso_2018_2025.csv', index=False)

print("Sensacional! Coluna de El Niño/La Niña adicionada com sucesso.")