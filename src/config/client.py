import os
import boto3
from dotenv import load_dotenv
from src.config.logger import get_logger

def config() -> dict:
    logger = get_logger("client-configuration")
    load_dotenv()
    logger.info("loaded dotenv, attempting to create AWS clients")

    endpoint = os.getenv("endpoint_url")
    clients={}

    try:
        common_config = {
            "endpoint_url": endpoint,
            "aws_access_key_id": os.getenv("aws_access_key_id"),
            "aws_secret_access_key": os.getenv("aws_secret_access_key"),
            "region_name": os.getenv("region_name")
        }
        clients["s3"] = boto3.client("s3", **common_config)
        clients["lambda"] = boto3.client("lambda", **common_config)
        logger.info("successfully created clients")

    except Exception as e:
        logger.error(f"error while creating AWS clients - {e}")
        raise

    return clients