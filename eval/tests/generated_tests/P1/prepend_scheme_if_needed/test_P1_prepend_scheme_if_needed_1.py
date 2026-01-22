from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_simple_host():
    """
    Test that a scheme is prepended to a simple hostname that lacks one.
    The function should recognize the missing scheme and apply the new one.
    """
    url = "example.com"
    new_scheme = "http"
    
    # parse_url internally prepends // for this input, parsing 'example.com' as host.
    # The function sees no scheme, sets it to 'http', and reconstructs the URL.
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://example.com"