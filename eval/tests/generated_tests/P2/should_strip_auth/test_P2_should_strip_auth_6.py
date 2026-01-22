import requests

def test_should_strip_auth_http_to_https_upgrade_nonstandard_destination():
    """
    Test that Authorization header is stripped when upgrading to HTTPS on a non-standard port.
    The special exemption for http->https upgrades only applies to standard ports (80/443).
    """
    session = requests.Session()
    # Target port is 8443, which is not the standard 443, so strip auth.
    assert session.should_strip_auth("http://example.com/foo", "https://example.com:8443/bar")