import pandas as pd
import base64
from PIL import Image
from io import BytesIO
import os

def load_csv(file):
    return pd.read_csv(file)

def decode_and_save_image(base64_str, folder, filename):
    try:
        img_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(img_data))
        output_path = os.path.join(folder, filename)
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error guardando {filename}: {e}")
        return False
