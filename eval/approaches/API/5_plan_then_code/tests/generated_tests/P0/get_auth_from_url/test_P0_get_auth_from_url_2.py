from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction and unquoting of percent-encoded username and password.
    """
    # Username: 'user@name' -> 'user%40name'
    # Password: 'pass word' -> 'pass%20word'
    url = "http://user%40name:pass%20word@example.com/api"
    expected_auth = ("user@name", "pass word")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth