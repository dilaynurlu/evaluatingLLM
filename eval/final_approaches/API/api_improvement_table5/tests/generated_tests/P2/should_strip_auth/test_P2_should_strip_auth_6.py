import pytest
from requests.sessions import Session

def test_should_strip_auth_same_url_path_change():
    """
    Test that Authorization header is KEPT when only the path/query changes
    on the same host, scheme, and port.
    Matches final return where changed_port and changed_scheme are False.
    """
    session = Session()
    old_url = "http://example.com/page1?q=a"
    new_url = "http://example.com/page2?q=b"
    
    # No scheme/host/port change -> should NOT strip auth
    assert session.should_strip_auth(old_url, new_url) is False