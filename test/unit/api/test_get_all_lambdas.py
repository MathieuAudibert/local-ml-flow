import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api.v2.lambdas.get_all_lambdas import get_all_lambdas
from src.main import app

client = TestClient(app)

class TestGetAllLambdas:
    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_returns_lambda_list(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {
            "Functions": [
                {"FunctionName": "lambda1"},
                {"FunctionName": "lambda2"},
                {"FunctionName": "lambda3"}
            ]
        }
        
        response = client.get("/lambda/get-all-lambdas")
        
        assert response.status_code == 200
        assert response.json() == {"lambdas": ["lambda1", "lambda2", "lambda3"]}

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_returns_empty_list(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {"Functions": []}
        
        response = client.get("/lambda/get-all-lambdas")
        
        assert response.status_code == 200
        assert response.json() == {"lambdas": []}

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_handles_missing_functions_key(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {}
        
        response = client.get("/lambda/get-all-lambdas")
        
        assert response.status_code == 200
        assert response.json() == {"lambdas": []}

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_single_lambda(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {
            "Functions": [{"FunctionName": "only-lambda"}]
        }
        
        response = client.get("/lambda/get-all-lambdas")
        
        assert response.status_code == 200
        assert response.json() == {"lambdas": ["only-lambda"]}

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_calls_config(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {"Functions": []}
        
        client.get("/lambda/get-all-lambdas")
        
        mock_config.assert_called_once()

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_calls_list_functions(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.return_value = {"Functions": []}
        
        client.get("/lambda/get-all-lambdas")
        
        mock_lambda.list_functions.assert_called_once()

    @patch("src.api.v2.lambdas.get_all_lambdas.config")
    def test_get_all_lambdas_exception_returns_500(self, mock_config):
        mock_lambda = MagicMock()
        mock_config.return_value = {"s3": MagicMock(), "lambda": mock_lambda}
        mock_lambda.list_functions.side_effect = Exception("Test error")
        
        with TestClient(app, raise_server_exceptions=False) as test_client:
            response = test_client.get("/lambda/get-all-lambdas")
        
        assert response.status_code == 500
        assert "Exception" in response.json()
