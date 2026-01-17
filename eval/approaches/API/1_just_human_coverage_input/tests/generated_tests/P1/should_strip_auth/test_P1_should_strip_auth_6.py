import requests

def test_should_strip_auth_http_to_https_non_standard_old_port():
    session = requests.Session()
    # Upgrade to HTTPS, but the original HTTP port was non-standard (8080).
    old_url = "http://example.com:8080/resource"
    new_url = "https://example.com/resource"
    
    # The special exception for http->https upgrade only applies if the old port
    # was 80 or None. Here it is 8080, so auth MUST be stripped.
    assert session.should_strip_auth(old_url, new_url) is True