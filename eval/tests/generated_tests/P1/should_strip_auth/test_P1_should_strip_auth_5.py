import pytest
from requests.sessions import Session

def test_should_strip_auth_handles_explicit_and_implicit_default_ports():
    """
    Test that Authorization headers are PRESERVED when the port 'changes'
    semantically only between explicit default port and implicit default port.
    e.g. http://host:80 -> http://host
    """
    session = Session()
    # explicit port 80 vs implicit port (None) for http
    old_url = "http://example.com:80/api"
    new_url = "http://example.com/api"
    
    # Logic:
    # Hostname match.
    # changed_scheme is False.
    # old port (80) in default_port (80, None).
    # new port (None) in default_port (80, None).
    # Returns False.
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is False, "Auth should be preserved when normalizing default ports"