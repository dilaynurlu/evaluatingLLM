import requests

def test_should_strip_auth_upgrade_http_to_https_allowed():
    s = requests.Session()
    # Scenario: Upgrading from HTTP to HTTPS on standard ports is a special exception 
    # in requests to preserve backwards compatibility, so it should NOT strip Authorization.
    assert s.should_strip_auth("http://example.com/foo", "https://example.com/bar") is False