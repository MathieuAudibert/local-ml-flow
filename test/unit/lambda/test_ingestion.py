import pytest
import pandas as pd
import numpy as np
import io
from unittest.mock import patch, MagicMock
from src.core.lambdas.ingestion import ingest, handler, save_test_data

class TestIngest:
    @pytest.fixture
    def mock_csv_content(self):
        csv_data = """price,area,mainroad,guestroom,basement,hotwaterheating,airconditioning,prefarea
100000,1000,yes,no,yes,no,yes,no
200000,2000,no,yes,yes,no,no,yes
300000,3000,yes,no,no,yes,yes,no"""
        return io.BytesIO(csv_data.encode())

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_calls_config(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_train.return_value = MagicMock()
        
        ingest()
        
        mock_config.assert_called_once()

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_retrieves_from_s3(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_train.return_value = MagicMock()
        
        ingest()
        
        mock_s3.get_object.assert_called_once_with(Bucket="local-ml-flow-data", Key="housing.csv")

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_calls_clean_df(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_train.return_value = MagicMock()
        
        ingest()
        
        mock_clean_df.assert_called_once()

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_calls_train(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        cleaned_df = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_clean_df.return_value = cleaned_df
        mock_train.return_value = MagicMock()
        
        ingest()
        
        mock_train.assert_called_once()

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_calls_save_model(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_model = MagicMock()
        mock_train.return_value = mock_model
        
        ingest()
        
        mock_save_model.assert_called_once_with(model=mock_model)

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_returns_none(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_train.return_value = MagicMock()
        
        result = ingest()
        
        assert result is None

    @patch("src.core.lambdas.ingestion.save_model")
    @patch("src.core.lambdas.ingestion.train")
    @patch("src.core.lambdas.ingestion.clean_df")
    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_logs_info_messages(self, mock_get_logger, mock_config, mock_clean_df, mock_train, mock_save_model, mock_csv_content):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {"Body": mock_csv_content}
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        mock_clean_df.return_value = pd.DataFrame({"price": [100]*10, "mainroad": [0]*10, "guestroom": [0]*10, "basement": [0]*10, "hotwaterheating": [0]*10, "airconditioning": [0]*10, "prefarea": [0]*10})
        mock_train.return_value = MagicMock()
        
        ingest()
        
        mock_get_logger.assert_called_with("lambda-ingestion")
        assert mock_logger.info.call_count >= 4

    @patch("src.core.lambdas.ingestion.config")
    @patch("src.core.lambdas.ingestion.get_logger")
    def test_ingest_handles_exception(self, mock_get_logger, mock_config):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.get_object.side_effect = Exception("S3 error")
        mock_config.return_value = {"s3": mock_s3, "lambdas": MagicMock()}
        
        with pytest.raises(Exception) as exc_info:
            ingest()
        
        assert "S3 error" in str(exc_info.value)
        mock_logger.error.assert_called_once()


class TestSaveTestData:
    def test_save_test_data_saves_both_files(self):
        mock_s3 = MagicMock()
        x_test = np.array([[1, 2, 3], [4, 5, 6]])
        y_test = np.array([100, 200])
        
        save_test_data(mock_s3, x_test, y_test)
        
        assert mock_s3.put_object.call_count == 2
        calls = mock_s3.put_object.call_args_list
        assert calls[0][1]["Bucket"] == "local-ml-flow-data"
        assert calls[0][1]["Key"] == "x_test.joblib"
        assert calls[1][1]["Bucket"] == "local-ml-flow-data"
        assert calls[1][1]["Key"] == "y_test.joblib"

    def test_save_test_data_calls_with_correct_data(self):
        mock_s3 = MagicMock()
        x_test = np.array([[1, 0], [0, 1]])
        y_test = np.array([50, 60])
        
        save_test_data(mock_s3, x_test, y_test)
        
        assert mock_s3.put_object.call_count == 2


class TestHandler:
    @patch("src.core.lambdas.ingestion.ingest")
    def test_handler_success_returns_200(self, mock_ingest):
        mock_ingest.return_value = None
        
        result = handler({}, {})
        
        assert result["statusCode"] == 200
        assert result["body"] == "success"

    @patch("src.core.lambdas.ingestion.ingest")
    def test_handler_calls_ingest(self, mock_ingest):
        mock_ingest.return_value = None
        
        handler({}, {})
        
        mock_ingest.assert_called_once()

    @patch("src.core.lambdas.ingestion.ingest")
    def test_handler_failure_returns_500(self, mock_ingest):
        mock_ingest.side_effect = Exception("Ingest error")
        
        result = handler({}, {})
        
        assert result["statusCode"] == 500
        assert "Ingest error" in result["body"]

    @patch("src.core.lambdas.ingestion.ingest")
    def test_handler_accepts_event_and_context(self, mock_ingest):
        mock_ingest.return_value = None
        event = {"test": "event"}
        context = {"test": "context"}
        
        result = handler(event, context)
        
        assert result["statusCode"] == 200
