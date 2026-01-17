import requests

def test_should_strip_auth_different_hostname():
    s = requests.Session()
    # Scenario: Redirecting to a completely different host should strip Authorization.
    # This ensures credentials are not leaked to third-party domains.
    assert s.should_strip_auth("http://example.com/foo", "http://other.com/bar") is True