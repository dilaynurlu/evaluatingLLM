import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction and decoding of percent-encoded username and password.
    Verifies that unquote is correctly applied to the components.
    """
    # 'user@domain' encoded as 'user%40domain'
    # 'pass/word' encoded as 'pass%2Fword'
    url = "https://user%40domain:pass%2Fword@example.com/api"
    expected_auth = ("user@domain", "pass/word")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth