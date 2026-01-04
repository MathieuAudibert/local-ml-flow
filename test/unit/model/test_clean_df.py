import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.core.model.conversion import clean_df

class TestCleanDf:
    @pytest.fixture
    def sample_dataframe(self):
        return pd.DataFrame({
            "price": [100000, 200000, 300000],
            "area": [1000, 2000, 3000],
            "mainroad": ["yes", "no", "yes"],
            "guestroom": ["no", "yes", "no"],
            "basement": ["yes", "yes", "no"],
            "hotwaterheating": ["no", "no", "yes"],
            "airconditioning": ["yes", "no", "yes"],
            "prefarea": ["no", "yes", "no"]
        })

    @pytest.fixture
    def housing_dataframe(self):
        try:
            return pd.read_csv("src/config/housing.csv")
        except FileNotFoundError:
            pytest.skip("housing.csv not found")

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_returns_dataframe(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        result = clean_df(sample_dataframe)
        
        assert isinstance(result, pd.DataFrame)

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_does_not_modify_original(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        original_copy = sample_dataframe.copy()
        
        clean_df(sample_dataframe)
        
        pd.testing.assert_frame_equal(sample_dataframe, original_copy)

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_preserves_shape(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        original_shape = sample_dataframe.shape
        
        result = clean_df(sample_dataframe)
        
        assert result.shape == original_shape

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_preserves_non_target_columns(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        result = clean_df(sample_dataframe)
        
        pd.testing.assert_series_equal(result["price"], sample_dataframe["price"])
        pd.testing.assert_series_equal(result["area"], sample_dataframe["area"])

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_logs_info_message(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        clean_df(sample_dataframe)
        
        mock_get_logger.assert_called_once_with("clean_dataframe")
        mock_logger.info.assert_called()

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_logs_debug_messages(self, mock_get_logger, sample_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        clean_df(sample_dataframe)
        
        assert mock_logger.debug.call_count >= 2

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_with_housing_csv(self, mock_get_logger, housing_dataframe):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        result = clean_df(housing_dataframe)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == housing_dataframe.shape

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_with_empty_dataframe(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        empty_df = pd.DataFrame(columns=[
            "price", "mainroad", "guestroom", "basement",
            "hotwaterheating", "airconditioning", "prefarea"
        ])
        
        result = clean_df(empty_df)
        
        assert len(result) == 0

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_with_all_yes_values(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        df = pd.DataFrame({
            "mainroad": ["yes", "yes"],
            "guestroom": ["yes", "yes"],
            "basement": ["yes", "yes"],
            "hotwaterheating": ["yes", "yes"],
            "airconditioning": ["yes", "yes"],
            "prefarea": ["yes", "yes"]
        })
        
        result = clean_df(df)
        
        assert isinstance(result, pd.DataFrame)

    @patch("src.core.model.conversion.get_logger")
    def test_clean_df_with_all_no_values(self, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        df = pd.DataFrame({
            "mainroad": ["no", "no"],
            "guestroom": ["no", "no"],
            "basement": ["no", "no"],
            "hotwaterheating": ["no", "no"],
            "airconditioning": ["no", "no"],
            "prefarea": ["no", "no"]
        })
        
        result = clean_df(df)
        
        assert isinstance(result, pd.DataFrame)