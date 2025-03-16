import cv2
import numpy as np
from cv2 import dnn_superres
from tqdm import tqdm
import time
import threading
from PIL import Image
import os
import sys
from pathlib import Path

def get_model_path(model_name):
    if getattr(sys, 'frozen', False):
        # Running as .exe — use the temp folder path
        base_path = sys._MEIPASS
    else:
        # Running as a regular script
        base_path = Path(__file__).parent

    return os.path.join(base_path, model_name)

def update_progress_bar(pbar, start_time):
    """Updates progress dynamically while processing."""
    while not pbar.n >= 100:
        elapsed_time = time.time() - start_time
        estimated_total_time = max(elapsed_time * 1.2, elapsed_time + 1)
        progress = min(int((elapsed_time / estimated_total_time) * 100), 100)
        pbar.n = progress
        pbar.refresh()
        time.sleep(0.2)

def unsharp_mask(image, strength=1.5, blur_size=(5, 5)):
    """Applies Unsharp Masking to sharpen the image."""
    blurred = cv2.GaussianBlur(image, blur_size, 0)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def enhance_resolution(image_path, factor, original_dpi):
    """Enhances image resolution using EDSR and updates DPI accordingly."""
    sr = dnn_superres.DnnSuperResImpl_create()

    # ✅ Extract EXIF before processing
    pil_image = Image.open(image_path)
    exif_data = pil_image.info.get("exif")

     # Check EXIF data
    if exif_data is None or not isinstance(exif_data, bytes):
        exif_data = b''  # Use empty bytes if no EXIF data

    # Read image
    image = cv2.imread(image_path)

    # Load model
    # path = "EDSR_x3.pb"
    path = get_model_path("EDSR_x3.pb")
    sr.readModel(path)
    sr.setModel("edsr", factor)

    # Start progress bar
    with tqdm(total=100, desc="Enhancing Resolution", bar_format="{l_bar}{bar} {n_fmt}% | {elapsed}s") as pbar:
        start_time = time.time()

        # Start the background thread for the progress bar
        progress_thread = threading.Thread(target=update_progress_bar, args=(pbar, start_time))
        progress_thread.start()

        # Run model processing
        result = sr.upsample(image)

        # Measure actual time
        actual_time = time.time() - start_time
        pbar.n = 100
        pbar.refresh()
        progress_thread.join()

    # Apply sharpening filter
    # sharpened_result = unsharp_mask(image=result, strength=1.5,blur_size=(5,5))
    sharpened_result = unsharp_mask(image=result, strength=2.5,blur_size=(7,7))

    # Calculate new DPI
    # new_dpi = original_dpi * factor
    new_dpi = original_dpi 
    print(f"\n✅ Enhancement completed in {actual_time:.2f} seconds! New DPI: {new_dpi}")

    # Convert to PIL Image
    enhanced_image = Image.fromarray(cv2.cvtColor(sharpened_result, cv2.COLOR_BGR2RGB))

    return enhanced_image, new_dpi, exif_data

# Example Usage:
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\images2.jpg"
# enhanced_img, new_dpi = enhance_resolution(image_path, factor=3, original_dpi=72)
# save_with_dpi(enhanced_img, "output.jpg", new_dpi)
