import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app
import io

client = TestClient(app)

class TestGetDataset:
    @patch("src.api.v3.bucket.get_dataset.config")
    def test_get_dataset_success(self, mock_config):
        mock_s3 = MagicMock()
        csv_data = "price,area,mainroad\n100000,1000,yes\n200000,2000,no"
        mock_body = MagicMock()
        mock_body.read.return_value = csv_data.encode('utf-8')
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/dataset")
        
        assert response.status_code == 200
        data = response.json()
        assert data["dataset_name"] == "housing.csv"
        assert data["bucket"] == "local-ml-flow-data"
        assert data["key"] == "housing.csv"
        assert data["row_count"] == 2
        assert len(data["values"]) == 2
        assert data["values"][0]["price"] == "100000"
        assert data["values"][0]["area"] == "1000"
        assert data["values"][0]["mainroad"] == "yes"

    @patch("src.api.v3.bucket.get_dataset.config")
    def test_get_dataset_empty_csv(self, mock_config):
        mock_s3 = MagicMock()
        csv_data = "price,area,mainroad"
        mock_body = MagicMock()
        mock_body.read.return_value = csv_data.encode('utf-8')
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/dataset")
        
        assert response.status_code == 200
        data = response.json()
        assert data["row_count"] == 0
        assert data["values"] == []

    @patch("src.api.v3.bucket.get_dataset.config")
    def test_get_dataset_calls_s3_correctly(self, mock_config):
        mock_s3 = MagicMock()
        csv_data = "col1\nval1"
        mock_body = MagicMock()
        mock_body.read.return_value = csv_data.encode('utf-8')
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/dataset")
        
        assert response.status_code == 200
        mock_s3.get_object.assert_called_once_with(Bucket="local-ml-flow-data", Key="housing.csv")

    @patch("src.api.v3.bucket.get_dataset.config")
    def test_get_dataset_multiple_rows(self, mock_config):
        mock_s3 = MagicMock()
        csv_data = "name,age\nAlice,30\nBob,25\nCharlie,35"
        mock_body = MagicMock()
        mock_body.read.return_value = csv_data.encode('utf-8')
        mock_s3.get_object.return_value = {"Body": mock_body}
        mock_config.return_value = {"s3": mock_s3}
        
        response = client.get("/bucket/dataset")
        
        assert response.status_code == 200
        data = response.json()
        assert data["row_count"] == 3
        assert data["values"][0]["name"] == "Alice"
        assert data["values"][1]["name"] == "Bob"
        assert data["values"][2]["name"] == "Charlie"
