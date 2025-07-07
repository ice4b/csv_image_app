import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from PIL import Image
import os
import shutil
from zipfile import ZipFile
from utils2 import load_csv, decode_and_save_image


st.title("Visor y Descarga de Imágenes (Base64) desde CSV")

# Subida del archivo CSV
csv_file = st.file_uploader("Sube un archivo CSV con imágenes codificadas en base64", type=["csv"])

if csv_file:
    df = load_csv(csv_file)
    st.write("Vista previa del CSV:")
    st.dataframe(df)

    # Supón que hay una columna llamada 'image' con rutas relativas o absolutas
    image_column = st.selectbox("Selecciona la columna con imágenes codificadas en base64", df.columns)

    name_column = st.selectbox("Selecciona la columna del nombre", df.columns)

    price_column = st.selectbox("Selecciona la columna del precio", df.columns)

    if image_column:
        st.subheader("Vista de previa de imágenes")

        # Mostrar imágenes en una cuadrícula
        cols = st.columns(3)
        for idx, row in df.iterrows():
            with cols[idx % 3]:
                try:
                    img_data = base64.b64decode(row[image_column])
                    img = Image.open(BytesIO(img_data))
                    # st.image(img, caption=f"Imagen {idx}", use_container_width=True)    # The use_column_width parameter has been deprecated and will be removed in a future release. Please utilize the use_container_width parameter instead.
                    st.image(img, caption=f"{idx} {row[name_column]} ${row[price_column]}", use_container_width=True)    # The use_column_width parameter has been deprecated and will be removed in a future release. Please utilize the use_container_width parameter instead.
                except Exception as e:
                    st.warning(f"Error al mostrar imagen {idx}: {e}")
        
        # Botón para exportar imágenes
        if st.button("Exportar todas las imágenes a ZIP"):
            temp_folder = "temp_images"
            zip_filename = "imagenes_exportadas.zip"
            os.makedirs(temp_folder, exist_ok=True)

            # Guardar imágenes
            filenames = []
            for idx, b64_str in enumerate(df[image_column]):
                filename = f"{idx} {df[name_column][idx]}.png"
                path = os.path.join(temp_folder, filename)
                if decode_and_save_image(b64_str, temp_folder, filename):
                    filenames.append(path)
            
            # Comprimir en ZIP
            with ZipFile(zip_filename, "w") as zipf:
                for file in filenames:
                    zipf.write(file, arcname=os.path.basename(file))

            # Leer el ZIP para descarga
            with open(zip_filename, "rb") as f:
                zip_bytes = f.read()
                st.download_button(
                    label="📦 Descargar imágenes como ZIP",
                    data=zip_bytes,
                    file_name=zip_filename,
                    mime="application/zip"
                )

            # Limpiar archivos temporales
            shutil.rmtree(temp_folder)
            os.remove(zip_filename)

