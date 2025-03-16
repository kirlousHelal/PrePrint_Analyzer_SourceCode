import numpy as np
import pickle
from tensorflow.keras.preprocessing import image  # Use tensorflow.keras
import cv2
from tensorflow.keras.models import load_model  # Use tensorflow.keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # Use tensorflow.keras
import os
import detect_resolution
import detect_contrast_RandomForset

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

# For Testing
def testDynamicModels(img_path, model_path):
    # Load the model
    full_model_path = get_model_path(model_path)
    classifier = load_model(full_model_path)

    # Get model's expected input shape
    expected_shape = classifier.input_shape
    print(f"🔍 Expected Model Input Shape: {expected_shape}")

    # Determine target image size
    img_size = (expected_shape[1], expected_shape[2]) if len(expected_shape) >= 3 else (64, 64)

    # Load and preprocess the image
    test_image = image.load_img(img_path, target_size=img_size)
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    # If the model expects a flattened input, reshape it
    if expected_shape[-1] is None or expected_shape[-1] > 3:  # If expecting a 1D vector
        test_image = test_image.reshape(1, -1)  # Flatten the image

    # Make the prediction
    result = classifier.predict(test_image)

    if result[0][0] == 1:
        if model_path == "Mitalic_model.h5":
            prediction = 'Not Metalic'
        if model_path ==  "model_Blue&4colors.h5":
            prediction = 'Blue'
        if model_path ==  "model_orange_4colors.h5":
            prediction = 'Orange'
        if model_path ==  "model_solid& gradiant Vs 4colors.h5":
            prediction = 'Solid and Grandiant'
        if model_path ==  "model_gradiant_solid.h5":
            prediction = 'Solid'
    else:
        if model_path == "Mitalic_model.h5":
            prediction = 'Metalic'
        if model_path ==  "model_Blue&4colors.h5":
            prediction = 'Not Blue'
        if model_path ==  "model_orange_4colors.h5":
            prediction = 'Not Orange'
        if model_path ==  "model_solid& gradiant Vs 4colors.h5":
            prediction = 'Not Solid and Grandiant'
        if model_path ==  "model_gradiant_solid.h5":
            prediction = 'Gradiant'

    print(prediction)

    # # Display the image
    # img = cv2.imread(img_path)
    # cv2.imshow('window name', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return prediction

def excuteDynamicModels(img_path):
    model_paths=["Mitalic_model.h5","model_Blue&4colors.h5","model_orange_4colors.h5","model_solid& gradiant Vs 4colors.h5",
                 "model_gradiant_solid.h5"]

    results=[]
    skipSolidGradiant =False
    for i in range(len(model_paths)):
        print(f"in model number {i+1}")

        if(skipSolidGradiant): 
            skipSolidGradiant = False
            continue

        result=testDynamicModels(img_path=img_path,model_path= model_paths[i])
        if(result =="Not Solid and Grandiant"):
            results.append("Not Solid")
            results.append("Not Gradiant")
            skipSolidGradiant=True
        elif (result == "Solid and Grandiant"): continue  
        elif(result == "Solid"): 
            results.append("Solid")
            results.append("Not Gradiant")
        elif(result == "Gradiant"): 
            results.append("Not Solid")
            results.append("Gradiant")
        else: results.append(result)


    # If none of the classifications match, it's a "4 Color Image"
    if all("Not" in result for result in results):
        results.append("Then This Image Is 4 Color Image")

    results.append(detect_contrast_RandomForset.predict_contrast(image_path=img_path))
    res,dim = detect_resolution.get_image_info(image_path=img_path)
    results.append(res)
    results.append(dim)
    return results
