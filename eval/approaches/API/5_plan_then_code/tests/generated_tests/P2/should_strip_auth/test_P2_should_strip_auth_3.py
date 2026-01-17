import requests

def test_should_strip_auth_https_http_downgrade():
    """
    Test that Authorization headers are stripped when downgrading from HTTPS to HTTP.
    This does NOT fall under the special compatibility exception.
    """
    session = requests.Session()
    
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Logic: Scheme changed, and it's not the allowed http->https upgrade.
    # Therefore, it should return True (strip auth).
    assert session.should_strip_auth(old_url, new_url) is True