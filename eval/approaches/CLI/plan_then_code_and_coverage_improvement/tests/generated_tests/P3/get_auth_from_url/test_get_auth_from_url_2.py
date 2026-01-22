from requests.utils import get_auth_from_url

def test_get_auth_from_url_2():
    # Encoded auth
    # user%40domain:p%40ss -> user@domain : p@ss
    url = "http://user%40domain:p%40ss@example.com"
    auth = get_auth_from_url(url)
    assert auth == ("user@domain", "p@ss")