import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

class TestGetAllModels:
    @patch("src.api.v3.bucket.get_all_models.config")
    def test_get_all_models_success(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [
                {"Name": "bucket1"},
                {"Name": "bucket2"}
            ]
        }
        mock_s3.list_objects_v2.side_effect = [
            {"Contents": [{"Key": "model1.joblib"}, {"Key": "model2.joblib"}]},
            {"Contents": [{"Key": "model3.pkl"}]}
        ]
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/get-all-models")
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) == 3
        assert {"bucket": "bucket1", "model": "model1.joblib"} in data["models"]
        assert {"bucket": "bucket1", "model": "model2.joblib"} in data["models"]
        assert {"bucket": "bucket2", "model": "model3.pkl"} in data["models"]

    @patch("src.api.v3.bucket.get_all_models.config")
    def test_get_all_models_empty_buckets(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {"Buckets": []}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/get-all-models")
        
        assert response.status_code == 200
        assert response.json() == {"models": []}

    @patch("src.api.v3.bucket.get_all_models.config")
    def test_get_all_models_bucket_without_contents(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [{"Name": "empty-bucket"}]
        }
        mock_s3.list_objects_v2.return_value = {}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/get-all-models")
        
        assert response.status_code == 200
        assert response.json() == {"models": []}

    @patch("src.api.v3.bucket.get_all_models.config")
    def test_get_all_models_with_exception(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [
                {"Name": "bucket1"},
                {"Name": "bucket2"}
            ]
        }
        mock_s3.list_objects_v2.side_effect = [
            Exception("Access denied"),
            {"Contents": [{"Key": "model.joblib"}]}
        ]
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/get-all-models")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["models"]) == 1
        assert {"bucket": "bucket2", "model": "model.joblib"} in data["models"]

    @patch("src.api.v3.bucket.get_all_models.config")
    def test_get_all_models_no_buckets_key(self, mock_config):
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/get-all-models")
        
        assert response.status_code == 200
        assert response.json() == {"models": []}
