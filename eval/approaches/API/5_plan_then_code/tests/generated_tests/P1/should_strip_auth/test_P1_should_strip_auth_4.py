from requests.sessions import Session

def test_should_not_strip_auth_on_standard_http_to_https_upgrade():
    """
    Test the special case allowing http -> https redirects without stripping auth
    when using standard ports (implicit).
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "https://example.com/resource"
    
    # Special case: http (implicit 80) -> https (implicit 443) -> return False
    assert session.should_strip_auth(old_url, new_url) is False