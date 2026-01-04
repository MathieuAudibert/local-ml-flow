import os
import boto3
from dotenv import load_dotenv
from src.config.logger import get_logger

def _config() -> list:
    logger = get_logger("client configuration")
    load_dotenv()
    logger.info("loaded dotenv, attempting to create AWS clients")

    clients=[]

    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=os.getenv("endpoint_url"),
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        clients.append(s3_client)

        lambda_client = boto3.client(
            "lambda",
            endpoint_url=os.getenv("endpoint_url"),
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        clients.append(lambda_client)
        logger.info("successfully created clients")

    except Exception as e:
        logger.error(f"error while creating AWS clients - {e}")
        raise

    return clients