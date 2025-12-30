import boto3
import os
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/bucket", tags=["buckets"])

@router.get("/get-all-buckets")
async def get_all_buckets():
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("endpoint_url"),
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        region_name=os.getenv("region_name")
    )
    
    response = s3_client.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
    
    return {"buckets": buckets}