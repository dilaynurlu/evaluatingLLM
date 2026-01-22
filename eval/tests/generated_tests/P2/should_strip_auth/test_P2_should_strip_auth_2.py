import requests

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization header is stripped when downgrading from HTTPS to HTTP on the same host.
    Security requirement: do not send credentials over plaintext if they were on secure channel.
    """
    session = requests.Session()
    # Scheme change from https to http
    assert session.should_strip_auth("https://example.com/foo", "http://example.com/bar")