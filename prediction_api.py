from fastapi import FastAPI, UploadFile, File
from typing import List
import tensorflow as tf
from PIL import Image
import numpy as np
import rasterio
import tempfile



app = FastAPI()

# Load your trained model
model = tf.keras.models.load_model("best_model.keras")

@app.post("/predict")
async def predict(files: List[UploadFile] = File(...)):
    results = {}
    counter=0
    
    for file in files:
        counter+=1
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        
        def calculations(filepath):
            with rasterio.open(filepath) as src:
                array=src.read()
            C,H,W=array.shape
            if H!=W:
               min_dim=min(H,W)
               array=array[:,:min_dim,:min_dim]

            t=array.shape[1]%64
            if t!=0:
               array=array[:,:-t,:-t]

            patches = []
            
            for i in range(0, array.shape[1], 64):
                for j in range(0, array.shape[2], 64):
                    patch = array[:, i:i+64, j:j+64]
                    patches.append(patch)

            patches = np.stack(patches)     
            patches = np.transpose(patches, (0, 2, 3, 1)).astype(np.float32)  
            return patches

        
        arr_list = calculations(tmp_path)
        pred = model.predict(arr_list)
        classes = np.argmax(pred, axis=1)
        results[f"image_{counter}"]=classes.tolist()

    return results

