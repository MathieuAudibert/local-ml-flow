#!/bin/bash
# this script calls the dockerfile for the lambdas wich bypass the free tier localstack lambda limit
set -e
echo "building docker image"

rm -f terraform/ingestion.zip terraform/inference.zip
mkdir -p terraform
echo "using Docker to build and ZIP..."

docker run --rm --entrypoint bash -v "/${PWD}:/project" public.ecr.aws/lambda/python:3.10 -c "
    if [ ! -d '/project/src' ]; then
        echo 'ERROR: /project/src not found. Check Docker volume mounts.';
        exit 1;
    fi

    echo 'installing dependencies...'
    mkdir -p /tmp/package
    pip install pandas scikit-learn joblib python-dotenv numpy -t /tmp/package --quiet --platform manylinux2014_x86_64 --only-binary=:all:
    cp -r /project/src /tmp/package/
    
    cd /tmp/package
    
    echo 'removing test files and reducing size...'
    find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name '*.dist-info' -exec rm -rf {} + 2>/dev/null || true
        
    find . -name '*.pyc' -delete
    find . -name '*.pyo' -delete
    find . -name '*.pyd' -delete
    
    yum install -y zip > /dev/null 2>&1 || true
    zip -r9 /project/terraform/ingestion.zip . > /dev/null
    cp /project/terraform/ingestion.zip /project/terraform/inference.zip
"

if [ -f "terraform/ingestion.zip" ]; then
    echo "zips created in /terraform"
    du -h terraform/ingestion.zip
else
    echo "failed to create Zips."
fi