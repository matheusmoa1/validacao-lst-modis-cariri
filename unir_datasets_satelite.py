import pandas as pd

sat1 = pd.read_csv('Monteiro_LST_2000_2009_25KM.csv')
sat2 = pd.read_csv('Monteiro_LST_2010_2019_25KM.csv')

sat1['data'] = pd.to_datetime(sat1['data'])
sat2['data'] = pd.to_datetime(sat2['data'])

satellite = pd.concat([sat1, sat2], ignore_index=True)

satellite = satellite.sort_values(by='data').reset_index(drop=True)

satellite = satellite.drop_duplicates(subset=['data'])

print(satellite.head())
print(satellite.tail())
print(f'Total de dias após unir: {satellite.shape[0]}')


satellite.to_csv('Monteiro_LST_2000_2019_25KM_unificado.csv', index=False)