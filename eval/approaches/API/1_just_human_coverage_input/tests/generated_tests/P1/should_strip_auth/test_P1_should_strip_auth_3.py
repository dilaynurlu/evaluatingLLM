import requests

def test_should_strip_auth_https_to_http_downgrade():
    session = requests.Session()
    old_url = "https://example.com/resource"
    new_url = "http://example.com/resource"
    
    # Downgrading from HTTPS to HTTP is insecure, so Authorization headers
    # should be stripped.
    assert session.should_strip_auth(old_url, new_url) is True