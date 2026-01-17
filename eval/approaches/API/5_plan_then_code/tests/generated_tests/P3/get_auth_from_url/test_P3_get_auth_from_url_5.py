from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_username_special_chars():
    """
    Test extraction where the username is empty but password is present and contains
    special reserved characters that are percent-encoded.
    
    Refines coverage for:
    - Handling of Sensitive Characters/Delimiters in password field.
    """
    # Password is "pass#word", where # must be encoded to avoid being treated as fragment
    url = "https://:pass%23word@example.com/resource"
    auth = get_auth_from_url(url)
    
    assert auth == ("", "pass#word")