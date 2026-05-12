import requests
import pandas as pd
import time
import os

def get_nasa_batch(lat, lon, start, end, vars_list):
    """Realiza a requisição de um lote específico de variáveis."""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": ",".join(vars_list),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Transforma o dicionário de parâmetros em DataFrame
        return pd.DataFrame(response.json()['properties']['parameter'])
    else:
        print(f"Erro no lote: {response.status_code}")
        return None

# Divisão das 34 variáveis em dois grupos para evitar o erro
vars_1 = [
    "T2M", "T2M_MAX", "T2M_MIN", "T2M_RANGE", "TS", "T2MDEW", "T2MWET", 
    "QV2M", "RH2M", "PRECTOTCORR", "PS", "WS2M", "WS2M_MAX", "WS2M_MIN", 
    "WS2M_RANGE", "WS10M", "WS10M_MAX"
]
vars_2 = [
    "WS10M_MIN", "WS10M_RANGE", "WS50M", "WS50M_MAX", "WS50M_MIN", 
    "WS50M_RANGE", "GWETTOP", "GWETROOT", "GWETPROF", "ALLSKY_SFC_SW_DWN", 
    "CLRSKY_SFC_SW_DWN", "TOA_SW_DWN", "ALLSKY_SFC_PAR_TOT", 
    "CLRSKY_SFC_PAR_TOT", "ALLSKY_SFC_UVA", "ALLSKY_SFC_UVB", "ALLSKY_SFC_UV_INDEX"
]

# Carregar coordenadas dos municípios
try:
    df_base = pd.read_csv("agroclimatology.csv")
    municipios = df_base[['codigo_ibge', 'latitude', 'longitude']].drop_duplicates()
except FileNotFoundError:
    print("Erro: Arquivo 'agroclimatology.csv' não encontrado.")
    exit()

novos_dados = []
start_date, end_date = "20210101", "20251231"

print(f"Iniciando coleta (2021-2025) para {len(municipios)} municípios...")

for index, row in municipios.iterrows():
    lat, lon, cod = row['latitude'], row['longitude'], int(row['codigo_ibge'])
    print(f"Processando IBGE: {cod}...")

    # Coleta os dois lotes
    df1 = get_nasa_batch(lat, lon, start_date, end_date, vars_1)
    time.sleep(0.5)
    df2 = get_nasa_batch(lat, lon, start_date, end_date, vars_2)

    if df1 is not None and df2 is not None:
        # Une as colunas dos dois lotes pelo índice (data)
        df_mun = pd.concat([df1, df2], axis=1).reset_index().rename(columns={'index': 'data'})
        
        # Adiciona metadados necessários
        df_mun['codigo_ibge'] = cod
        df_mun['latitude'] = lat
        df_mun['longitude'] = lon
        
        novos_dados.append(df_mun)
    
    # Respeita o rate limit global da API
    time.sleep(1.0) 

# Salva o resultado final
if novos_dados:
    final_df = pd.concat(novos_dados)
    final_df.to_csv("agroclimatology_2021_2025.csv", index=False)
    print(f"\n--- SUCESSO! ---\nArquivo 'agroclimatology_2021_2025.csv' com {len(final_df)} linhas gerado.")