import pytest
import pandas as pd
import io
from unittest.mock import patch, MagicMock
from src.core.lambdas.ingestion import ingest, handler

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
        mock_clean_df.return_value = pd.DataFrame()
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
        mock_clean_df.return_value = pd.DataFrame()
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
        mock_clean_df.return_value = pd.DataFrame()
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
        cleaned_df = pd.DataFrame()
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
        mock_clean_df.return_value = pd.DataFrame()
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
        mock_clean_df.return_value = pd.DataFrame()
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
        mock_clean_df.return_value = pd.DataFrame()
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
