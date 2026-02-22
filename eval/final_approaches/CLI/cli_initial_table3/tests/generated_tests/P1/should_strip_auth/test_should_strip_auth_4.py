from requests.sessions import Session

def test_should_strip_auth_downgrade():
    s = Session()
    old = "https://example.com/foo"
    new = "http://example.com/bar"
    # Downgrade is NOT safe, auth stripped.
    assert s.should_strip_auth(old, new) is True
