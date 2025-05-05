import pandas as pd

# Leitura do CSV bruto com dados horários da estação A334
in_loco = pd.read_csv('dados_A334_H_2007-08-21_2024-12-31.csv', sep=';', skiprows=9, encoding='utf-8-sig')

# Padroniza os nomes das colunas
in_loco.columns = in_loco.columns.str.strip()

# Converte a coluna de data para datetime
in_loco['Data Medicao'] = pd.to_datetime(in_loco['Data Medicao'])

# Seleciona apenas as colunas relevantes
in_loco = in_loco[['Data Medicao', 'Hora Medicao', 'TEMPERATURA MAXIMA NA HORA ANT. (AUT)(°C)']]

# Renomeia a coluna para facilitar a manipulação
in_loco.rename(columns={'TEMPERATURA MAXIMA NA HORA ANT. (AUT)(°C)': 'Temp_C'}, inplace=True)

# Filtra as medições das 13h e 14h
hora_13 = in_loco[in_loco['Hora Medicao'] == 1300]
hora_14 = in_loco[in_loco['Hora Medicao'] == 1400]

# Junta os dois dataframes pela data
merged = pd.merge(hora_13, hora_14, on='Data Medicao', suffixes=('_13h', '_14h'))

# Interpolação simples (média das temperaturas das 13h e 14h)
merged['Temp_13h30'] = ((merged['Temp_C_13h'] + merged['Temp_C_14h']) / 2).round(2)

# Seleciona apenas a data e a temperatura interpolada final
interpolado = merged[['Data Medicao', 'Temp_13h30']]

# Salva o resultado em CSV
interpolado.to_csv('in_loco_interpolado_13h30.csv', index=False)

# Mensagem final
print(f"Interpolação finalizada! Total de dias interpolados: {interpolado.shape[0]}")
