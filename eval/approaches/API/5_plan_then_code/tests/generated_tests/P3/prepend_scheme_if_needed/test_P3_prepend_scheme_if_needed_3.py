import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_no_scheme():
    """
    Test prepending a scheme to protocol-relative URLs (starting with //).
    Refined to include:
    1. Protocol-relative with Authentication.
    2. Protocol-relative without Authentication.
    """
    new_scheme = "postgresql"

    # Case 1: With Auth
    url_auth = "//user:pass@db.local"
    expected_auth = "postgresql://user:pass@db.local"
    assert prepend_scheme_if_needed(url_auth, new_scheme) == expected_auth

    # Case 2: Without Auth (common XSS vector if handled poorly)
    url_clean = "//example.com"
    expected_clean = "postgresql://example.com"
    assert prepend_scheme_if_needed(url_clean, new_scheme) == expected_clean