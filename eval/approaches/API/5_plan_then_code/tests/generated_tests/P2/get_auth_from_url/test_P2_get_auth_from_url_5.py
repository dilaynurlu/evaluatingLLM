from requests.utils import get_auth_from_url

def test_get_auth_empty_username():
    """
    Test extraction when the username field is empty but the password is provided.
    URL format: http://:password@host
    """
    url = "http://:secret123@example.com"
    expected_auth = ("", "secret123")
    
    assert get_auth_from_url(url) == expected_auth