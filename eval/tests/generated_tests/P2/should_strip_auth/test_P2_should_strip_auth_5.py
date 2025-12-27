import requests

def test_should_strip_auth_on_port_change_same_scheme():
    """
    Test that Authorization headers are stripped when the port changes
    while the scheme and hostname remain the same.
    """
    session = requests.Session()
    old_url = "http://example.com:8000/data"
    new_url = "http://example.com:9000/data"
    
    # Same scheme, same host, but different ports -> strip auth.
    assert session.should_strip_auth(old_url, new_url) is True