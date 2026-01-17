import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_to_protocol_relative_url():
    """
    Test that a protocol-relative URL (starting with //) gets the scheme prepended.
    This format explicitly defines a netloc without a scheme.
    """
    url = "//example.com/path"
    new_scheme = "https"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "https://example.com/path"