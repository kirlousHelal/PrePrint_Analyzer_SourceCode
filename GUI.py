import TestingModels  # Uncomment this when you have TestingModels module ready
import tkinter as tk
from tkinter import filedialog, Label, Button, Entry,ttk
from PIL import Image, ImageTk
import enhance_contrast
import edit_dpi
import reduce_cmyk
import os
import enhance_resolution_EDSR_X3

# Create directories if they don't exist
if not os.path.exists("enhanced_contrast"):
    os.makedirs("enhanced_contrast")
if not os.path.exists("reduced_cmyk"):
    os.makedirs("reduced_cmyk")
if not os.path.exists("changed_dpi"):
    os.makedirs("changed_dpi")

size_one = ("360x700")
size_two = ("520x700")

# Main window to display image and results
def upload_image():
    global img_path
    img_path = filedialog.askopenfilename()
    if img_path:
        # Display the uploaded image
        img = Image.open(img_path)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # Image display panel
        panel = Label(window, image=img)
        panel.image = img  # Keep a reference to avoid garbage collection
        panel.grid(row=2, column=0, columnspan=2)

        # Classify the image
        results = TestingModels.excuteDynamicModels(img_path)  # Uncomment when real classification function is ready

        # Convert results to string for display
        result_text = "\n".join(results)

        # Update the result label with the classification and the additional condition
        result_label.config(text=f"Classification Results:\n{result_text}")

# Enhance Contrast Window
def open_contrast_window():
    contrast_window = tk.Toplevel(window)
    contrast_window.title("Enhance Contrast")
    contrast_window.geometry(size_two)

    # Original Image display
    original_img = Image.open(img_path)
    original_img = original_img.resize((250, 250), Image.ANTIALIAS)
    original_img_tk = ImageTk.PhotoImage(original_img)
    original_panel = Label(contrast_window, image=original_img_tk)
    original_panel.image = original_img_tk
    original_panel.grid(row=0, column=0)

    # Input field for contrast factor
    contrast_label = Label(contrast_window, text="Enter Contrast Factor (e.g., 2.0)")
    contrast_label.grid(row=1, column=0)
    contrast_input = Entry(contrast_window)
    contrast_input.grid(row=2, column=0)
    
    # Function to update the image dynamically
    def update_contrast():
        contrast_factor = float(contrast_input.get()) if contrast_input.get() else 1.0
        enhanced_img = enhance_contrast.enhance_contrast(img_path, contrast_factor)
        enhanced_img = enhanced_img.resize((250, 250), Image.ANTIALIAS)
        enhanced_img_tk = ImageTk.PhotoImage(enhanced_img)
        enhanced_panel.config(image=enhanced_img_tk)
        enhanced_panel.image = enhanced_img_tk
    
    # Button to update the image
    update_button = Button(contrast_window, text="Update Image", command=update_contrast)
    update_button.grid(row=3, column=0)

    # Enhanced Image display
    enhanced_label = Label(contrast_window, text="Enhanced Image")
    enhanced_label.grid(row=0, column=1)
    enhanced_img = original_img
    enhanced_img_tk = ImageTk.PhotoImage(enhanced_img)
    enhanced_panel = Label(contrast_window, image=enhanced_img_tk)
    enhanced_panel.image = enhanced_img_tk
    enhanced_panel.grid(row=1, column=1)

    # Save button
    def save_enhanced_image():
        contrast_factor = float(contrast_input.get()) if contrast_input.get() else 1.0
        enhanced_img = enhance_contrast.enhance_contrast(img_path, contrast_factor)
        
        # Save to 'enhanced_contrast' folder
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg"),("PNG Files", "*.png")], initialdir="enhanced_contrast")
        if save_path:
            enhanced_img.save(save_path)  # Save the image with the applied enhancement

    save_button = Button(contrast_window, text="Save Enhanced Image", command=lambda: save_enhanced_image())
    save_button.grid(row=4, column=0)

