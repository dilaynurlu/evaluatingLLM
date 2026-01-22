from requests.utils import get_auth_from_url

def test_get_auth_from_url_encoded_credentials():
    """
    Test extraction of percent-encoded characters in username and password.
    Should be unquoted in the result.
    """
    # Username: user@domain -> user%40domain
    # Password: p@ssword -> p%40ssword
    url = "https://user%40domain:p%40ssword@example.com/index"
    expected_auth = ("user@domain", "p@ssword")
    
    assert get_auth_from_url(url) == expected_auth