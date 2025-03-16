import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import isclose
from blur_detection.detection import (check_contrast, estimate_blur,
                                      fix_image_size)


def check_contrast_blur(image_path) :   
    input_image = cv2.imread(image_path)

    # Check if the image was successfully loaded
    if input_image is None:
        print(f"Error: Unable to load image from path: {image_path}")
    else:
        # Fix the image size (if necessary)
        input_image = fix_image_size(input_image)
        # # Calculate blur
        blur_map, score, is_blurry = estimate_blur(input_image, threshold=5.0)
        # # Calculate contrast
        contrast_ratio, is_low_contrast = check_contrast(input_image)
        # assert isclose(score, 0.8788307786605958, abs_tol=10**-3)
        # assert isclose(contrast_ratio, 0.27411588235294115, abs_tol=10**-3)

        # Convert the image to RGB for displaying with Matplotlib
        input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        # Display the image and results
        

        # Print the results
        print(f"Contrast Ratio: {contrast_ratio:.2f}")
        if is_low_contrast:
            s = "Low Contrast"
        else:
            s = "Good Contrast"

        return s
        # print(s)
        # print(f"Blur Ratio: {score:.2f}")
        # if is_blurry:
        #     print(f"BLur")
        # else:
        #     print(f"Non BLur")


        # plt.figure(figsize=(8, 8))
        # plt.imshow(input_image_rgb)
        # plt.axis('off')
        # plt.title(s)
        # plt.show()