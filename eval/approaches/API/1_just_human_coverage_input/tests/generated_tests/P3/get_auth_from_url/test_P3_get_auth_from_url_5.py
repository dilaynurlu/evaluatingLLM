import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_username_only_no_colon():
    """
    Test behavior when username is provided without a password or colon separator.
    e.g., 'http://user@example.com/'
    
    Standard requests behavior relies on urllib.parse.urlparse.
    If no colon is present in userinfo, the password attribute is None.
    Attempting to unquote None raises a TypeError, which get_auth_from_url 
    catches, resulting in a return value of ("", "").
    """
    url = "http://user@example.com/"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth