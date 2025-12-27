import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_returns_empty_tuple_when_no_auth_present():
    """
    Test that get_auth_from_url returns a tuple of empty strings when the URL
    contains no authentication components.
    
    Refinements:
    - Uses HTTPS.
    - explicitly checks for the safe default return value ("","").
    """
    url = "https://example.com/index.html"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth