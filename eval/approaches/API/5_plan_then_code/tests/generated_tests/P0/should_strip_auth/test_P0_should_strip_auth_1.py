import pytest
from requests import Session

def test_should_strip_auth_different_hostname():
    """
    Test that Authorization headers are stripped when redirecting to a different hostname.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Expect True because hostnames differ
    assert session.should_strip_auth(old_url, new_url) is True