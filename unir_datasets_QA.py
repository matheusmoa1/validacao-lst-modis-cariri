import pandas as pd

df_2000_2009 = pd.read_csv('Monteiro_MYD11A1_LST_QA_2000_2009.csv')
df_2010_2019 = pd.read_csv('Monteiro_MYD11A1_LST_QA_2010_2024.csv')

df = pd.concat([df_2000_2009, df_2010_2019], ignore_index=True)

df['data'] = pd.to_datetime(df['data'])

df_filtrado = df[df['QC_Day'] <= 1].copy()

colunas_desejadas = ['data', 'LST_Celsius']
df_filtrado = df_filtrado[colunas_desejadas]

df_filtrado.to_csv('Monteiro_LST_QA_masked_2000_2024.csv', index=False)

print(f"Exportado com sucesso!")
print(f"Total de dias após filtro QC_Day <= 1: {df_filtrado.shape[0]} dias")
