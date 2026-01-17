from requests.utils import get_auth_from_url

def test_get_auth_not_a_url():
    url = ""
    assert get_auth_from_url(url) == ("", "")
