from requests.utils import get_auth_from_url

def test_get_auth_unicode_encoded():
    """
    Test extraction of non-ASCII characters that are percent-encoded in the URL.
    Input user: 'ñam' (%C3%B1am)
    Input pass: '123€' (123%E2%82%AC)
    """
    url = "http://%C3%B1am:123%E2%82%AC@example.com"
    expected_auth = ("ñam", "123€")
    
    assert get_auth_from_url(url) == expected_auth