from fastapi import APIRouter
from src.config.client import config
import csv
from io import StringIO

router = APIRouter(prefix="/bucket", tags=["buckets"])

@router.get("/dataset")
async def get_dataset():
    clients = config()
    s3_client = clients["s3"]
        
    bucket_name = "local-ml-flow-data"
    key = "housing.csv"
        
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    data = response['Body'].read().decode('utf-8')
                
    csv_reader = csv.DictReader(StringIO(data))
    values = list(csv_reader)
        
    return {
        "dataset_name": "housing.csv",
        "bucket": bucket_name,
        "key": key,
        "row_count": len(values),
        "values": values
    }
    

