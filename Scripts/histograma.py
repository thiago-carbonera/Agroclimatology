import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_csv('Data/produtividade_soja_completa.csv')

# Identificar as colunas que representam os anos (2004 até 2024)
colunas_anos = [str(ano) for ano in range(2004, 2025)]

# Transformar o formato Wide para Long
df_melted = df.melt(id_vars=['nivel', 'codigo_ibge', 'name'], 
                    value_vars=colunas_anos, 
                    var_name='ano', 
                    value_name='produtividade_kg_ha')

# Remover valores nulos (caso alguma cidade não tenha plantado soja em um ano específico)
df_clean = df_melted.dropna(subset=['produtividade_kg_ha'])

# Imprime o número exato de instâncias para você colocar no texto do LaTeX!
total_instancias = len(df_clean)
print("-" * 50)
print(f"✅ Total de instâncias reais (linhas de colheita válidas): {total_instancias}")
print("-" * 50)

# Criar a figura do Histograma
plt.figure(figsize=(10, 6))

# Plota o histograma
sns.histplot(df_clean['produtividade_kg_ha'], bins=30, kde=True, color='#2ca02c')

plt.title('Distribuição da Produtividade da Soja no Estado do Paraná', fontsize=14)
plt.xlabel('Produtividade (kg/ha)', fontsize=12)
plt.ylabel('Frequência (Número de Instâncias)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salvar o gráfico
plt.savefig('Imagens/distribuicao_produtividade.pdf', format='pdf', bbox_inches='tight')

print("Gráfico salvo com sucesso: 'distribuicao_produtividade.pdf'")
plt.show()