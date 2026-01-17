import requests

def test_should_strip_auth_implicit_vs_explicit_default_port():
    session = requests.Session()
    # http://example.com implies port 80.
    # http://example.com:80 specifies port 80.
    old_url = "http://example.com/resource"
    new_url = "http://example.com:80/resource"
    
    # The logic detects these are effectively the same port for the 'http' scheme.
    # Therefore, auth should NOT be stripped.
    assert session.should_strip_auth(old_url, new_url) is False