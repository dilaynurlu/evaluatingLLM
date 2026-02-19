from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username():
    """
    Test extraction when username is empty (starts with colon).
    """
    url = "https://:secret@example.com"
    expected_auth = ("", "secret")
    
    assert get_auth_from_url(url) == expected_auth