import ee
from gee_utils import initialize_gee
from pdi_pipeline import get_modis_lst

initialize_gee()

geometry = ee.Geometry.Point([-37.12472221, -7.89444444])

collection = get_modis_lst('2000-01-01', '2019-12-31', geometry, buffer_km=20)

def extract_daily_means(image):
    timestamp = image.get('system:time_start')
    
    mean = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geometry.buffer(20000),
        scale=1000
    ).get('LST_Celsius')

    return ee.Feature(None, {
        'timestamp': timestamp,    
        'mean_LST': mean,
        'has_time': timestamp,
        'has_data': mean
    })

feature_collection = collection.map(extract_daily_means) \
    .filter(ee.Filter.notNull(['has_time', 'has_data']))

print("Quantidade de imagens após cálculo da média:", feature_collection.size().getInfo())

task = ee.batch.Export.table.toDrive(
    collection=feature_collection,
    description='Export_Monteiro_MODIS_LST',
    folder='GEE_EXPORT',                      
    fileNamePrefix='Monteiro_MODIS_LST_buffer20km',
    fileFormat='CSV'
)

task.start()
print("Exportação iniciada!")
