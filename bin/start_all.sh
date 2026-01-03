#!/bin/bash
# this file is to run the project locally, you might wanna change some things there to match your config

echo "starting virtual env"
source venv/Scripts/activate

echo "install and build project"
pip install -e .
pip install -e ".[test]"

echo "starting localstack"
docker compose up -d

echo "start fastapi"
fastapi dev src/main.py