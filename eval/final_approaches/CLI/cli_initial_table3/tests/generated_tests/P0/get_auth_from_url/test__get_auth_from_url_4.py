from requests.utils import get_auth_from_url

def test_get_auth_from_url_4():
    url = "http://example.com"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
