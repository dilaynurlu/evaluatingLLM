import requests

def test_should_strip_auth_host_change():
    session = requests.Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # When the hostname changes, the Authorization header must be stripped
    # to prevent leaking credentials to a third party.
    assert session.should_strip_auth(old_url, new_url) is True