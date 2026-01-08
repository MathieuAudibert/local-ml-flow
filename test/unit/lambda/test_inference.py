import pytest
import numpy as np
import io
from unittest.mock import patch, MagicMock
import joblib
from src.core.lambdas.inference import inference, handler

class TestInference:
    @pytest.fixture
    def mock_model(self):
        model = MagicMock()
        model.predict.return_value = np.array([100000, 200000, 150000])
        return model

    @pytest.fixture
    def mock_test_data(self):
        x_test = np.array([[1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1], [1, 1, 0, 0, 1, 1]])
        y_test = np.array([110000, 190000, 160000])
        return x_test, y_test

    @patch("src.core.lambdas.inference.r2")
    @patch("src.core.lambdas.inference.joblib.load")
    @patch("src.core.lambdas.inference.config")
    @patch("src.core.lambdas.inference.get_logger")
    def test_inference_success(self, mock_get_logger, mock_config, mock_joblib_load, mock_r2, mock_model, mock_test_data):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_s3 = MagicMock()
        x_test, y_test = mock_test_data
        
        # Mock S3 responses
        model_body = MagicMock()
        model_body.read.return_value = b"model_binary"
        x_test_body = MagicMock()
        x_test_body.read.return_value = b"x_test_binary"
        y_test_body = MagicMock()
        y_test_body.read.return_value = b"y_test_binary"
        
        mock_s3.get_object.side_effect = [
            {"Body": model_body},
            {"Body": x_test_body},
            {"Body": y_test_body}
        ]
        mock_config.return_value = {"s3": mock_s3}
        
        mock_joblib_load.side_effect = [mock_model, x_test, y_test]
        mock_r2.return_value = 0.85
        
        inference()
        
        assert mock_s3.get_object.call_count == 3
        mock_s3.get_object.assert_any_call(Bucket="local-ml-flow-models", Key="model.joblib")
        mock_s3.get_object.assert_any_call(Bucket="local-ml-flow-data", Key="x_test.joblib")
        mock_s3.get_object.assert_any_call(Bucket="local-ml-flow-data", Key="y_test.joblib")
        mock_model.predict.assert_called_once()
        mock_r2.assert_called_once()
        mock_s3.put_object.assert_called_once_with(Bucket="local-ml-flow-data", Key="score.txt", Body="85.0%")

    @patch("src.core.lambdas.inference.config")
    @patch("src.core.lambdas.inference.get_logger")
    def test_inference_handles_exception(self, mock_get_logger, mock_config):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_s3 = MagicMock()
        mock_s3.get_object.side_effect = Exception("Model not found")
        mock_config.return_value = {"s3": mock_s3}
        
        with pytest.raises(Exception) as exc_info:
            inference()
        
        assert "Model not found" in str(exc_info.value)
        mock_logger.error.assert_called_once()

    @patch("src.core.lambdas.inference.r2")
    @patch("src.core.lambdas.inference.joblib.load")
    @patch("src.core.lambdas.inference.config")
    @patch("src.core.lambdas.inference.get_logger")
    def test_inference_logs_messages(self, mock_get_logger, mock_config, mock_joblib_load, mock_r2, mock_model, mock_test_data):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        mock_s3 = MagicMock()
        x_test, y_test = mock_test_data
        
        model_body = MagicMock()
        model_body.read.return_value = b"model_binary"
        x_test_body = MagicMock()
        x_test_body.read.return_value = b"x_test_binary"
        y_test_body = MagicMock()
        y_test_body.read.return_value = b"y_test_binary"
        
        mock_s3.get_object.side_effect = [
            {"Body": model_body},
            {"Body": x_test_body},
            {"Body": y_test_body}
        ]
        mock_config.return_value = {"s3": mock_s3}
        
        mock_joblib_load.side_effect = [mock_model, x_test, y_test]
        mock_r2.return_value = 0.92
        
        inference()
        
        mock_get_logger.assert_called_once_with("lambda-inference")
        assert mock_logger.info.call_count >= 4


class TestHandler:
    @patch("src.core.lambdas.inference.inference")
    def test_handler_success_returns_200(self, mock_inference):
        mock_inference.return_value = None
        
        result = handler({}, {})
        
        assert result["statusCode"] == 200
        assert result["body"] == "success"

    @patch("src.core.lambdas.inference.inference")
    def test_handler_calls_inference(self, mock_inference):
        mock_inference.return_value = None
        
        handler({}, {})
        
        mock_inference.assert_called_once()

    @patch("src.core.lambdas.inference.inference")
    def test_handler_failure_returns_500(self, mock_inference):
        mock_inference.side_effect = Exception("Inference error")
        
        result = handler({}, {})
        
        assert result["statusCode"] == 500
        assert "Inference error" in result["body"]

    @patch("src.core.lambdas.inference.inference")
    def test_handler_accepts_event_and_context(self, mock_inference):
        mock_inference.return_value = None
        event = {"test": "event"}
        context = {"test": "context"}
        
        result = handler(event, context)
        
        assert result["statusCode"] == 200
