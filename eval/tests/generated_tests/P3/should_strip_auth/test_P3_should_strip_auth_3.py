from requests.sessions import Session

def test_should_strip_auth_localhost_vs_ip_alias():
    """
    Test that authentication headers are stripped when redirecting between aliases 
    that resolve to the same machine but are distinct strings (localhost vs 127.0.0.1).
    Security best practices dictate stripping auth if the string origin differs.
    """
    session = Session()
    old_url = "http://localhost:8080/api"
    new_url = "http://127.0.0.1:8080/api"
    
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when redirecting between localhost and 127.0.0.1"