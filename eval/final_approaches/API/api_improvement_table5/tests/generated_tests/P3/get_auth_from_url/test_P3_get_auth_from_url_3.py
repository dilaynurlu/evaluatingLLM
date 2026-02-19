from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_field():
    """
    Test URL with username and delimiter ':' but empty password.
    Ensures that an empty password provided in the URL remains an empty string
    and does not trigger exception handling.
    """
    url = "http://test_usr:@example.com"
    result = get_auth_from_url(url)
    assert result == ("test_usr", "")