import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth():
    """
    Test prepending a scheme to a URL with authentication info.
    This exercises the logic that reconstructs netloc with auth.
    We use // to ensure parsing sees it as an authority, not a scheme.
    """
    url = "//user:pass@db.internal"
    new_scheme = "postgres"
    
    # parse_url extracts auth='user:pass', host='db.internal'.
    # prepend_scheme_if_needed reconstructs 'user:pass@db.internal' before unparsing.
    expected = "postgres://user:pass@db.internal"
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == expected