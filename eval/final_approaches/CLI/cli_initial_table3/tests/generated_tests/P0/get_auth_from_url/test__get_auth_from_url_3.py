from requests.utils import get_auth_from_url

def test_get_auth_from_url_3():
    url = "http://user%40:pass%3A@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@", "pass:")
