import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_ipv6_literal():
    """
    Test prepending scheme to a URL containing an IPv6 literal.
    """
    # Using protocol relative // to ensure parser sees it as netloc immediately
    url = "//[::1]:8080"
    new_scheme = "http"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "http://[::1]:8080"