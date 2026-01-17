import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL without any authentication components returns
    an empty tuple ("","").
    """
    url = "http://example.com/"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth