from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt

def enhance_contrast(image_path, contrast_factor=2.0):
    # Open the image
    image = Image.open(image_path)
    
    # Create a contrast enhancer object
    enhancer = ImageEnhance.Contrast(image)
    
    # Enhance the contrast
    enhanced_image = enhancer.enhance(contrast_factor)
    
    # # Display the original and enhanced images side by side
    # fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    # # Display original image
    # axes[0].imshow(image)
    # axes[0].axis('off')
    # axes[0].set_title("Original Image")
    
    # # Display enhanced image
    # axes[1].imshow(enhanced_image)
    # axes[1].axis('off')
    # axes[1].set_title(f"Enhanced Contrast (Factor: {contrast_factor})")
    
    # plt.show()
    return enhanced_image

