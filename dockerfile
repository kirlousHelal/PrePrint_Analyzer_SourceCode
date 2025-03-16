# Use TensorFlow image as base
FROM tensorflow/tensorflow:latest

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV, Tkinter, and GUI support
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-tk \
    x11-apps \
    xvfb

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set DISPLAY environment variable for GUI apps (will be overridden in docker-compose)
ENV DISPLAY=host.docker.internal:0

# Run the app with X virtual framebuffer (for GUI support)
CMD ["xvfb-run", "python", "GUI.py"]
