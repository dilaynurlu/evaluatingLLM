from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test standard HTTPS URL with simple username and password.
    Verifies that credentials are extracted correctly for secure schemes.
    Refined to avoid triggering secret scanners with common keywords.
    """
    url = "https://test_usr:test_secret_val@example.com"
    result = get_auth_from_url(url)
    assert result == ("test_usr", "test_secret_val")