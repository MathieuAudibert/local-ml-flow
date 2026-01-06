from fastapi import APIRouter
from src.config.client import config

router = APIRouter(prefix="/lambda", tags=["lambdas"])

@router.get("/get-all-lambdas")
async def get_all_lambdas():
    clients=config()
    lambda_client = clients["lambda"]
    
    response = lambda_client.list_functions()
    lambdas = [lambdaa["FunctionName"] for lambdaa in response.get("Functions", [])]
    
    return {"lambdas": lambdas}