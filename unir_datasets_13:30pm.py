import pandas as pd

periodo1 = pd.read_csv('Monteiro_MYD11A1_LST_2000_2009.csv')
periodo2 = pd.read_csv('Monteiro_MYD11A1_LST_2010_2024.csv')

periodo1.columns = periodo1.columns.str.strip()
periodo2.columns = periodo2.columns.str.strip()

colunas_interesse = ['system:index', 'LST_Celsius', 'data', 'timestamp_utc', '.geo']

periodo1 = periodo1[colunas_interesse]
periodo2 = periodo2[colunas_interesse]

unificado = pd.concat([periodo1, periodo2], ignore_index=True)

unificado['data'] = pd.to_datetime(unificado['data'])
unificado = unificado.sort_values(by='data')

total_dias = unificado.shape[0]
print(f"Total de dias após a união: {total_dias}")

unificado.to_csv('Monteiro_MYD11A1_LST_2000_2019_unificado.csv', index=False)
print('Arquivo unificado salvo como Monteiro_MYD11A1_LST_2000_2024_unificado.csv')
