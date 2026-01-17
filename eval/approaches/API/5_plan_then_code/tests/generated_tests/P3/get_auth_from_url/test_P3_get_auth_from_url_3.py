from requests.utils import get_auth_from_url

def test_get_auth_from_url_ambiguous_query_params():
    """
    Test that authentication delimiters appearing in the query string do not confuse the parser.
    The function should correctly identify that the authority section has no credentials.
    
    Refines coverage for:
    - Authority Confusion and Ambiguity.
    """
    # The 'user:pass@evil.com' is part of the query string, not the authority
    url = "http://example.com/login?redirect=http://user:pass@evil.com"
    auth = get_auth_from_url(url)
    
    assert auth == ("", "")