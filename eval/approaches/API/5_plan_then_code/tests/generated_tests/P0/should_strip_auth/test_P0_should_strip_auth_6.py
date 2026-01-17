import pytest
from requests import Session

def test_should_strip_auth_http_to_https_non_standard_ports():
    """
    Test that Authorization headers are stripped when upgrading from HTTP to HTTPS
    if non-standard ports are involved, as the special exemption only applies to standard ports.
    """
    session = Session()
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com:8443/foo"
    
    # Expect True because ports are non-standard, so the special http->https logic doesn't apply,
    # and scheme/port have changed.
    assert session.should_strip_auth(old_url, new_url) is True