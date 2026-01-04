# training the model using linear regression 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from src.config.logger import get_logger
from src.core.model.train_test_split import split

def train(dataset: pd.DataFrame) -> LinearRegression:
    logger = get_logger("train model")
    logger.info("attempting to train model")

    model = LinearRegression()
    x_train_scaled, x_test_scaled, y_train, y_test = split(dataset=dataset)
    
    try: 
        model.fit(x_train_scaled, y_train)
        logger.info("model trained !")
    except Exception as e:
        logger.error(f"error while training the model - {e}")
        raise

    return model
