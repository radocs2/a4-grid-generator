import os
import streamlit as st
from PIL import Image


def clean_dir(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):  # Check if it's a file, not a subdirectory
            try:
                os.remove(file_path)
                print(f"Removed: {filename}")
            except Exception as e:
                pass


def reset_page():
    clean_dir('temp')
    st.session_state["uploader_key"] += 1
    st.cache_data.clear()


def generate_a4_grid(image_paths, num_rows=4, num_cols=3):
    # A4 dimensions in pixels (assuming 300 DPI)
    # 1 inch = 25.4 mm
    # A4 width: 210 mm / 25.4 mm/inch * 300 dpi = 2480 pixels
    # A4 height: 297 mm / 25.4 mm/inch * 300 dpi = 3508 pixels
    a4_width_px = 2480
    a4_height_px = 3508

    # Create a new blank A4 image
    a4_image = Image.new('RGB', (a4_width_px, a4_height_px), color='white')

    # Calculate cell size
    cell_width = a4_width_px // num_cols
    cell_height = a4_height_px // num_rows

    images = [Image.open(path) for path in image_paths]

    for i, img in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        aspect_ratio = img.height / img.width

        # Resize image to fit cell (optional, but recommended)
        new_height = int(cell_width * aspect_ratio * 0.85)
        new_width = int(cell_width * 0.85)
        img = img.resize((new_width, new_height))

        # Calculate paste position
        x_offset = (col * cell_width) + 75
        y_offset = (row * cell_height) + 75

        a4_image.paste(img, (x_offset, y_offset))

    a4_image.save(f'temp/a4_image_grid.png')
