import pandas as pd

satellite_csv = 'Monteiro_MODIS_LST_buffer20km_QAmask2.csv'  # ou o com QA
output_csv = 'comparativo_in_loco_vs_satellite_no_QA_25km.csv'

satellite = pd.read_csv(satellite_csv)
satellite['date'] = pd.to_datetime(satellite['date']) 

in_loco = pd.read_csv('dados_82792_D_1980-01-01_2019-01-01.csv', sep=';', skiprows=9, encoding='utf-8-sig')
in_loco.columns = in_loco.columns.str.strip()
in_loco['Data Medicao'] = pd.to_datetime(in_loco['Data Medicao'])
in_loco.rename(columns={'TEMPERATURA MAXIMA, DIARIA(°C)': 'TX'}, inplace=True)

merged = pd.merge(in_loco, satellite, left_on='Data Medicao', right_on='date', how='inner')

merged = merged.dropna(subset=['TX', 'lst_mean_celsius'])

merged = merged.rename(columns={'lst_mean_celsius': 'LST_Celsius'})

merged = merged[['Data Medicao', 'TX', 'LST_Celsius']]

merged.to_csv(output_csv, index=False)
print(f'Finalizado e exportado como {output_csv}')
