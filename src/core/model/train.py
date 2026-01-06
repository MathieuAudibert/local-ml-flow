# training the model using linear regression 

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from src.config.logger import get_logger

def train(x_train, y_train) -> LinearRegression:
    logger = get_logger("train model")
    logger.info("attempting to train model")

    model = LinearRegression()
    
    try: 
        model.fit(x_train, y_train)
        logger.info("model trained !")
    except Exception as e:
        logger.error(f"error while training the model - {e}")
        raise

    return model
