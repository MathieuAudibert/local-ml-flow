# keeping data aside to test

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.config.logger import get_logger

def split(dataset: pd.DataFrame) -> tuple:
    logger = get_logger("split training data and tests")
    logger.info("attempting to split data")

    target_columns = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "prefarea"]
    try:
        x=pd.DataFrame(dataset, columns=target_columns)
        y=dataset.price
        # 80% into the training, 20% into tests
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    except Exception as e:
        logger.error(f"error while splitting train and tests - {e}")
    
    logger.info("attempting to normalise caracteristics")
    scaler = StandardScaler()

    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    
    return x_train_scaled, x_test_scaled, y_train, y_test
