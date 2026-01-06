from fastapi import APIRouter
from src.config.client import config

router = APIRouter(prefix="/result", tags=["result"])

@router.get("/{bucket_name}")
async def get_result_file(bucket_name: str):
    clients = config()
    s3_client = clients["s3"]
        
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key="result.txt")
        content = response["Body"].read().decode("utf-8")
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}