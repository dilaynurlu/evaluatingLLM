from requests.sessions import Session

def test_should_not_strip_auth_mixed_implicit_explicit_upgrade():
    """
    Test the special case http->https upgrade when one port is explicit and the other implicit,
    but both are standard.
    """
    session = Session()
    old_url = "http://example.com:80/resource"
    new_url = "https://example.com/resource"
    
    # Old is http:80 (standard), New is https:None (standard).
    # Matches special case criteria -> return False
    assert session.should_strip_auth(old_url, new_url) is False