import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.core.model.train_test_split import split

class TestSplit:
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

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_returns_tuple(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        result = split(sample_dataset)
        
        assert isinstance(result, tuple)
        assert len(result) == 4

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_returns_correct_sizes(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train_scaled, x_test_scaled, y_train, y_test = split(sample_dataset)
        
        # 80% training, 20% test
        assert len(y_train) == 80
        assert len(y_test) == 20

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_returns_scaled_features(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train_scaled, x_test_scaled, y_train, y_test = split(sample_dataset)
        
        # Check that features are numpy arrays
        assert isinstance(x_train_scaled, np.ndarray)
        assert isinstance(x_test_scaled, np.ndarray)

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_logs_info_messages(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        split(sample_dataset)
        
        mock_get_logger.assert_called_once_with("split training data and tests")
        assert mock_logger.info.call_count >= 2

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_feature_dimensions(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train_scaled, x_test_scaled, y_train, y_test = split(sample_dataset)
        
        # 6 features: mainroad, guestroom, basement, hotwaterheating, airconditioning, prefarea
        assert x_train_scaled.shape[1] == 6
        assert x_test_scaled.shape[1] == 6

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_y_values_are_series(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train_scaled, x_test_scaled, y_train, y_test = split(sample_dataset)
        
        assert isinstance(y_train, pd.Series)
        assert isinstance(y_test, pd.Series)

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_reproducibility(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        result1 = split(sample_dataset)
        result2 = split(sample_dataset)
        
        # With random_state=42, results should be identical
        np.testing.assert_array_equal(result1[0], result2[0])
        np.testing.assert_array_equal(result1[1], result2[1])

    @patch("src.core.model.train_test_split.get_logger")
    def test_split_scaled_values_normalized(self, mock_get_logger, sample_dataset):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        x_train_scaled, x_test_scaled, y_train, y_test = split(sample_dataset)
        
        # Training data should be approximately normalized (mean ~0, std ~1)
        # Due to binary data, this might not be exact but should be close
        assert np.abs(np.mean(x_train_scaled)) < 0.5
