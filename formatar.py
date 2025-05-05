import pandas as pd

def format_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

    df = df.rename(columns={
        'system:index': 'image_index',
        'mean_LST': 'lst_mean_celsius'
    })
    df = df[['date', 'image_index', 'lst_mean_celsius']]

    df.to_csv(output_csv, index=False)
    print(f"CSV formatado e salvo como '{output_csv}'")

input_csv = 'Monteiro_MODIS_LST_buffer20km.csv'
output_csv = 'Monteiro_MODIS_LST_buffer20km_QAmask2.csv'

format_csv(input_csv, output_csv)
