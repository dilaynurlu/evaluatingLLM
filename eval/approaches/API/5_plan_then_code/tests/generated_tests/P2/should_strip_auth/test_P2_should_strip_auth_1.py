import requests

def test_should_strip_auth_host_mismatch():
    """
    Test that Authorization headers are stripped when the hostname changes.
    """
    session = requests.Session()
    
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Logic: hostname differs -> strip auth
    assert session.should_strip_auth(old_url, new_url) is True