import requests

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization header is stripped when downgrading from HTTPS to HTTP,
    even on standard ports. This is a security requirement.
    """
    session = requests.Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Expect True because downgrading scheme is insecure
    assert session.should_strip_auth(old_url, new_url) is True