import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_characters():
    """
    Test that percent-encoded characters in username and password are decoded.
    """
    # Username: 'user:name' -> 'user%3Aname'
    # Password: 'p@ss#word' -> 'p%40ss%23word'
    url = "https://user%3Aname:p%40ss%23word@example.com/path"
    expected_auth = ("user:name", "p@ss#word")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth