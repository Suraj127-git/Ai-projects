#!/bin/bash

# Project root
mkdir -p house-price-api
cd house-price-api || exit

# Create folders
mkdir -p data notebooks app model

# Create empty files
touch data/housing.csv
touch notebooks/model_training.ipynb
touch app/main.py app/model.py app/schemas.py
touch model/house_price_model.pkl
touch requirements.txt
touch Dockerfile
touch README.md

echo "✅ Project structure created successfully!"
