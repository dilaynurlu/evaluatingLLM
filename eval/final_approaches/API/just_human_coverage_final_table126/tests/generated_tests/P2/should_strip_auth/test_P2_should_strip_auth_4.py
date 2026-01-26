import requests

def test_should_strip_auth_port_change_non_default():
    """
    Test that Authorization header is stripped when changing between different non-standard ports.
    Different ports imply different services/origins.
    """
    session = requests.Session()
    # Port change 8000 -> 8001
    assert session.should_strip_auth("http://example.com:8000/foo", "http://example.com:8001/bar")