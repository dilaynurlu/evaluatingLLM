from requests.sessions import Session

def test_should_strip_auth_default_to_custom_port():
    """
    Test that auth is stripped when changing from a default port to a custom port
    on the same scheme.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://example.com:8080/resource"
    
    # Port changes from default (80/None) to 8080.
    # default_port logic checks fails for new_url.
    # changed_port is True -> return True
    assert session.should_strip_auth(old_url, new_url) is True