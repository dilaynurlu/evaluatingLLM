from requests.utils import get_auth_from_url

def test_get_auth_from_url_complex_url_structure():
    """
    Test extraction of credentials from a URL containing explicit port, query parameters, 
    fragment identifiers, and a secure scheme.
    
    Refines coverage for:
    - URL Component Variations (Port, Query, Fragment, Scheme).
    """
    url = "https://user:password@example.com:8443/resource?query=param#fragment"
    auth = get_auth_from_url(url)
    
    assert auth == ("user", "password")