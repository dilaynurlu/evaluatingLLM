from requests.utils import get_auth_from_url

def test_get_auth_normal():
    url = "http://user:pass@example.com"
    assert get_auth_from_url(url) == ("user", "pass")