# Enhance Red Window
def open_reduce_cmyk_window():
    red_window = tk.Toplevel(window)
    red_window.title("Reduce CMYK")
    red_window.geometry(size_two)

    # Original Image display
    original_img = Image.open(img_path)
    original_img = original_img.resize((250, 250), Image.ANTIALIAS)
    original_img_tk = ImageTk.PhotoImage(original_img)
    original_panel = Label(red_window, image=original_img_tk)
    original_panel.image = original_img_tk
    original_panel.grid(row=0, column=0, columnspan=2)

    # Dropdown for CMYK channel selection
    channel_label = Label(red_window, text="Select CMYK Channel:")
    channel_label.grid(row=1, column=0, padx=5, pady=5)
    
    channel_options = ["Cyan", "Magenta", "Yellow", "Black"]
    selected_channel = tk.StringVar(value="Magenta")  # Default to Magenta

    channel_dropdown = ttk.Combobox(red_window, textvariable=selected_channel, values=channel_options, state="readonly")
    channel_dropdown.grid(row=1, column=1, padx=5, pady=5)

    # Input field for reduction factor
    reduction_label = Label(red_window, text="Enter Reduction Factor (e.g., 0.5)")
    reduction_label.grid(row=2, column=0, columnspan=2)
    
    reduction_input = Entry(red_window)
    reduction_input.grid(row=3, column=0, columnspan=2)

    # Function to update the image dynamically
    def update_red():
        reduction_factor = float(reduction_input.get()) if reduction_input.get() else 1.0
        channel_type = selected_channel.get().lower()  # Get selected channel

        reduced_img = reduce_cmyk.reduce_cmyk(image_path=img_path, channel_type=channel_type, reduction_factor=reduction_factor)
        reduced_img = reduced_img.resize((250, 250), Image.ANTIALIAS)
        reduced_img_tk = ImageTk.PhotoImage(reduced_img)
        reduced_panel.config(image=reduced_img_tk)
        reduced_panel.image = reduced_img_tk

    # Button to update the image
    update_button = Button(red_window, text="Update Image", command=update_red)
    update_button.grid(row=4, column=0, columnspan=2, pady=5)

    # Reduced Image display
    reduced_label = Label(red_window, text="Reduced Image")
    reduced_label.grid(row=5, column=0, columnspan=2)

    reduced_img = original_img
    reduced_img_tk = ImageTk.PhotoImage(reduced_img)
    reduced_panel = Label(red_window, image=reduced_img_tk)
    reduced_panel.image = reduced_img_tk
    reduced_panel.grid(row=6, column=0, columnspan=2)

    # Save button
    def save_reduced_image():
        reduction_factor = float(reduction_input.get()) if reduction_input.get() else 1.0
        channel_type = selected_channel.get().lower()

        reduced_img = reduce_cmyk.reduce_cmyk(img_path, channel_type, reduction_factor)

        # Save to 'reduced_cmyk' folder
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg"),("PNG Files", "*.png")], initialdir="reduced_cmyk")
        if save_path:
            reduced_img.save(save_path)  # Save the image with the applied enhancement

    save_button = Button(red_window, text="Save Reduced Image", command=save_reduced_image)
    save_button.grid(row=7, column=0, columnspan=2, pady=5)


# DPI Window

