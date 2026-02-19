import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction and decoding of percent-encoded characters 
    in username and password (e.g., @ and /).
    """
    # Username: "user@domain" -> Encoded: "user%40domain"
    # Password: "pass/word" -> Encoded: "pass%2Fword"
    url = "https://user%40domain:pass%2Fword@example.com/login"
    expected_auth = ("user@domain", "pass/word")
    
    assert get_auth_from_url(url) == expected_auth