import requests

def test_should_strip_auth_same_scheme_port_change():
    s = requests.Session()
    # Scenario: Changing the port on the same scheme (when not using default ports) 
    # implies a different service, so it should strip Authorization.
    assert s.should_strip_auth("http://example.com:8080/foo", "http://example.com:8081/bar") is True