import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_reconstructs_auth_regression():
    """
    Regression test: correctly reconstructs URL including authentication info
    when the scheme is already present.
    Verifies that complex auth strings don't cause double-scheme issues.
    """
    # Complex auth chars to ensure robustness
    url = "ftp://user:p@ss#word@fileserver.local"
    new_scheme = "http"
    
    # Scheme is present, so it should be ignored, but auth must remain intact
    expected = "ftp://user:p@ss#word@fileserver.local"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected