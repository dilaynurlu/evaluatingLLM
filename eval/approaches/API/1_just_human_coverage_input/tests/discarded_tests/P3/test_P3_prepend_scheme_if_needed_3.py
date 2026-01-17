from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_unicode_host():
    # Scenario: URL contains Unicode (IDNA) characters in the hostname.
    # Critique addressed: IDNA / Unicode Domains.
    # The function should preserve unicode characters while prepending the scheme.
    url = "münchen.de/api"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://münchen.de/api"