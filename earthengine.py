import ee
import time


ee.Authenticate()
ee.Initialize()


def maskS2clouds(image):
    qa = image.select('QA60')
    cloudMask = qa.bitwiseAnd(1 << 10).Or(qa.bitwiseAnd(1 << 11))
    return image.updateMask(cloudMask.Not())

def get_image(Task_Name,lon,lat,area,start_date,end_date):
    
        point = ee.Geometry.Point([lon, lat])
        small_region = point.buffer(area*1000).bounds() 

        collection = (ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
                    .filterBounds(small_region)
                    .filterDate(start_date, end_date)
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                    .map(maskS2clouds) 
                    .sort('system:time_start', False))

        num_images = collection.size().getInfo()
        print("Number of images:", num_images)

        if num_images > 0:
            image_list = collection.toList(num_images) 
            print(f"Starting export of {num_images} images...")
            for i in range(num_images):
                image = ee.Image(image_list.get(i))
                date_str = image.date().format('YYYY-MM-dd').getInfo()
                cloud_pct = image.get('CLOUDY_PIXEL_PERCENTAGE').getInfo()
                print(f"Exporting image {i+1}/{num_images}: {date_str} (Clouds: {cloud_pct}%)")
                

                

                task = ee.batch.Export.image.toDrive(
                    image=image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9','B10', 'B11', 'B12']),
                    description=f'Sentinel2_{date_str}',
                    folder="MyProject",
                    fileNamePrefix=f'{Task_Name}:{date_str}_{lon}_{lat}',
                    region=small_region,
                    scale=10,
                    fileFormat='GeoTIFF',
                    maxPixels=1e9
                )
                
                task.start()
               # print(f"  Export started with ID: {task.id}")
            
           # print(f"All {num_images} export tasks have been started!")
           # print("Check progress at: https://code.earthengine.google.com/tasks")
            
        else:
            print("No images found in the collection!")
        return   num_images
