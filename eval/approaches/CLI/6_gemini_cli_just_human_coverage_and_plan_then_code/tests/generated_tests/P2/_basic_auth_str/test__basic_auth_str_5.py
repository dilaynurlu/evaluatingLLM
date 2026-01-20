import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_creds():
    # Scenario: Empty username and password
    # : -> Og==
    result = _basic_auth_str("", "")
    assert result == "Basic Og=="
