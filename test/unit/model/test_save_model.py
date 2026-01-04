import pytest
from unittest.mock import patch, MagicMock
from sklearn.linear_model import LinearRegression
from src.core.model.save_model import save_model

class TestSaveModel:
    @pytest.fixture
    def mock_model(self):
        model = LinearRegression()
        model.coef_ = [1.0, 2.0, 3.0]
        model.intercept_ = 0.5
        return model

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_calls_config(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        mock_config.assert_called_once()

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_uploads_to_s3(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        mock_s3.put_object.assert_called_once()

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_uses_correct_bucket(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        call_kwargs = mock_s3.put_object.call_args[1]
        assert call_kwargs["Bucket"] == "local-ml-flow-models"

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_uses_default_filename(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        call_kwargs = mock_s3.put_object.call_args[1]
        assert call_kwargs["Key"] == "model.joblib"

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_uses_custom_filename(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model, filename="custom_model.joblib")
        
        call_kwargs = mock_s3.put_object.call_args[1]
        assert call_kwargs["Key"] == "custom_model.joblib"

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_logs_info_messages(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        mock_get_logger.assert_called_once_with("save-model")
        assert mock_logger.info.call_count >= 3

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_handles_exception(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = Exception("Upload error")
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        with pytest.raises(Exception) as exc_info:
            save_model(mock_model)
        
        assert "Upload error" in str(exc_info.value)
        mock_logger.error.assert_called_once()

    @patch("src.core.model.save_model.get_logger")
    @patch("src.core.model.save_model.config")
    def test_save_model_body_is_bytes(self, mock_config, mock_get_logger, mock_model):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_s3 = MagicMock()
        mock_config.return_value = {"s3": mock_s3, "lambda": MagicMock()}
        
        save_model(mock_model)
        
        call_kwargs = mock_s3.put_object.call_args[1]
        assert isinstance(call_kwargs["Body"], bytes)
