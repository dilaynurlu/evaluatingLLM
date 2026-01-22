from requests.utils import get_auth_from_url

def test_get_auth_from_url_2():
    url = "http://user@example.com"
    auth = get_auth_from_url(url)
    # requests implementation returns empty auth if unquoting fails (e.g. password is None)
    assert auth == ("", "")
