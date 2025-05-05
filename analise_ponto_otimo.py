import json
import pandas as pd
import matplotlib.pyplot as plt

limiar_melhora = 2.0

with open('relatorio_comparativo.json', 'r') as f:
    historico = json.load(f)

df = pd.DataFrame(historico)

df['buffer_km'] = df['nome_teste'].str.extract(r'Buffer (\d+) km').astype(int)

df = df.sort_values(by='buffer_km').reset_index(drop=True)

df['delta_rmse'] = df['rmse'].diff()
df['pct_reducao_rmse'] = -df['delta_rmse'] / df['rmse'].shift(1) * 100

print(df[['buffer_km', 'rmse', 'delta_rmse', 'pct_reducao_rmse']])

ultimo_pct_reducao = df['pct_reducao_rmse'].iloc[-1]
if ultimo_pct_reducao < limiar_melhora:
    print(f"\nA melhoria entre os últimos buffers foi de {ultimo_pct_reducao:.2f}% — menor que o limiar de {limiar_melhora}%: PODE SER O PONTO ÓTIMO.")
else:
    print(f"\nA melhoria entre os últimos buffers foi de {ultimo_pct_reducao:.2f}% — ainda acima do limiar, pode valer continuar testando.")

plt.figure(figsize=(8, 6))
plt.plot(df['buffer_km'], df['rmse'], marker='o', label='RMSE')
plt.plot(df['buffer_km'], df['mae'], marker='o', label='MAE')
plt.plot(df['buffer_km'], df['bias_media'], marker='o', label='Bias')
plt.xlabel('Tamanho do Buffer (km)')
plt.ylabel('Métricas de Erro')
plt.title('Elbow Plot - Buffer vs. Erros')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('elbow_plot_buffer_vs_metricas.png')
plt.show()
