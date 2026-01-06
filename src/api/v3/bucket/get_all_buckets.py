from fastapi import APIRouter
from src.config.client import config

router = APIRouter(prefix="/bucket", tags=["buckets"])

@router.get("/get-all-buckets")
async def get_all_buckets():
    clients=config()
    s3_client = clients["s3"]
    
    response = s3_client.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
    
    return {"buckets": buckets}