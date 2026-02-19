import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_host_with_query_no_path():
    """
    Test prepending scheme to 'host?query'.
    The parser likely sees 'host' as a path and 'query' as a query.
    The function should swap path->netloc, handle the empty path, and preserve the query.
    """
    url = "example.com?search=test"
    new_scheme = "https"
    
    expected = "https://example.com?search=test"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected