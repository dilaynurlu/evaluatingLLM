from requests.sessions import Session

def test_should_strip_auth_on_non_standard_http_to_https_upgrade():
    """
    Test that the special http->https allowance does NOT apply if ports are non-standard.
    """
    session = Session()
    old_url = "http://example.com:8080/resource"
    new_url = "https://example.com:8443/resource"
    
    # Non-standard ports do not match the (80, None)/(443, None) requirement.
    # changed_port=True, changed_scheme=True -> return True
    assert session.should_strip_auth(old_url, new_url) is True