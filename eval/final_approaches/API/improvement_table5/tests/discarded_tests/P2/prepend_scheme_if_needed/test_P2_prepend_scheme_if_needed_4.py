import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_and_no_scheme():
    """
    Test prepending scheme to a URL with authentication info.
    We use the '//' prefix to ensure the parser treats 'user:pass' as authentication
    rather than a scheme (like 'user:').
    
    This exercises the logic where auth is re-attached to the netloc:
        netloc = "@".join([auth, netloc])
    """
    url = "//user:p@ssword@db.internal:5432/data"
    new_scheme = "postgresql"
    
    expected = "postgresql://user:p@ssword@db.internal:5432/data"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected