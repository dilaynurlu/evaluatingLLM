import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test that percent-encoded characters in the username and password 
    are correctly unquoted/decoded by the function.
    """
    # Username: user@domain -> user%40domain
    # Password: pass#word -> pass%23word
    url = "https://user%40domain:pass%23word@example.com/api"
    expected_auth = ("user@domain", "pass#word")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth