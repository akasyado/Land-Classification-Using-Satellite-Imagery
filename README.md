# Land-Classification-Using-Satellite-Imagery

This project uses CNN to classify land covers using images download from sentinel2 satellite.
The earthengine.py downloads the images for a given date range and and co-ordinates.
Google Earth Engine is used to get satellite data



## Tech Stack
| Category                             | Tools / Frameworks               |
| ------------------------------------ | -------------------------------- |
| **Language**                         | Python                           |
| **Machine Learning / Deep Learning** | TensorFlow                       |
| **API Framework**                    | FastAPI                          |
| **Web Interface**                    | Streamlit / Flask                |
| **Geospatial Processing**            | Earth Engine API, Rasterio       |
| **Visualization**                    | Matplotlib                       |
| **Cloud & Deployment**               | AWS, Google Cloud                |
| **Utilities**                        | NumPy, Python-Multipart, Uvicorn |



## How to Run
# Install dependencies
pip install -r requirements.txt

# Authenticate Google Earth Engine
import ee                                                                   
ee.Authenticate()                                                           
In earthengine.py                                                           
replace                                                                      
ee.Initialize()                                                              
with                                                                         
ee.Initialize(project="your-project-name")                                   
Change "your-project-name" with your actual google cloud or earth engine project Id



Replace "your-project-name" with your actual Google Cloud or Earth Engine project ID
Create Folder named "MyProject" in google drive
Any images downloaded are stored in this folder

# Set up Google Drive integration using Rclone
The project uses Rclone to retrieve the images from Google Drive.
Create a local mount folder: ./gdrive

# Run the project
python start.py

