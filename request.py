import requests
import glob
import os



def list_(tif_files):
    print(f"Found {len(tif_files)} images")
    files = [] 
    for file_path in tif_files: 
        files.append( ('files', (os.path.basename(file_path), open(file_path, 'rb'), 'image/tiff')) )


    response = requests.post("http://localhost:8000/predict", files=files)
    return response



