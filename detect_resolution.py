from PIL import Image
import matplotlib.pyplot as plt

def get_image_info(image_path, default_dpi=72):
    # Open the image
    image = Image.open(image_path)
    
    # Get pixel dimensions
    width_px, height_px = image.size
    
    # Get DPI from metadata (default to 72 if not available)
    dpi = image.info.get('dpi', (default_dpi, default_dpi))
    dpi_x, dpi_y = float(dpi[0]), float(dpi[1])  # Convert DPI to float
    
    # Calculate physical size in inches
    physical_width_inch = width_px / dpi_x
    physical_height_inch = height_px / dpi_y
    
    # Check for EXIF data (metadata)
    exif_data = image._getexif()
    if exif_data:
        metadata_status = "Metadata (EXIF) found"
    else:
        metadata_status = "No metadata (EXIF) available"
    
    # Display results
    print(f"Image Path: {image_path}")
    print(f"Image Dimensions (pixels): {width_px} x {height_px}")
    print(f"DPI (Pixels per Inch): {dpi_x:.2f} x {dpi_y:.2f}")
    print(f"Physical Size (inches): {physical_width_inch:.2f} x {physical_height_inch:.2f}")
    print(f"Pixels per Inch (PPI): Horizontal = {dpi_x:.2f}, Vertical = {dpi_y:.2f}")
    print(metadata_status)
    
    # # Display the image with physical size using matplotlib
    # fig = plt.figure(figsize=(physical_width_inch, physical_height_inch))  # Set the figure size based on physical dimensions
    # plt.imshow(image)
    # plt.axis('off')  # Hide the axis
    # plt.title(f"Displayed at {dpi_x:.2f} DPI")  # Add title with DPI info
    # plt.show()  # Display the image
    
    res = round(dpi_x, 2)
    if (res < 300) : result = f"{res} (Warnning the Resolution is less than 300!!!)"
    else : result = f"{res}"

    dimensions = f"{width_px} x {height_px}"
    return result,dimensions
