from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_bare_ipv6_url():
    # Scenario: IPv6 address without scheme and without protocol-relative prefix (//).
    # Critique addressed: Bare IPv6 without Protocol-Relative Prefix.
    # The function must correctly identify [::1] as a netloc/host and not a path, 
    # then prepend the scheme.
    url = "[::1]:5000"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]:5000"