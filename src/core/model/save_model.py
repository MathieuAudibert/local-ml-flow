# take the model and serialize it into a binary

import joblib
import io
from src.config.client import config
from src.config.logger import get_logger

def save_model(model, filename="model.joblib"):
    logger = get_logger("save-model")
    clients = config()
    s3_client = clients["s3"]
    bucket_name = "local-ml-flow-models"

    try:
        logger.info("serialize model w/ a buffer")
        model_buffer = io.BytesIO()
        joblib.dump(model, model_buffer)
        model_buffer.seek(0)

        logger.info("attempting to upload it on s3")
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=model_buffer.getvalue())
        logger.info(f"model successfully uploaded to s3://{bucket_name}/{filename}")
        
    except Exception as e:
        logger.error(f"Failed to save model - {e}")
        raise