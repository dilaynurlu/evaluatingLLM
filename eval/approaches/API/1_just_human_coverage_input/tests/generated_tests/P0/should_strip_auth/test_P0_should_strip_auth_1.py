import requests

def test_should_strip_auth_cross_host():
    """
    Test that Authorization header is stripped when redirecting to a different hostname.
    """
    session = requests.Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Expect True because the hostname has changed
    assert session.should_strip_auth(old_url, new_url) is True