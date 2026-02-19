import pytest
from requests.sessions import Session

def test_should_strip_auth_default_port_normalization():
    """
    Test that Authorization header is KEPT when the only difference is 
    explicit vs implicit default port (e.g., http:80 vs http).
    Matches branch: not changed_scheme and ports in default_port.
    """
    session = Session()
    # Explicit port 80 vs Implicit port None (which implies 80 for http)
    old_url = "http://example.com:80/resource"
    new_url = "http://example.com/resource"
    
    # Semantic equivalence of ports -> should NOT strip auth
    assert session.should_strip_auth(old_url, new_url) is False