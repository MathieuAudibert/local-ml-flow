import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from sklearn.linear_model import LinearRegression
from src.core.model.train import train

class TestTrain:
    @pytest.fixture
    def sample_training_data(self):
        np.random.seed(42)
        x_train = np.random.rand(80, 6)
        y_train = np.random.rand(80)
        return x_train, y_train

    @patch("src.core.model.train.get_logger")
    def test_train_returns_linear_regression_model(self, mock_get_logger, sample_training_data):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train, y_train = sample_training_data
        
        result = train(x_train=x_train, y_train=y_train)
        
        assert isinstance(result, LinearRegression)

    @patch("src.core.model.train.get_logger")
    def test_train_logs_info_messages(self, mock_get_logger, sample_training_data):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train, y_train = sample_training_data
        
        train(x_train=x_train, y_train=y_train)
        
        mock_get_logger.assert_called_once_with("train model")
        assert mock_logger.info.call_count >= 2

    @patch("src.core.model.train.get_logger")
    def test_train_handles_exception(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Invalid data that will cause fit to fail
        x_train = None
        y_train = None
        
        with pytest.raises(Exception):
            train(x_train=x_train, y_train=y_train)

    @patch("src.core.model.train.get_logger")
    def test_train_model_is_fitted(self, mock_get_logger, sample_training_data):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train, y_train = sample_training_data
        
        model = train(x_train=x_train, y_train=y_train)
        
        # Check that model has been fitted by verifying it has coefficients
        assert hasattr(model, 'coef_')
        assert len(model.coef_) == 6

    @patch("src.core.model.train.get_logger")
    @patch("src.core.model.train.LinearRegression")
    def test_train_logs_error_on_fit_failure(self, mock_linear_regression, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Mock LinearRegression to raise exception on fit
        mock_model = MagicMock()
        mock_model.fit.side_effect = Exception("Fit error")
        mock_linear_regression.return_value = mock_model
        
        x_train = np.random.rand(80, 6)
        y_train = np.random.rand(80)
        
        with pytest.raises(Exception):
            train(x_train=x_train, y_train=y_train)
        
        mock_logger.error.assert_called_once()
