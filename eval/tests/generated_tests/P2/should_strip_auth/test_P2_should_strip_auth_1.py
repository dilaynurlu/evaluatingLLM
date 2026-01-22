import requests

def test_should_strip_auth_host_mismatch():
    """
    Test that Authorization header is stripped when redirecting to a different hostname.
    Security requirement: do not leak credentials to a different origin.
    """
    session = requests.Session()
    # Host change from example.com to other.com
    assert session.should_strip_auth("http://example.com/foo", "http://other.com/bar")