import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative():
    """
    Test prepending a scheme to a protocol-relative URL (starting with //).
    This ensures the netloc is correctly identified and scheme is added.
    """
    url = "//example.com"
    new_scheme = "ftp"
    
    # //example.com is parsed as scheme=None, netloc=example.com
    expected = "ftp://example.com"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected