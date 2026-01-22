import pytest
from requests.utils import get_auth_from_url

def test_get_auth_percent_encoded_credentials():
    """
    Test that percent-encoded characters in username and password are
    correctly decoded, specifically focusing on reserved characters.
    
    Refinements based on critique:
    - Includes encoded reserved characters like '@', ':', and '/' to 
      ensure the parser handles delimiters inside credentials correctly.
    """
    # Username: user@domain (user%40domain)
    # Password: pass:word/safe (pass%3Aword%2Fsafe)
    url = "https://user%40domain:pass%3Aword%2Fsafe@example.com"
    expected_auth = ("user@domain", "pass:word/safe")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth