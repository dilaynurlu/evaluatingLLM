from requests.utils import get_auth_from_url

def test_get_auth_special_chars():
    # characters that don't need encoding but are unusual
    url = "http://u$er:p&ss@example.com"
    assert get_auth_from_url(url) == ("u$er", "p&ss")
