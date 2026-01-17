import requests

def test_should_strip_auth_same_url():
    session = requests.Session()
    old_url = "http://example.com/resource"
    new_url = "http://example.com/resource"
    
    # Redirecting to the exact same URL (or equivalent) should not strip auth.
    assert session.should_strip_auth(old_url, new_url) is False