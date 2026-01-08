from fastapi import APIRouter
from src.config.client import config

router = APIRouter(prefix="/bucket", tags=["buckets"])

@router.get("/get-all-models")
async def get_all_models():
    clients=config()
    s3_client = clients["s3"]
    
    response = s3_client.list_buckets()
    buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
    
    all_models = []
    for bucket_name in buckets:
        try:
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in objects:
                models = [obj['Key'] for obj in objects['Contents']]
                all_models.extend([{"bucket": bucket_name, "model": model} for model in models])
        except Exception:
            continue
    
    return {"models": all_models}