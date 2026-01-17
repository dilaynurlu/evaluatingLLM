import requests

def test_should_strip_auth_upgrade_http_to_https_non_standard_port():
    s = requests.Session()
    # Scenario: Upgrading from HTTP to HTTPS where the source uses a non-standard port 
    # does NOT match the compatibility exception, so it should strip Authorization.
    # Source port 8080 is not in the allowed list (80, None).
    assert s.should_strip_auth("http://example.com:8080/foo", "https://example.com/bar") is True