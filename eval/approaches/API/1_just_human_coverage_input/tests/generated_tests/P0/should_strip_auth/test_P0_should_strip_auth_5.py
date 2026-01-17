import requests

def test_should_strip_auth_port_normalization():
    """
    Test that Authorization header is KEPT when the port change is merely due to
    implicit vs explicit default port usage (e.g. http://host -> http://host:80).
    """
    session = requests.Session()
    # Implicit port 80 vs explicit port 80
    old_url = "http://example.com/resource"
    new_url = "http://example.com:80/resource"
    
    # Expect False because both effectively use port 80
    assert session.should_strip_auth(old_url, new_url) is False