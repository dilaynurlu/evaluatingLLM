import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_returns_empty_tuple_for_url_without_auth():
    """
    Test that a URL with no authentication components returns a tuple of empty strings.
    """
    url = "http://example.com/api/v1"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth