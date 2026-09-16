import pandas as pd

ARQUIVO_CLIMA = '../Data/agroclimatologia_completa.csv'
ARQUIVO_ENSO = '../Data/classificacao_ENSO.csv'
ARQUIVO_SAIDA = '../Data/agroclimatologia_completa_enso.csv'

ANO_INICIAL = 2003
ANO_FINAL = 2025

print("Carregando dataset climático...")

df_clima = pd.read_csv(ARQUIVO_CLIMA)

# Garantir que a coluna data esteja no formato datetime
df_clima['data'] = pd.to_datetime(
    df_clima['fdata'],
    errors='coerce'
)

# Verificar se existem datas inválidas
datas_invalidas = df_clima['data'].isna().sum()

if datas_invalidas > 0:
    print(
        f"Atenção: {datas_invalidas} registros possuem "
        "datas inválidas."
    )

# Criar chaves temporais para associação
df_clima['ano_enso'] = df_clima['data'].dt.year
df_clima['mes_enso'] = df_clima['data'].dt.month

print("Carregando tabela histórica do ONI...")

df_enso = pd.read_csv(ARQUIVO_ENSO)

# Padronizar nomes das colunas
df_enso.columns = df_enso.columns.str.strip()

# Garantir tipos corretos
df_enso['Year'] = pd.to_numeric(
    df_enso['Year'],
    errors='coerce'
).astype('Int64')

df_enso['ONI'] = pd.to_numeric(
    df_enso['ONI'],
    errors='coerce'
)

df_enso['Periodo'] = df_enso['Periodo'].astype(str).str.strip()
df_enso['Fenomeno'] = df_enso['Fenomeno'].astype(str).str.strip()

# Filtrar somente o período utilizado no TCC (2003-2024)
df_enso = df_enso[
    (df_enso['Year'] >= ANO_INICIAL) &
    (df_enso['Year'] <= ANO_FINAL)
].copy()

print(
    f"Tabela ENSO carregada: "
    f"{df_enso['Year'].min()} até {df_enso['Year'].max()}"
)

# Associar cada período ao mês central
meses_centrais = {
    'DJF': 1,
    'JFM': 2,
    'FMA': 3,
    'MAM': 4,
    'AMJ': 5,
    'MJJ': 6,
    'JJA': 7,
    'JAS': 8,
    'ASO': 9,
    'SON': 10,
    'OND': 11,
    'NDJ': 12
}

df_enso['mes_enso'] = df_enso['Periodo'].map(meses_centrais)

# Verificar se todos os períodos foram reconhecidos
periodos_nao_reconhecidos = df_enso[
    df_enso['mes_enso'].isna()
]['Periodo'].unique()

if len(periodos_nao_reconhecidos) > 0:
    raise ValueError(
        f"Períodos não reconhecidos: "
        f"{periodos_nao_reconhecidos}"
    )

# Renomear colunas para facilitar o merge
df_enso = df_enso.rename(columns={
    'Year': 'ano_enso',
    'ONI': 'oni',
    'Fenomeno': 'fenomeno_enso'
})

# Selecionando apenas as colunas necessárias

df_enso = df_enso[
    [
        'ano_enso',
        'mes_enso',
        'oni',
        'fenomeno_enso'
    ]
].copy()

# Verificar duplicidades
duplicidades = df_enso.duplicated(
    subset=['ano_enso', 'mes_enso']
).sum()

if duplicidades > 0:
    raise ValueError(
        f"Foram encontradas {duplicidades} duplicidades "
        "na chave ano + mês da tabela ENSO."
    )

print("Tabela ENSO validada com sucesso.")
print(f"Total de referências mensais: {len(df_enso)}")

print("Associando os dados do ENSO ao dataset climático...")

# Se o script for executado novamente, remove as colunas
# antigas para evitar nomes como oni_x, oni_y etc.
colunas_enso_antigas = [
    'oni',
    'fenomeno_enso'
]

df_clima = df_clima.drop(
    columns=[
        coluna for coluna in colunas_enso_antigas
        if coluna in df_clima.columns
    ]
)

# Associação por ano e mês
df_clima = df_clima.merge(
    df_enso,
    on=['ano_enso', 'mes_enso'],
    how='left',
    validate='many_to_one'
)

registros_sem_enso = df_clima['oni'].isna().sum()

if registros_sem_enso > 0:
    print(
        f"Atenção: {registros_sem_enso} registros "
        "ficaram sem correspondência de ENSO."
    )
    print(
        "Esses registros permanecerão como NaN."
    )
else:
    print("Todos os registros climáticos receberam dados do ENSO.")

df_clima = df_clima.drop(
    columns=['ano_enso', 'mes_enso']
)

# Salvar dataset final
df_clima.to_csv(
    ARQUIVO_SAIDA,
    index=False
)

print("\nDataset salvo com sucesso!")
print(f"Arquivo: {ARQUIVO_SAIDA}")
print(f"Total de registros: {len(df_clima)}")

print("\n===== AUDITORIA ENSO =====")

auditoria = (
    df_clima
    .groupby(['oni', 'fenomeno_enso'], dropna=False)
    .size()
    .reset_index(name='quantidade_registros')
    .sort_values('oni')
)

print(auditoria.to_string(index=False))