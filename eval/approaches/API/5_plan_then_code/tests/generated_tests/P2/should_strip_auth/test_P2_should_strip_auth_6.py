import requests

def test_should_strip_auth_http_https_upgrade_non_standard():
    """
    Test that Authorization headers are stripped when upgrading from HTTP to HTTPS 
    if non-standard ports are involved. This ensures the special exception case
    strictly adheres to standard ports.
    """
    session = requests.Session()
    
    # Case 1: Old port is non-standard
    old_url_1 = "http://example.com:8080/foo"
    new_url_1 = "https://example.com/bar"
    assert session.should_strip_auth(old_url_1, new_url_1) is True
    
    # Case 2: New port is non-standard
    old_url_2 = "http://example.com/foo"
    new_url_2 = "https://example.com:8443/bar"
    assert session.should_strip_auth(old_url_2, new_url_2) is True