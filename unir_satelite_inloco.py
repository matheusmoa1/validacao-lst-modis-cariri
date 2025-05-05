import pandas as pd

# Carrega os dados do satélite MODIS (extraídos no GEE)
satellite = pd.read_csv('Monteiro_MYD11A1_LST_2000_2024.csv')
satellite['data'] = pd.to_datetime(satellite['data'])

# Carrega os dados interpolados da estação A334 (Monteiro/PB)
in_loco = pd.read_csv('in_loco_interpolado_13h30.csv')
in_loco['Data Medicao'] = pd.to_datetime(in_loco['Data Medicao'])

# Renomeia a coluna de temperatura in loco para TX (temperatura máxima)
in_loco.rename(columns={'Temp_13h30': 'TX'}, inplace=True)

# Realiza o merge entre os datasets com base na data
merged = pd.merge(in_loco, satellite, left_on='Data Medicao', right_on='data', how='inner')

# Remove linhas com valores ausentes em TX ou LST_Celsius
merged = merged.dropna(subset=['TX', 'LST_Celsius'])

# Seleciona apenas as colunas relevantes para análise
merged = merged[['Data Medicao', 'TX', 'LST_Celsius']]

# Salva a base final como CSV
merged.to_csv('comparativo_in_loco_vs_satellite_interpolado.csv', index=False)

print(f"Finalizado e exportado! Total de dias comparados: {merged.shape[0]}")
