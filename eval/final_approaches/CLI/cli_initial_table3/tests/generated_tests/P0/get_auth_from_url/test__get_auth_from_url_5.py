from requests.utils import get_auth_from_url

def test_get_auth_from_url_5():
    auth = get_auth_from_url(None)
    assert auth == ("", "")
