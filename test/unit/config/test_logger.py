import pytest
import logging
import sys
from unittest.mock import patch, MagicMock
from src.config.logger import get_logger

class TestGetLogger:
    def test_get_logger_returns_logger_instance(self):
        logger = get_logger("test_logger")
        
        assert isinstance(logger, logging.Logger)

    def test_get_logger_returns_logger_with_correct_name(self):
        logger = get_logger("my_custom_logger")
        
        assert logger.name == "my_custom_logger"

    def test_get_logger_sets_info_level(self):
        logger = get_logger("level_test_logger")
        
        assert logger.level == logging.INFO

    def test_get_logger_adds_handler(self):
        logger_name = "handler_test_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        assert len(logger.handlers) >= 1

    def test_get_logger_adds_stream_handler(self):
        logger_name = "stream_handler_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) >= 1

    def test_get_logger_handler_uses_stdout(self):
        logger_name = "stdout_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert any(h.stream == sys.stdout for h in stream_handlers)

    def test_get_logger_does_not_add_duplicate_handlers(self):
        logger_name = "duplicate_handler_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger1 = get_logger(logger_name)
        initial_handler_count = len(logger1.handlers)
        
        logger2 = get_logger(logger_name)
        
        assert len(logger2.handlers) == initial_handler_count

    def test_get_logger_returns_same_logger_for_same_name(self):
        logger1 = get_logger("same_name_logger")
        logger2 = get_logger("same_name_logger")
        
        assert logger1 is logger2

    def test_get_logger_returns_different_loggers_for_different_names(self):
        logger1 = get_logger("first_logger")
        logger2 = get_logger("second_logger")
        
        assert logger1 is not logger2
        assert logger1.name != logger2.name

    def test_get_logger_formatter_format(self):
        logger_name = "formatter_test_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        handler = logger.handlers[0]
        expected_format = '[%(asctime)s][%(levelname)s]: %(name)s - %(message)s'
        assert handler.formatter._fmt == expected_format

    def test_get_logger_can_log_info(self):
        logger_name = "info_log_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        with patch.object(logger.handlers[0], 'emit') as mock_emit:
            logger.info("Test message")
            mock_emit.assert_called_once()

    def test_get_logger_can_log_error(self):
        logger_name = "error_log_logger"
        logging.getLogger(logger_name).handlers.clear()
        
        logger = get_logger(logger_name)
        
        with patch.object(logger.handlers[0], 'emit') as mock_emit:
            logger.error("Error message")
            mock_emit.assert_called_once()

    def test_get_logger_with_empty_string_name(self):
        logger = get_logger("")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "root"