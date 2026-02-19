import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test extracting auth from a URL with no credentials.
    Should return a tuple of empty strings ('', '').
    
    This exercises the exception handling block where attribute access 
    or unquote(None) raises an exception.
    """
    url = "http://example.com/some/path"
    auth = get_auth_from_url(url)
    
    assert auth == ("", "")