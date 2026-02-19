from requests.sessions import Session

def test_should_strip_auth_non_standard_upgrade():
    """
    Test that authentication is STRIPPED when upgrading from HTTP to HTTPS
    if non-standard ports are used.
    """
    session = Session()
    old_url = "http://example.com:8080/a"
    new_url = "https://example.com:8443/b"
    
    # Logic:
    # 1. Host matches.
    # 2. Scheme changes http->https.
    # 3. Ports are not standard (80/443), so the upgrade exception does not apply.
    # Expected: True
    assert session.should_strip_auth(old_url, new_url) is True