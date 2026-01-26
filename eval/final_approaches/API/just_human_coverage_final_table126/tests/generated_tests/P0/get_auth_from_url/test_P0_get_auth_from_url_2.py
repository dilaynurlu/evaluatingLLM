import pytest
from requests.utils import get_auth_from_url

def test_get_auth_percent_encoded_credentials():
    """
    Test extracting username and password containing special characters
    that are percent-encoded in the URL.
    """
    # Username: "user@domain.com", Password: "pass word"
    # Encoded: user%40domain.com : pass%20word
    url = "https://user%40domain.com:pass%20word@example.com/api"
    expected_auth = ("user@domain.com", "pass word")
    
    assert get_auth_from_url(url) == expected_auth