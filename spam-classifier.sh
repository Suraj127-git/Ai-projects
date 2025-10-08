#!/bin/bash

# Create root directory
mkdir -p spam-classifier
cd spam-classifier

# Create subdirectories
mkdir -p data notebooks app model

# Create placeholder files
touch data/emails.csv
touch notebooks/train_model.ipynb
touch app/main.py
touch app/model.py
touch app/schemas.py
touch model/spam_model.pkl
touch requirements.txt
touch Dockerfile
touch README.md

# Add a simple README header
echo "# Spam Email Classifier 🚀
A Naive Bayes-based spam detection API built with FastAPI." > README.md

# Print done message
echo "✅ Project structure created successfully!"
tree .
