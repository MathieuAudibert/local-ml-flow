#!/bin/bash
# this file is to run the project locally, you might wanna change some things there to match your config

echo "starting virtual env"
source venv/Scripts/activate

echo "install and build project"
./bin/install-dependencies.sh

echo "starting localstack"
docker compose up -d --build

echo "waiting for infrastructure to be provisionned (might take a while...)"
until docker exec localstack-main awslocal s3 ls s3://local-ml-flow-data >/dev/null 2>&1; do
    echo "terraform still appyling ..."
    sleep 5
done

echo "✅ infrastructure ready, starting fastapi"
fastapi dev src/main.py