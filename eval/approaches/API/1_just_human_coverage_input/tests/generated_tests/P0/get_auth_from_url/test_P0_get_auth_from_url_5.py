import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test behavior when the URL contains no authentication information.
    """
    url = "http://example.com/index.html"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth