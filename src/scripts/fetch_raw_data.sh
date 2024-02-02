#!/usr/bin/env bash

#!/bin/bash

# Replace 'your_kaggle_username' and 'your_kaggle_api_key' with your actual Kaggle credentials

# Check if the variables are set
if [ -z "$KAGGLE_USERNAME" ] || [ -z "$KAGGLE_KEY" ]; then
    echo "Error: Kaggle credentials are not set. Please edit this script and set your Kaggle username and API key."
    exit 1
fi

# Download the dataset
kaggle datasets download -d fangfangz/audio-based-violence-detection-dataset -p data/raw

# Add any other commands related to your project or dataset here

echo "Download completed successfully."
