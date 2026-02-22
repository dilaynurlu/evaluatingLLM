from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_chars():
    """
    Test extraction of user and password containing encoded characters.
    """
    # user%40domain:pass%23word
    url = "http://user%40domain:pass%23word@example.com/foo"
    auth = get_auth_from_url(url)
    
    assert auth == ("user@domain", "pass#word")
