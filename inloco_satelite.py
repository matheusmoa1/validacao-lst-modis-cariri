import pandas as pd

satellite = pd.read_csv('Monteiro_MYD11A1_LST_2000_2024.csv')

in_loco = pd.read_csv('dados_A334_H_2007-08-21_2024-12-31.csv', sep=';', skiprows=9, encoding='utf-8-sig')

in_loco.columns = in_loco.columns.str.strip()

satellite['data'] = pd.to_datetime(satellite['data'])
in_loco['Data Medicao'] = pd.to_datetime(in_loco['Data Medicao'])

in_loco_12h = in_loco[in_loco['Hora Medicao'] == 1200]

in_loco_12h.rename(columns={'TEMPERATURA MAXIMA NA HORA ANT. (AUT)(°C)': 'TX'}, inplace=True)

merged = pd.merge(in_loco_12h, satellite, left_on='Data Medicao', right_on='data', how='inner')

merged = merged.dropna(subset=['TX', 'LST_Celsius'])

merged = merged[['Data Medicao', 'Hora Medicao', 'TX', 'LST_Celsius']]

merged.to_csv('comparativo_inloco_12h_vs_satellite.csv', index=False)

total_dias = merged.shape[0]
print(f"Merge finalizado! Total de dias com registros às 12h: {total_dias}")
print("Arquivo salvo como comparativo_inloco_12h_vs_satellite.csv")
