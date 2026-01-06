# load the dataset, split, train and save model/test data

import pandas as pd
import joblib
import io
from src.config.logger import get_logger
from src.config.client import config
from src.core.model.conversion import clean_df
from src.core.model.train_test_split import split
from src.core.model.train import train
from src.core.model.save_model import save_model

def save_test_data(s3_client, x_test, y_test) -> None:
    bucket_name = "local-ml-flow-data"
    x_buffer = io.BytesIO()
    joblib.dump(x_test, x_buffer)
    x_buffer.seek(0)
    s3_client.put_object(Bucket=bucket_name, Key="x_test.joblib", Body=x_buffer.getvalue())
    
    y_buffer = io.BytesIO()
    joblib.dump(y_test, y_buffer)
    y_buffer.seek(0)
    s3_client.put_object(Bucket=bucket_name, Key="y_test.joblib", Body=y_buffer.getvalue())

def ingest() -> None:
    logger=get_logger("lambda-ingestion")
    clients = config()
    s3_client = clients["s3"]
    bucket_name = "local-ml-flow-data"
    obj_name = "housing.csv"

    try:
        logger.info("attempting to retrieve dataset")
        response = s3_client.get_object(Bucket=bucket_name, Key=obj_name)
        base_df = pd.read_csv(response["Body"])

        logger.info("retrieved dataset, now cleaning it")
        housing = clean_df(df=base_df)

        logger.info("splitting into train and test data")
        x_train, x_test, y_train, y_test = split(dataset=housing)

        logger.info("training model on training data")
        model_object = train(x_train=x_train, y_train=y_train)

        logger.info("saving model")
        save_model(model=model_object)

        logger.info("saving test data for inference")
        save_test_data(s3_client, x_test, y_test)

    except Exception as e:
        logger.error(f"error while ingest - {e}")
        raise

    return None

def handler(event, context) -> dict:
    try:
        ingest()
        return {"statuscode": 200, "body": "success"}

    except Exception as e:
        return {"statuscode": 500, "body": str(e)}