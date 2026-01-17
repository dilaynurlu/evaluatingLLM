from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username():
    """
    Test extraction when username is an empty string (indicated by a leading colon).
    """
    url = "https://:secret_token@api.example.com"
    expected_auth = ("", "secret_token")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth