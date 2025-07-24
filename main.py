import time
import os
import streamlit as st
from utils import generate_a4_grid, reset_page

image_paths = []
directory_path = "temp"
os.makedirs(directory_path, exist_ok=True)

st.cache_data.clear()

st.header('Gerador de múltiplas imagens em folha A4')

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

uploaded_files = st.file_uploader(
    label='Suba sua imagem aqui!',
    type=['jpg', 'png', 'svg'],
    accept_multiple_files=True,
    key=st.session_state["uploader_key"]
)


if uploaded_files:
    num_rows = st.number_input(label='Número de linhas por arquivo',
                               min_value=1, max_value=8, value=4)

    num_cols = st.number_input(label='Número de colunas por arquivo',
                               min_value=1, max_value=8, value=3)

    max_copies = int((num_rows * num_cols) / len(uploaded_files))
    num_copies = st.number_input(label='Número de cópias por arquivo',
                                 min_value=1, max_value=max_copies, value=1)

    generate_button = st.button(label='Gerar')

    if generate_button:
        for file in uploaded_files:
            with open(f"temp/{file.name}", "wb") as f:
                f.write(file.getbuffer())
            image_paths += [f"temp/{file.name}"] * num_copies

        generate_a4_grid(image_paths, num_rows, num_cols)
        time.sleep(5)

if os.path.exists('temp/a4_image_grid.png'):
    with open("temp/a4_image_grid.png", "rb") as file:
        st.download_button(
            label="Download image",
            data=file,
            file_name="a4_image_grid.png",
            mime="image/png",
            on_click=reset_page
        )
