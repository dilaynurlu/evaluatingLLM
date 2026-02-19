from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal_variants():
    """
    Test that IPv6 literals (bracketed) are correctly handled.
    Covers IPv6 with and without ports to ensure colon handling logic is robust.
    """
    new_scheme = "http"

    # IPv6 with port
    url_with_port = "[::1]:8080"
    assert prepend_scheme_if_needed(url_with_port, new_scheme) == "http://[::1]:8080"

    # IPv6 without port (Critique: Edge Cases / Colon handling)
    url_no_port = "[::1]"
    assert prepend_scheme_if_needed(url_no_port, new_scheme) == "http://[::1]"