import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_multibyte_encoded():
    """
    Test extraction and decoding of UTF-8 multibyte characters that are percent-encoded.
    """
    # Username: "useré" (UTF-8 encoded -> %C3%A9)
    # Password: "p€ss" (UTF-8 encoded -> %E2%82%AC)
    url = "http://user%C3%A9:p%E2%82%ACss@example.com/"
    expected_auth = ("useré", "p€ss")
    
    assert get_auth_from_url(url) == expected_auth