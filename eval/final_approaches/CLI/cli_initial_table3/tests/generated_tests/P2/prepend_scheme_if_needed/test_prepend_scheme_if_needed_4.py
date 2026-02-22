from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_no_scheme():
    """
    Test prepending scheme when auth is present but no scheme.
    """
    url = "//user:pass@example.com/foo"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    assert result == "https://user:pass@example.com/foo"
