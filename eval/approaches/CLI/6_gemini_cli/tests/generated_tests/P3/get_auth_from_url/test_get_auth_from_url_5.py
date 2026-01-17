from requests.utils import get_auth_from_url

def test_get_auth_empty_creds():
    url = "http://:@example.com"
    assert get_auth_from_url(url) == ("", "")
