from requests.utils import get_auth_from_url

def test_get_auth_from_url_6():
    # Due to implementation using unquote on potential None password, 
    # this returns empty strings instead of ('user', '')
    url = "http://user@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
