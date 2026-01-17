from requests.utils import get_auth_from_url

def test_get_auth_encoded_credentials():
    """
    Test extraction when username and password contain percent-encoded characters.
    Input: user encoded as 'user%40mail', password encoded as 'pass%3Aword'
    Expected: decoded 'user@mail' and 'pass:word'
    """
    url = "https://user%40mail:pass%3Aword@example.com/resource"
    expected_auth = ("user@mail", "pass:word")
    
    assert get_auth_from_url(url) == expected_auth