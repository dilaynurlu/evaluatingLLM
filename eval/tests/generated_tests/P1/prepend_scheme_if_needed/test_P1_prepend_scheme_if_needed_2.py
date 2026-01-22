from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_preserves_existing_scheme():
    """
    Test that if the URL already has a scheme, it is NOT replaced,
    even if it differs from the new_scheme argument.
    """
    url = "ftp://example.com/resource"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Expect the original scheme 'ftp' to be preserved.
    assert result == "ftp://example.com/resource"