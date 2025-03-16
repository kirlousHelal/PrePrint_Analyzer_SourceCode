from PIL import Image

def reduce_cmyk(image_path, channel_type, reduction_factor=0.5):
    # Open the image
    img = Image.open(image_path)

    # Convert the image to CMYK mode
    cmyk_image = img.convert('CMYK')

    # Split the CMYK image into individual channels
    c, m, y, k = cmyk_image.split()

    # Create a dictionary to map types to their respective channels
    channels = {'cyan': c, 'magenta': m, 'yellow': y, 'black': k}

    # Ensure the given type is valid
    if channel_type.lower() not in channels:
        raise ValueError("Invalid channel type. Choose from 'cyan', 'magenta', 'yellow', or 'black'.")

    # Reduce the intensity of the selected channel
    channels[channel_type.lower()] = channels[channel_type.lower()].point(lambda i: int(i * reduction_factor))

    # Merge the modified channels back into a CMYK image
    modified_cmyk = Image.merge('CMYK', (channels['cyan'], channels['magenta'], channels['yellow'], channels['black']))

    # Convert back to RGB for display
    rgb_image = modified_cmyk.convert('RGB')

    return rgb_image
