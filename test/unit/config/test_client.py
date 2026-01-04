import pytest
from unittest.mock import patch, MagicMock
from src.config.client import config

class TestConfig:
    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_returns_list(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        result = config()
        
        assert isinstance(result, list)

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_returns_two_clients(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        result = config()
        
        assert len(result) == 2

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_calls_load_dotenv(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        mock_load_dotenv.assert_called_once()

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_creates_s3_client(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        calls = mock_boto_client.call_args_list
        s3_call = [call for call in calls if call[0][0] == "s3"]
        assert len(s3_call) == 1

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_creates_lambda_client(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        calls = mock_boto_client.call_args_list
        lambda_call = [call for call in calls if call[0][0] == "lambda"]
        assert len(lambda_call) == 1

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_uses_environment_variables(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        env_values = {
            "endpoint_url": "http://localhost:4566",
            "aws_access_key_id": "test_key",
            "aws_secret_access_key": "test_secret",
            "region_name": "us-east-1"
        }
        mock_getenv.side_effect = lambda key: env_values.get(key)
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        assert mock_getenv.call_count >= 4

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_logs_info_on_success(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        assert mock_logger.info.call_count >= 2

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_raises_exception_on_client_error(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.side_effect = Exception("Client creation failed")
        
        with pytest.raises(Exception) as exc_info:
            config()
        
        assert "Client creation failed" in str(exc_info.value)

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_logs_error_on_exception(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.side_effect = Exception("Client creation failed")
        
        with pytest.raises(Exception):
            config()
        
        mock_logger.error.assert_called_once()

    @patch("src.config.client.get_logger")
    @patch("src.config.client.load_dotenv")
    @patch("src.config.client.boto3.client")
    @patch("src.config.client.os.getenv")
    def test_config_creates_logger_with_correct_name(self, mock_getenv, mock_boto_client, mock_load_dotenv, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_getenv.return_value = "test_value"
        mock_boto_client.return_value = MagicMock()
        
        config()
        
        mock_get_logger.assert_called_once_with("client configuration")