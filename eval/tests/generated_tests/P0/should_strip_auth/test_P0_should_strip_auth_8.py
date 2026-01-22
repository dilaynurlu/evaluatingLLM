from requests.sessions import Session

def test_should_strip_auth_implicit_explicit_default_port_mix():
    """
    Test that authentication headers are preserved when ports differ syntactically 
    (implicit vs explicit) but are semantically the same default port for the scheme.
    """
    session = Session()
    old_url = "http://example.com/foo"      # Implicit port 80
    new_url = "http://example.com:80/bar"   # Explicit port 80
    
    # Default port logic should detect that None (implicit) and 80 (explicit) are equivalent for http
    assert session.should_strip_auth(old_url, new_url) is False