import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.core.model.evaluation import r2

class TestR2:
    @patch("src.core.model.evaluation.get_logger")
    def test_r2_returns_float(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.1, 2.9, 4.0, 5.1])
        
        result = r2(y_test, y_pred)
        
        assert isinstance(result, float)

    @patch("src.core.model.evaluation.get_logger")
    def test_r2_perfect_prediction(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1, 2, 3, 4, 5])
        
        result = r2(y_test, y_pred)
        
        assert result == 1.0

    @patch("src.core.model.evaluation.get_logger")
    def test_r2_good_prediction(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 1.9, 3.1, 3.9, 5.1])
        
        result = r2(y_test, y_pred)
        
        assert result > 0.9

    @patch("src.core.model.evaluation.get_logger")
    def test_r2_logs_info_message(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1, 2, 3, 4, 5])
        
        r2(y_test, y_pred)
        
        mock_get_logger.assert_called_once_with("r2")
        mock_logger.info.assert_called()

    @patch("src.core.model.evaluation.get_logger")
    @patch("src.core.model.evaluation.r2_score")
    def test_r2_handles_exception(self, mock_r2_score, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_r2_score.side_effect = Exception("Calculation error")
        
        y_test = np.array([1, 2, 3])
        y_pred = np.array([1, 2, 3])
        
        with pytest.raises(Exception) as exc_info:
            r2(y_test, y_pred)
        
        assert "Calculation error" in str(exc_info.value)
        mock_logger.error.assert_called_once()

    @patch("src.core.model.evaluation.get_logger")
    def test_r2_with_negative_values(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = np.array([-5, -2, 0, 2, 5])
        y_pred = np.array([-5, -2, 0, 2, 5])
        
        result = r2(y_test, y_pred)
        
        assert result == 1.0

    @patch("src.core.model.evaluation.get_logger")
    def test_r2_with_list_inputs(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        y_test = [1, 2, 3, 4, 5]
        y_pred = [1, 2, 3, 4, 5]
        
        result = r2(y_test, y_pred)
        
        assert result == 1.0
