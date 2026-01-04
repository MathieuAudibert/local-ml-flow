# convert dataset's yes/no to 1/0

import pandas as pd
from src.config.logger import get_logger

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    logger=get_logger("clean_dataframe")
    logger.info("Attempting to clean dataframe (from Yes/no to 1/0)")

    df_clean = df.copy()
    target_columns = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "prefarea"]

    logger.debug(f"initial shape: {df.shape}, columns: {list(df.columns)}")
    logger.debug(f"sum of target columns: {df[target_columns].sum()}")

    try: 
        for col in target_columns:
            df_clean.loc[df_clean[col] == "yes", col] = "1"
            df_clean.loc[df_clean[col] == "no", col] = "0"
        logger.info("Successfully cleaned dataframe")
    
    except Exception as e:
        logger.error(f"failed to clean dataframe - {e}")
        raise

    return df_clean
