## Testing
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import joblib
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

# Feature Extraction
def extract_features(images):
    features = []
    for img in images:
        # Ensure the image is in uint8 format for cv2.calcHist
        if img.dtype != np.uint8:
            img_uint8 = (img * 255).astype(np.uint8)  # Convert back to uint8
        else:
            img_uint8 = img
        
        # Histogram statistics
        hist = cv2.calcHist([img_uint8], [0], None, [256], [0, 256]).flatten()
        mean, std_dev = np.mean(img), np.std(img)
        features.append(np.concatenate([hist, [mean, std_dev]]))
    return np.array(features)

# Predict on New Images
def predict_contrast(image_path, model=None):
    model_path=get_model_path('random_forest_model.joblib')
    model = joblib.load(model_path)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = cv2.resize(img, (128, 128))
        img = img / 255.0
        features = extract_features([img])
        prediction = model.predict(features)
        return "Good Contrast" if prediction[0] == 1 else "Low Contrast"
    else:
        return "Invalid Image"
    

 # Load the trained model
# loaded_model = joblib.load('random_forest_model.joblib')

#### Example usage
# image_path = test_images()
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0003.jpg"
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0004.jpg"
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0005.jpg"
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0006.jpg"
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0007.jpg"
# image_path = r"C:\Users\kirlo\OneDrive\Desktop\test_images\IMG-20250121-WA0008.jpg"


# result = predict_contrast(image_path, loaded_model)
# print("Prediction:", result)

#  # Display the image and results
# input_image = cv2.imread(image_path)

# # Convert the image to RGB for displaying with Matplotlib
# input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
# plt.figure(figsize=(8, 8))
# plt.imshow(input_image_rgb)
# plt.axis('off')
# plt.title(result)
# plt.show()
