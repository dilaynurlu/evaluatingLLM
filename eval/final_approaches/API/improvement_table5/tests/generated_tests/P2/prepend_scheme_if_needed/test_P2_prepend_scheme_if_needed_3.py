import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative():
    """
    Test prepending scheme to a protocol-relative URL (starting with //).
    In this case, the parser correctly identifies the netloc, so no path swapping occurs,
    but the scheme is None, so the new scheme should be prepended.
    """
    url = "//cdn.example.com/lib.js"
    new_scheme = "https"
    
    expected = "https://cdn.example.com/lib.js"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected