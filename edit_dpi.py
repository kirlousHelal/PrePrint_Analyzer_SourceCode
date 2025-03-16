from PIL import Image
import piexif
from io import BytesIO

def save_with_dpi(image_path, dpi_value=300):
    # Open image
    img = Image.open(image_path)

    # Create EXIF metadata with DPI
    exif_dict = {"0th": {
        piexif.ImageIFD.XResolution: (dpi_value, 1),  # 300 DPI
        piexif.ImageIFD.YResolution: (dpi_value, 1),  # 300 DPI
        piexif.ImageIFD.ResolutionUnit: 2  # 2 = Inches, 3 = Centimeters
    }}
    
    # Convert EXIF data to bytes
    exif_bytes = piexif.dump(exif_dict)

    # Create a BytesIO object to save the image in memory
    img_byte_arr = BytesIO()

    # Save image to the BytesIO object with new DPI and EXIF
    img.save(img_byte_arr, format="PNG", dpi=(dpi_value, dpi_value), exif=exif_bytes)
    
    # Return the in-memory image as a PIL Image object
    img_byte_arr.seek(0)
    updated_img = Image.open(img_byte_arr)
    
    print(f"✅ Resolution updated to {dpi_value} in memory.")
    return updated_img,exif_bytes
