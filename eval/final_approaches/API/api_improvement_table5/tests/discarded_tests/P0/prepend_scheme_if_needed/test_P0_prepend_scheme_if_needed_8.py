import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_auth_no_host():
    """
    Test an edge case where auth is provided but the host part is empty.
    This exercises the 'if not netloc' swap combined with 'if auth' logic.
    """
    url = "//user:pass@"
    new_scheme = "http"
    
    # parsed: auth="user:pass", host=""
    # netloc (from parsed) is usually ""
    # 'if not netloc' triggers swap: netloc gets path (likely ""), path gets ""
    # 'if auth' appends auth to netloc: netloc = "user:pass@" + ""
    expected = "http://user:pass@"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected