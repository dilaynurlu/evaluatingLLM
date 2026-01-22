from requests.utils import get_auth_from_url

def test_get_auth_from_url_4():
    # Malformed URL?
    url = "not_a_url"
    auth = get_auth_from_url(url)
    assert auth == ("", "")
