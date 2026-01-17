import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid_input_type():
    """
    Test behavior with invalid input types (e.g., None, integer).
    Ensures the function handles exceptions (AttributeError/TypeError) gracefully
    and returns empty credentials instead of crashing.
    """
    inputs = [None, 123, object()]
    expected_auth = ("", "")
    
    for inp in inputs:
        assert get_auth_from_url(inp) == expected_auth