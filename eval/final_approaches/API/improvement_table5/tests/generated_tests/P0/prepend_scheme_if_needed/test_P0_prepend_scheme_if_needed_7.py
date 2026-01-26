import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_query_no_path():
    """
    Test a URL that has a host and query but no path component.
    This exercises the logic ensuring 'path' is treated correctly (converted from None to empty string)
    during URL reconstruction.
    """
    url = "example.com?a=b"
    new_scheme = "https"
    
    # parse_url("example.com?a=b") -> host="example.com", path=None, query="a=b"
    # Function sets path="" if it is None.
    # urlunparse handles empty path by omitting the slash after netloc if not required?
    # Actually standard urlunparse with empty path often produces "scheme://netloc?query"
    expected = "https://example.com?a=b"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected