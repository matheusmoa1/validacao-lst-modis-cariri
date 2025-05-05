import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt

def registrar_experimento(nome_teste, merged, pasta_graficos='graficos', arquivo_csv='relatorio_comparativo.csv', arquivo_json='relatorio_comparativo.json'):
    corr, _ = pearsonr(merged['TX'], merged['LST_Celsius'])
    mae = mean_absolute_error(merged['TX'], merged['LST_Celsius'])
    rmse = np.sqrt(mean_squared_error(merged['TX'], merged['LST_Celsius']))
    bias = (merged['LST_Celsius'] - merged['TX']).mean()
    std_diff = (merged['LST_Celsius'] - merged['TX']).std()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    resultado = {
        "timestamp": timestamp,
        "nome_teste": nome_teste,
        "correlacao_pearson": round(corr, 3),
        "mae": round(mae, 3),
        "rmse": round(rmse, 3),
        "bias_media": round(bias, 3),
        "desvio_padrao_diferencas": round(std_diff, 3),
        "total_de_dias": int(merged.shape[0])
    }

    df_resultado = pd.DataFrame([resultado])
    if os.path.exists(arquivo_csv):
        df_resultado.to_csv(arquivo_csv, mode='a', header=False, index=False)
    else:
        df_resultado.to_csv(arquivo_csv, index=False)

    if os.path.exists(arquivo_json):
        with open(arquivo_json, 'r') as f:
            historico = json.load(f)
    else:
        historico = []
    historico.append(resultado)
    with open(arquivo_json, 'w') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

    print(f"Versão '{nome_teste}' registrada no relatório!")

    os.makedirs(pasta_graficos, exist_ok=True)

    gerar_graficos(merged, nome_teste, timestamp, pasta_graficos)

def gerar_graficos(merged, nome_teste, timestamp, pasta_graficos):
    plt.figure(figsize=(8, 6))
    plt.scatter(merged['TX'], merged['LST_Celsius'], alpha=0.5, label='Dias comparados')
    plt.plot([merged['TX'].min(), merged['TX'].max()],
             [merged['TX'].min(), merged['TX'].max()], 'r--', label='y = x (ideal)')
    plt.xlabel('Temperatura Máxima In Loco (°C)')
    plt.ylabel('Temperatura LST Satélite (°C)')
    plt.title(f'{nome_teste} - Dispersão TX x LST\n{timestamp}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{pasta_graficos}/scatter_{nome_teste}_{timestamp}.png')
    plt.close()

    merged['Diferenca'] = merged['LST_Celsius'] - merged['TX']
    plt.figure(figsize=(6, 5))
    plt.boxplot(merged['Diferenca'], vert=True)
    plt.ylabel('Diferença (LST_Celsius - TX) [°C]')
    plt.title(f'{nome_teste} - Boxplot das Diferenças\n{timestamp}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{pasta_graficos}/boxplot_{nome_teste}_{timestamp}.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(pd.to_datetime(merged['Data Medicao']), merged['TX'], label='TX (in loco)', color='blue')
    plt.plot(pd.to_datetime(merged['Data Medicao']), merged['LST_Celsius'], label='LST_Celsius (satélite)', color='orange')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.title(f'{nome_teste} - Séries Temporais\n{timestamp}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{pasta_graficos}/temporal_{nome_teste}_{timestamp}.png')
    plt.close()

    print(f"Gráficos salvos em '{pasta_graficos}/'")

nome_teste = input("Digite o nome do comparativo: ")

merged = pd.read_csv('comparativo_in_loco_vs_satellite_interpolado_pixelCentral.csv')

registrar_experimento(nome_teste, merged)
