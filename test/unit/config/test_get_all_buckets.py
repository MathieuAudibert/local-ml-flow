import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api.v2.bucket.get_all_buckets import get_all_buckets
from src.main import app, default_exception_handler

client = TestClient(app)

class TestReadRoot:
    def test_read_root_returns_app_info(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "app": "Local Machine Learning Flow",
            "endpoints": ["/bucket/get-all-buckets"]
        }


class TestDefaultExceptionHandler:
    def test_exception_handler_returns_500(self):
        with patch("src.api.v2.bucket.get_all_buckets.boto3.client") as mock_client:
            mock_s3 = MagicMock()
            mock_client.return_value = mock_s3
            mock_s3.list_buckets.side_effect = Exception("Test error")
            with TestClient(app, raise_server_exceptions=False) as test_client:
                response = test_client.get("/bucket/get-all-buckets")
            assert response.status_code == 500
            assert "Exception" in response.json()


class TestGetAllBuckets:
    @patch("src.api.v2.bucket.get_all_buckets.boto3.client")
    def test_get_all_buckets_returns_bucket_list(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_buckets.return_value = {
            "Buckets": [
                {"Name": "bucket1"},
                {"Name": "bucket2"},
                {"Name": "bucket3"}
            ]
        }
        
        response = client.get("/bucket/get-all-buckets")
        
        assert response.status_code == 200
        assert response.json() == {"buckets": ["bucket1", "bucket2", "bucket3"]}

    @patch("src.api.v2.bucket.get_all_buckets.boto3.client")
    def test_get_all_buckets_returns_empty_list(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_buckets.return_value = {"Buckets": []}
        
        response = client.get("/bucket/get-all-buckets")
        
        assert response.status_code == 200
        assert response.json() == {"buckets": []}

    @patch("src.api.v2.bucket.get_all_buckets.boto3.client")
    def test_get_all_buckets_handles_missing_buckets_key(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_buckets.return_value = {}
        
        response = client.get("/bucket/get-all-buckets")
        
        assert response.status_code == 200
        assert response.json() == {"buckets": []}

    @patch("src.api.v2.bucket.get_all_buckets.os.getenv")
    @patch("src.api.v2.bucket.get_all_buckets.boto3.client")
    def test_get_all_buckets_uses_environment_variables(self, mock_boto_client, mock_getenv):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_buckets.return_value = {"Buckets": []}
        
        env_values = {
            "endpoint_url": "http://localhost:9000",
            "aws_access_key_id": "test_key",
            "aws_secret_access_key": "test_secret",
            "region_name": "us-east-1"
        }
        mock_getenv.side_effect = lambda key: env_values.get(key)
        
        response = client.get("/bucket/get-all-buckets")
        
        assert response.status_code == 200

    @patch("src.api.v2.bucket.get_all_buckets.boto3.client")
    def test_get_all_buckets_single_bucket(self, mock_boto_client):
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        mock_s3.list_buckets.return_value = {
            "Buckets": [{"Name": "only-bucket"}]
        }
        
        response = client.get("/bucket/get-all-buckets")
        
        assert response.status_code == 200
        assert response.json() == {"buckets": ["only-bucket"]}