from requests.utils import get_auth_from_url

def test_get_auth_encoded():
    url = "http://%40user:%40pass@example.com"
    # %40 is @
    assert get_auth_from_url(url) == ("@user", "@pass")
