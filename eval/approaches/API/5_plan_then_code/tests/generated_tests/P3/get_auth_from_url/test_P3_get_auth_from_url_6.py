from requests.utils import get_auth_from_url

def test_get_auth_from_url_partial_auth_fails_safely():
    """
    Test that a URL with a username but no password delimiter (no colon) results in no auth extraction.
    This verifies the 'Fail Closed' behavior where partial ambiguity prevents credential extraction.
    
    Mechanism: urlparse returns username='user', password=None. 
    unquote(None) raises TypeError, which is caught by the function, returning ("", "").
    """
    url = "http://user@example.com/resource"
    auth = get_auth_from_url(url)
    
    assert auth == ("", "")