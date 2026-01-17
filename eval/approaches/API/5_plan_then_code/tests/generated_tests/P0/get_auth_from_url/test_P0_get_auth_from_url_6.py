from requests.utils import get_auth_from_url

def test_get_auth_from_url_invalid_input_type():
    """
    Test that providing non-string input (which causes internal attribute errors)
    is handled gracefully and returns empty strings.
    """
    # Passing None triggers AttributeError in urlparse (or TypeError), 
    # which get_auth_from_url catches.
    auth = get_auth_from_url(None)
    
    assert auth == ("", "")