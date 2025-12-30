import pytest
from unittest.mock import patch, MagicMock
from src.main import app, default_exception_handler

class TestAppConfiguration:
    def test_app_title(self):
        assert app.title == "local-ml-testing"

    def test_app_description(self):
        assert app.description == "Api to handle lambdas and ML interactions"

    def test_bucket_router_included(self):
        routes = [route.path for route in app.routes]
        assert "/bucket/get-all-buckets" in routes