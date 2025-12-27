import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extracting percent-encoded username and password. 
    Special characters should be correctly unquoted.
    """
    # Username: user@name -> user%40name
    # Password: p@ss/word -> p%40ss%2Fword
    url = "https://user%40name:p%40ss%2Fword@example.com/path"
    expected_auth = ("user@name", "p@ss/word")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth