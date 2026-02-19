from requests.sessions import Session

def test_should_strip_auth_different_ports():
    """
    Test that authentication is stripped when redirecting to a different port
    on the same host.
    Refined to includes IPv6 literals to ensure parsing robustness.
    """
    session = Session()
    
    # IPv4 explicit port change
    assert session.should_strip_auth("http://127.0.0.1:8000/a", "http://127.0.0.1:8001/b") is True
    
    # IPv6 explicit port change (ensures bracket parsing works)
    old_ipv6 = "http://[::1]:8080/api"
    new_ipv6 = "http://[::1]:9090/api"
    assert session.should_strip_auth(old_ipv6, new_ipv6) is True