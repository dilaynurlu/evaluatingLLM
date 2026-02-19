from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal():
    """
    Test prepending a scheme to an IPv6 literal address.
    The function should handle the bracketed host correctly.
    """
    url = "[::1]:8080"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]:8080"