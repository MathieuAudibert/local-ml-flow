#!/bin/bash

rm -rf build_layer
mkdir -p build_layer/python/
pip install pandas scikit-learn joblib -t build_layer/python/

echo "clean up..."
find build_layer/python/ -type d -name "tests" -exec rm -rf {} +
find build_layer/python/ -type d -name "__pycache__" -exec rm -rf {} +
find build_layer/python/ -name "*.pyc" -delete
rm -rf build_layer/python/*.dist-info
rm -rf build_layer/python/*.egg-info

# you might wanna change this
echo "compressing Layer..."
cd build_layer
powershell.exe -Command "Compress-Archive -Path python -DestinationPath ../terraform/ml_layer.zip -Force"
cd ..

echo "compressing lambdas..."
powershell.exe -Command "Compress-Archive -Path src -DestinationPath terraform/ingestion.zip -Force"
powershell.exe -Command "Compress-Archive -Path src -DestinationPath terraform/inference.zip -Force"

#rm -rf build_layer