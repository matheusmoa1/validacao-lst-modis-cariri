import ee

def get_modis_lst(start_date, end_date, geometry, buffer_km=20):
    region = geometry.buffer(buffer_km * 1000)

    collection = ee.ImageCollection('MODIS/061/MOD11A1') \
        .filterDate(start_date, end_date) \
        .filterBounds(region)

    def mask_quality(image):
        quality = image.select('QC_Day')
        mask = quality.lte(1)  # Aceitando QA 0 e 1 (boa qualidade + perfeita)
        lst = image.select('LST_Day_1km').multiply(0.02).subtract(273.15).rename('LST_Celsius')
        
        return lst.updateMask(mask).set('system:time_start', image.get('system:time_start'))

    masked_collection = collection.map(mask_quality)
    return masked_collection
