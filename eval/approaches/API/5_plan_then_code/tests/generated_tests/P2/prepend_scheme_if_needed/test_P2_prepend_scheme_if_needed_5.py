from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_host():
    """
    Test prepending a scheme to a URL containing an IPv6 literal in the host.
    """
    url = "[::1]:8080"
    new_scheme = "http"
    expected = "http://[::1]:8080"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected