import requests

def test_should_strip_auth_same_scheme_different_ports():
    session = requests.Session()
    old_url = "http://example.com:8000/resource"
    new_url = "http://example.com:8001/resource"
    
    # Changing ports on the same host/scheme should strip auth 
    # unless they map to the same default port (which these do not).
    assert session.should_strip_auth(old_url, new_url) is True