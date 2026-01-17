import requests

def test_should_strip_auth_http_to_https_standard_ports():
    session = requests.Session()
    # Standard upgrade from HTTP to HTTPS on default ports
    old_url = "http://example.com/resource"
    new_url = "https://example.com/resource"
    
    # This is a special exception in requests to allow upgrading to HTTPS
    # without stripping auth, provided ports are standard (80/None -> 443/None).
    assert session.should_strip_auth(old_url, new_url) is False