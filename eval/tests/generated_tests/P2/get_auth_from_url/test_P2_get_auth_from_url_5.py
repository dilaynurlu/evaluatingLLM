import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL with no authentication information returns 
    a tuple of empty strings.
    """
    url = "http://example.com/public/resource"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth