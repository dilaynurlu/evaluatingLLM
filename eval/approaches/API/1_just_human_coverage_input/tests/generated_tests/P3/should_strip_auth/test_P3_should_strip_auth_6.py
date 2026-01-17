import requests
from requests.sessions import Session

def test_should_strip_auth_http_to_https_non_standard_port():
    """
    Test that Authorization header is stripped when upgrading to HTTPS but on a 
    port that does not match the standard HTTPS default (443), or when the 
    upgrade target uses the 'wrong' default port (e.g. https on 80).
    """
    session = Session()
    
    # http (80) -> https (8443)
    # Not the standard secure port exemption.
    assert session.should_strip_auth("http://example.com/foo", "https://example.com:8443/foo") is True
    
    # http (80) -> https (80)
    # Scheme upgrade, but port 80 is not the standard port for HTTPS.
    # The standard exemption logic requires moving from default HTTP to default HTTPS.
    assert session.should_strip_auth("http://example.com/foo", "https://example.com:80/foo") is True