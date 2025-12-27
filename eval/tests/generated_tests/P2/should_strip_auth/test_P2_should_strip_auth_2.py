import requests

def test_should_strip_auth_on_scheme_downgrade():
    """
    Test that Authorization headers are stripped when downgrading the scheme
    from HTTPS to HTTP, even if the hostname remains the same.
    """
    session = requests.Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # HTTPS to HTTP downgrade is not protected by the special case,
    # and changed_scheme will be True. Should strip auth.
    assert session.should_strip_auth(old_url, new_url) is True