def open_dpi_window():
    dpi_window = tk.Toplevel(window)
    dpi_window.title("Enhance Resolution")
    dpi_window.geometry(size_one)

    # Original Image display
    original_img = Image.open(img_path)
    original_width, original_height = original_img.size
    original_img = original_img.resize((250, 250), Image.ANTIALIAS)
    original_img_tk = ImageTk.PhotoImage(original_img)
    original_panel = Label(dpi_window, image=original_img_tk)
    original_panel.image = original_img_tk
    original_panel.grid(row=0, column=0)

    dpi = original_img.info.get('dpi', (72, 72))
    dpi_x, dpi_y = float(dpi[0]), float(dpi[1])  # Convert DPI to float

    # Original DPI label
    dpi_label = Label(dpi_window, text=f"Original DPI: {round(dpi_x, 2)}")
    dpi_label.grid(row=1, column=0)

    # Original Dimensions label
    original_dim_label = Label(dpi_window, text=f"Original Dimensions: {original_width} x {original_height}")
    original_dim_label.grid(row=2, column=0)

    dpi_input = Entry(dpi_window)
    dpi_input.grid(row=3, column=0)

    # Function to update the DPI value dynamically
    def update_dpi():
        global upadatedImage  # Make sure to modify the global variable
        global newDpi  # Make sure to modify the global variable
        global exifData  # Make sure to modify the global variable

        dpi_factor = int(dpi_input.get()) if dpi_input.get() else 3
        img_with_dpi, new_dpi, exif_data = enhance_resolution_EDSR_X3.enhance_resolution(
            image_path=img_path, factor=dpi_factor, original_dpi=round(dpi_x, 2)
        )

        # Update current DPI and dimensions
        current_width, current_height = img_with_dpi.size
        dpi_label_result.config(text=f"Current DPI: {new_dpi}")
        current_dim_label.config(text=f"Current Dimensions: {current_width} x {current_height}")

        upadatedImage = img_with_dpi
        newDpi = new_dpi
        exifData = exif_data

        img_with_dpi = img_with_dpi.resize((250, 250), Image.LANCZOS)
        img_with_dpi_tk = ImageTk.PhotoImage(img_with_dpi)
        img_with_dpi_panel.config(image=img_with_dpi_tk)
        img_with_dpi_panel.image = img_with_dpi_tk

    # Button to update the DPI
    update_button = Button(dpi_window, text="Update Resolution", command=update_dpi)
    update_button.grid(row=4, column=0)

    # Current DPI label
    dpi_label_result = Label(dpi_window, text=f"Current DPI: {round(dpi_x, 2)}")
    dpi_label_result.grid(row=5, column=0)

    # Current Dimensions label
    current_dim_label = Label(dpi_window, text=f"Current Dimensions: {original_width} x {original_height}")
    current_dim_label.grid(row=6, column=0)

    # DPI Image display
    img_with_dpi = original_img
    img_with_dpi_tk = ImageTk.PhotoImage(img_with_dpi)
    img_with_dpi_panel = Label(dpi_window, image=img_with_dpi_tk)
    img_with_dpi_panel.image = img_with_dpi_tk
    img_with_dpi_panel.grid(row=7, column=0)

    # Save button
    def save_with_dpi():
        img_with_dpi = upadatedImage
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG Files", "*.jpg"), ("PNG Files", "*.png")],
            initialdir="changed_dpi",
        )
        if save_path:
            img_with_dpi.save(save_path, dpi=(newDpi, newDpi), exif=exifData)

    save_button = Button(dpi_window, text="Save Image with DPI", command=save_with_dpi)
    save_button.grid(row=8, column=0)


# Setting up the Tkinter window
window = tk.Tk()
window.title("Image Classifier")
window.geometry(size_one)

# Title Label
title = Label(window, text="Image Classification", font=("Arial", 18))
title.grid(row=0, column=0, columnspan=2)

# Upload Button
upload_button = Button(window, text="Upload Image", command=upload_image, font=("Arial", 12))
upload_button.grid(row=1, column=0, columnspan=2, pady=20)

# Classification result display label
result_label = Label(window, text="", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2, pady=20)

# Buttons for each enhancement
contrast_button = Button(window, text="Enhance Contrast", command=open_contrast_window)
contrast_button.grid(row=4, column=0, pady=10)

dpi_button = Button(window, text="Enhance Resolution", command=open_dpi_window)
dpi_button.grid(row=5, column=0, pady=10)

red_button = Button(window, text="Reduce CMYK", command=open_reduce_cmyk_window)
red_button.grid(row=6, column=0, pady=10)

# Start the GUI event loop
window.mainloop()
