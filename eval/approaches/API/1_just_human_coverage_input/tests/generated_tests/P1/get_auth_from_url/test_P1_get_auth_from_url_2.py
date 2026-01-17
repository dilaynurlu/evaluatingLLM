import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_decodes_percent_encoded_characters():
    """
    Test that URL-encoded characters in the username and password are decoded 
    correctly in the returned tuple.
    """
    # 'user@name' -> 'user%40name'
    # 'pass word' -> 'pass%20word'
    url = "https://user%40name:pass%20word@example.com"
    expected_auth = ("user@name", "pass word")
    
    assert get_auth_from_url(url) == expected_auth