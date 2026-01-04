# check R² to see the accuracy

from sklearn.metrics import mean_squared_error, r2_score
from src.config.logger import get_logger

def r2(y_test, y_pred) -> float:
    logger = get_logger("r2")
    logger.info("attempting to calculate...")
    r2=0
    
    try:
        r2 = r2_score(y_test, y_pred)

    except Exception as e:
        logger.error(f"error while calculating r2 - {e}")
        raise

    return r2
