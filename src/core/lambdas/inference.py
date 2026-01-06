# download the binary, download the test dataset, make the prediction and get the score

import joblib
import io
from src.config.logger import get_logger
from src.config.client import config
from src.core.model.evaluation import r2

def inference() -> None:
    logger = get_logger("lambda-inference")
    clients = config()
    s3_client = clients["s3"]
    model_bucket_name = "local-ml-flow-models"
    data_bucket_name = "local-ml-flow-data"
    obj_name = "model.joblib"
    x_test_name = "x_test.joblib"
    y_test_name = "y_test.joblib"

    try:
        logger.info("attempting to get the binary (model)")
        model_res = s3_client.get_object(Bucket=model_bucket_name, Key=obj_name)
        model = joblib.load(io.BytesIO(model_res["Body"].read()))

        logger.info("attempting to retrieve test dataset(s) and testing model")
        x_res = s3_client.get_object(Bucket=data_bucket_name, Key = x_test_name)
        y_res = s3_client.get_object(Bucket=data_bucket_name, Key= y_test_name)
        
        x_test = joblib.load(io.BytesIO(x_res["Body"].read()))
        y_test = joblib.load(io.BytesIO(y_res["Body"].read()))

        y_pred = model.predict(x_test)

        logger.info("calculating R2")
        r2_score = r2(y_test, y_pred)

        logger.info("putting the score as %")
        r2_percentage = str(r2_score * 100) + "%"

        logger.info("saving the score in a textfile in the bucket")
        s3_client.put_object(Bucket=data_bucket_name, Key="score.txt", Body=r2_percentage)
    except Exception as e:
        logger.error(f"error while inference - {e}")
        raise

def handler(event, context) -> dict:
    try:
        inference()
        return {"statuscode": 200, "body": "success"}

    except Exception as e:
        return {"statuscode": 500, "body": str(e)}
