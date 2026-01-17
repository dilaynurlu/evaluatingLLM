import requests

def test_should_strip_auth_downgrade_https_to_http():
    s = requests.Session()
    # Scenario: Downgrading from HTTPS to HTTP on the same host should strip Authorization.
    # This prevents sending credentials over an unencrypted connection (security hygiene).
    assert s.should_strip_auth("https://example.com/foo", "http://example.com/bar") is True