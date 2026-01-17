import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_user_only_fallback():
    """
    Test the specific fallback behavior when a URL has a username but NO password component
    (no colon). In this case, urlparse sets password to None, which causes unquote(None)
    to raise a TypeError. The function catches this and returns ("", "").
    """
    url = "http://user@example.com/"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth