#!/bin/bash
echo "copy dataset to S3..."
awslocal s3 cp /tmp/data/housing.csv s3://local-ml-flow-data/housing.csv