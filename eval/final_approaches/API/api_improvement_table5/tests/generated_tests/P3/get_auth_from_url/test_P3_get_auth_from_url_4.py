from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username_field():
    """
    Test URL with empty username and valid password.
    Ensures the username is returned as an empty string.
    """
    url = "http://:test_secret_val@example.com"
    result = get_auth_from_url(url)
    assert result == ("", "test_secret_val")