#!/bin/bash
# this file is to run the project locally, you might wanna change some things there to match your config
set -e

echo "****************** starting virtual env ******************"
source venv/Scripts/activate

echo "install and build project"
./bin/install-dependencies.sh

echo "****************** starting docker engine (if not already running)... ******************"
if ! docker info >/dev/null 2>&1; then
    echo "Docker daemon is not running. Please start Docker Desktop manually."
    exit 1
fi

echo "****************** building terraform lambdas ******************"
./bin/build_image.sh

echo "****************** starting localstack ******************"
docker compose up -d --build

echo "****************** waiting for infrastructure to be provisionned (might take a while...) ******************"

echo "waiting for the creation of the s3 bucket(s)"
until docker exec localstack-main awslocal s3 ls s3://local-ml-flow-data >/dev/null 2>&1; do
    echo "terraform still appyling ..."
    sleep 5
done

echo "waiting for the creation of the lambdas"
until docker exec localstack-main awslocal lambda list-functions >/dev/null 2>&1; do
    echo "terraform still appyling ..."
    sleep 5
done

echo "****************** applying the aws lambdas ******************"
echo "waiting for ingestion lambda to be active..."
until aws --endpoint-url=http://localhost:4566 lambda get-function --function-name local-ml-flow-ingestion >/dev/null 2>&1; do
  echo "still waiting for ingestion lambda..."
  sleep 2
done

echo "invoking ingestion lambda..."
aws --endpoint-url=http://localhost:4566 lambda invoke --function-name local-ml-flow-ingestion terraform/logs/output.txt

echo "waiting for inference lambda to be active..."
until aws --endpoint-url=http://localhost:4566 lambda get-function --function-name local-ml-flow-inference >/dev/null 2>&1; do
  echo "still waiting for inference lambda..."
  sleep 2
done

echo "invoking inference lambda..."
aws --endpoint-url=http://localhost:4566 lambda invoke --function-name local-ml-flow-inference terraform/logs/output.txt

echo "******************************************************"
echo "✅ infrastructure ready, starting fastapi"
fastapi dev src/main.py