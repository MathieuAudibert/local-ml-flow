import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

class TestGetResult:
    @patch("src.api.v3.result.get_result.config")
    def test_get_result_file_success(self, mock_config):
        mock_s3 = MagicMock()
        mock_body = MagicMock()
        mock_body.read.return_value = b"85.5%"
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/result/local-ml-flow-data")
        
        assert response.status_code == 200
        assert response.json() == {"content": "85.5%"}
        mock_s3.get_object.assert_called_once_with(Bucket="local-ml-flow-data", Key="score.txt")

    @patch("src.api.v3.result.get_result.config")
    def test_get_result_file_error(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.get_object.side_effect = Exception("Bucket not found")
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/result/test-bucket")
        
        assert response.status_code == 200
        assert "error" in response.json()
        assert "Bucket not found" in response.json()["error"]

    @patch("src.api.v3.result.get_result.config")
    def test_get_result_file_different_bucket(self, mock_config):
        mock_s3 = MagicMock()
        mock_body = MagicMock()
        mock_body.read.return_value = b"92.3%"
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/result/my-custom-bucket")
        
        assert response.status_code == 200
        assert response.json() == {"content": "92.3%"}
        mock_s3.get_object.assert_called_once_with(Bucket="my-custom-bucket", Key="score.txt")
