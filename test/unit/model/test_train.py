import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from sklearn.linear_model import LinearRegression
from src.core.model.train import train

class TestTrain:
    @pytest.fixture
    def sample_dataset(self):
        np.random.seed(42)
        n_samples = 100
        return pd.DataFrame({
            "price": np.random.randint(100000, 500000, n_samples),
            "mainroad": np.random.choice(["1", "0"], n_samples),
            "guestroom": np.random.choice(["1", "0"], n_samples),
            "basement": np.random.choice(["1", "0"], n_samples),
            "hotwaterheating": np.random.choice(["1", "0"], n_samples),
            "airconditioning": np.random.choice(["1", "0"], n_samples),
            "prefarea": np.random.choice(["1", "0"], n_samples)
        })

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_returns_linear_regression_model(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train = np.random.rand(80, 6)
        x_test = np.random.rand(20, 6)
        y_train = np.random.rand(80)
        y_test = np.random.rand(20)
        mock_split.return_value = (x_train, x_test, y_train, y_test)
        
        result = train(sample_dataset)
        
        assert isinstance(result, LinearRegression)

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_calls_split(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train = np.random.rand(80, 6)
        x_test = np.random.rand(20, 6)
        y_train = np.random.rand(80)
        y_test = np.random.rand(20)
        mock_split.return_value = (x_train, x_test, y_train, y_test)
        
        train(sample_dataset)
        
        mock_split.assert_called_once_with(dataset=sample_dataset)

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_logs_info_messages(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train = np.random.rand(80, 6)
        x_test = np.random.rand(20, 6)
        y_train = np.random.rand(80)
        y_test = np.random.rand(20)
        mock_split.return_value = (x_train, x_test, y_train, y_test)
        
        train(sample_dataset)
        
        mock_get_logger.assert_called_once_with("train model")
        assert mock_logger.info.call_count >= 2

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_handles_exception(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_split.side_effect = Exception("Split error")
        
        with pytest.raises(Exception) as exc_info:
            train(sample_dataset)
        
        assert "Split error" in str(exc_info.value)

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_model_is_fitted(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        np.random.seed(42)
        x_train = np.random.rand(80, 6)
        x_test = np.random.rand(20, 6)
        y_train = np.random.rand(80)
        y_test = np.random.rand(20)
        mock_split.return_value = (x_train, x_test, y_train, y_test)
        
        model = train(sample_dataset)
        
        # Check that model has been fitted by verifying it has coefficients
        assert hasattr(model, 'coef_')
        assert len(model.coef_) == 6

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.split")
    def test_train_logs_error_on_fit_failure(self, mock_split, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Return invalid data that will cause fit to fail
        mock_split.return_value = (None, None, None, None)
        
        with pytest.raises(Exception):
            train(sample_dataset)
        
        mock_logger.error.assert_called_once()
