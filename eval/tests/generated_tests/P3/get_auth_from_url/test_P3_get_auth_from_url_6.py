import pytest
from requests.utils import get_auth_from_url

def test_get_auth_unicode_chars():
    """
    Test that URLs with unicode characters in the authentication section
    are handled and decoded correctly.
    """
    # URL encoded 'ñ' is '%C3%B1'
    # http://uñ:pñ@example.com
    url = "http://u%C3%B1:p%C3%B1@example.com"
    expected_auth = ("uñ", "pñ")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth