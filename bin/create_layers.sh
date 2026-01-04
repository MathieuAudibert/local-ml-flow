#!/bin/bash

mkdir -p terraform/python/
pip install pandas scikit-learn joblib -t terraform/python/

echo "clean up..."
find terraform/python/ -type d -name "tests" -exec rm -rf {} +
find terraform/python/ -type d -name "__pycache__" -exec rm -rf {} +
find terraform/python/ -name "*.pyc" -delete
rm -rf terraform/python/*.dist-info
rm -rf terraform/python/*.egg-info

# you might wanna change this
echo "compressing Layer..."
powershell.exe -Command "Compress-Archive -Path terraform/python -DestinationPath terraform/ml_layer.zip -Force"

echo "compressing Code..."
powershell.exe -Command "Compress-Archive -Path src -DestinationPath terraform/ingestion.zip -Force"

rm -rf terraform/python/