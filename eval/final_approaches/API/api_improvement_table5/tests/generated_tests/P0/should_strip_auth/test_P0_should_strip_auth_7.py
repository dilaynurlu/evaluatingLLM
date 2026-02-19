import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_non_standard_ports():
    """
    Test that authentication is stripped when redirecting from HTTP to HTTPS
    if non-standard ports are used.
    """
    session = Session()
    # http:8080 -> https:8443
    old_url = "http://example.com:8080/start"
    new_url = "https://example.com:8443/end"
    
    # The exemption for http->https only applies to ports (80, None) and (443, None).
    assert session.should_strip_auth(old_url, new_url) is True