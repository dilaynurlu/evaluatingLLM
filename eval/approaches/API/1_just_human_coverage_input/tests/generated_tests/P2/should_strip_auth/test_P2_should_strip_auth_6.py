import requests
import pytest

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com/foo", "http://example.com:80/bar"),
    ("http://example.com:80/foo", "http://example.com/bar"),
    ("https://example.com/foo", "https://example.com:443/bar"),
    ("https://example.com:443/foo", "https://example.com/bar"),
])
def test_should_strip_auth_port_normalization(old_url, new_url):
    s = requests.Session()
    # Scenario: Switching between implicit (None) and explicit (80/443) default ports 
    # for the same scheme is considered the same location, so it should NOT strip Authorization.
    assert s.should_strip_auth(old_url, new_url) is False