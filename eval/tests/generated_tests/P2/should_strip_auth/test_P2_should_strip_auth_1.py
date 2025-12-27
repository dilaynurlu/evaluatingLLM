import requests

def test_should_strip_auth_on_hostname_mismatch():
    """
    Test that Authorization headers are stripped when the hostname changes
    between the old URL and the new URL.
    """
    session = requests.Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # When hostnames differ, the function should return True (strip auth)
    assert session.should_strip_auth(old_url, new_url) is True