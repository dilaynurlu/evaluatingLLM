from requests.sessions import Session

def test_should_not_strip_auth_implicit_to_explicit_http_port():
    """
    Test that auth is preserved when redirecting from implicit http port to explicit port 80.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://example.com:80/resource"
    
    # Implicit None and explicit 80 are treated as equal for 'http' scheme.
    # default_port logic -> return False
    assert session.should_strip_auth(old_url, new_url) is False