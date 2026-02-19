import requests

def test_should_strip_auth_http_to_https_upgrade_standard():
    """
    Test that Authorization header is NOT stripped when upgrading from HTTP to HTTPS on standard ports.
    Usability allowance: allow upgrading to secure channel on the same host.
    """
    session = requests.Session()
    # Scheme upgrade http -> https, standard ports implied (80 -> 443)
    assert not session.should_strip_auth("http://example.com/foo", "https://example.com/bar")