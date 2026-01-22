import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_ipv6_authority():
    # Scenario: Input is an IPv6 address (enclosed in brackets).
    # We use '//' to ensure the parser treats it strictly as a netloc/authority.
    url = "//[2001:db8::1]:8080"
    new_scheme = "http"
    
    # Execution
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Verification
    # The IPv6 address and port should remain intact, with scheme prepended.
    assert result == "http://[2001:db8::1]:8080"