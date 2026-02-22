from requests.utils import get_auth_from_url

def test_get_auth_from_url_normal():
    url = "http://user:password@example.com/foo"
    auth = get_auth_from_url(url)
    assert auth == ("user", "password")
