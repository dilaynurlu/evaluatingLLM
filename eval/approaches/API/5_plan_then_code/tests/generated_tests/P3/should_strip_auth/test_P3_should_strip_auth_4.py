import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com:8080/resource", "http://example.com:9090/resource"),
    ("https://example.com:8443/resource", "https://example.com:9443/resource"),
    ("http://[::1]:8080/resource", "http://[::1]:9090/resource"),
])
def test_should_strip_auth_port_changes(old_url, new_url):
    """
    Test that authentication headers are stripped when the port changes to a 
    non-standard port, indicating a different service.
    """
    session = Session()
    # Changing ports (when not normalizing default 80/443) means a different origin.
    assert session.should_strip_auth(old_url, new_url) is True