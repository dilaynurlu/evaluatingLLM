import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_unicode_handling():
    """
    Test extracting credentials containing unicode characters.
    Ensure that non-ASCII characters are handled correctly if they appear 
    in the URL (usually encoded) or as literals if supported.
    """
    # "café" -> UTF-8 bytes: c3 a6 -> %C3%A6
    # user: café, pass: latte
    url = "http://caf%C3%A6:latte@example.com"
    auth = get_auth_from_url(url)
    
    assert auth == ("café", "latte")