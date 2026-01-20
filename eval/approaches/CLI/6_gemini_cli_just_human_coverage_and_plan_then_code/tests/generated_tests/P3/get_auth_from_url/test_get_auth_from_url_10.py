from requests.utils import get_auth_from_url

def test_get_auth_ipv6():
    url = "http://user:pass@[::1]"
    assert get_auth_from_url(url) == ("user", "pass")
