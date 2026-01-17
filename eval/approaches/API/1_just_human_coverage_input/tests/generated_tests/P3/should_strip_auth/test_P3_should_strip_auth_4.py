import requests
from requests.sessions import Session

def test_should_strip_auth_different_ports_non_default():
    """
    Test that Authorization header is stripped when the port changes to a non-default port,
    covering both explicit-to-explicit and explicit-to-implicit mismatches.
    """
    session = Session()
    
    # Explicit -> Explicit (Different non-standard ports)
    assert session.should_strip_auth("http://example.com:8080/r", "http://example.com:9090/r") is True
    
    # Explicit (non-standard) -> Implicit (standard 80)
    # 8080 != 80, so auth should be stripped.
    assert session.should_strip_auth("http://example.com:8080/r", "http://example.com/r") is True