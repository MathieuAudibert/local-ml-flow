#!/bin/bash

echo "localstack hook, starting terraform"
cd /etc/localstack/init/terraform

terraform init
terraform apply -var-file="terraform.tfvars" -auto-approve
echo "terraform applied"

echo "copy dataset to S3..."
awslocal s3 cp /tmp/data/housing.csv s3://local-ml-flow-data/housing.csv