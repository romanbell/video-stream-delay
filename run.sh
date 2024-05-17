#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python could not be found, please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found, please install pip."
    exit 1
fi

echo "Installing required Python packages..."
pip3 install opencv-python screeninfo

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install Python packages."
    exit 1
fi

echo "Starting the video stream script..."
# Assume the Python script is named delayed_video_stream.py and located in the same directory as this shell script
python3 delayed_video_stream.py