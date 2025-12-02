#!/bin/bash

# Setup script for coral-sampling-tool

# Create conda environment with Python 3.7
echo "Creating conda environment 'coral-sampling'..."
conda create -n coral-sampling python=3.7 -y

# Activate conda environment
echo "Activating conda environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate coral-sampling

# Install dependencies
echo "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

echo ""
echo "Setup complete! To run the app:"
echo "1. Activate the environment: conda activate coral-sampling"
echo "2. Run the app: python app.py"
