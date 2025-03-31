import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import lambda_function
import requests

def test_process_launch():
    sample_launch = {
        "id": "abc123",
        "name": "Test Mission",
        "date_utc": "2025-03-30T00:00:00Z",
        "rocket": "rocket_123",
        "upcoming": False,
        "success": True
    }
    processed = lambda_function.process_launch(sample_launch)
    assert processed['launch_id'] == "abc123"
    assert processed['mission_name'] == "Test Mission"
    assert processed['launch_date'] == "2025-03-30T00:00:00Z"
    assert processed['rocket'] == "rocket_123"
    assert processed['status'] == "success"

def test_fetch_launches(monkeypatch):
    def mock_get(url, timeout):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return [{
                    "id": "1", 
                    "name": "Mock Mission", 
                    "date_utc": "2025-01-01T00:00:00Z", 
                    "rocket": "r1", 
                    "upcoming": True, 
                    "success": None
                }]
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)
    launches = lambda_function.fetch_launches()
    assert isinstance(launches, list)
    assert launches[0]["id"] == "1"

