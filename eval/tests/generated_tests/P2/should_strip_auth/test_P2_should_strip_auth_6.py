import requests

def test_should_keep_auth_on_implicit_vs_explicit_default_port():
    """
    Test that Authorization headers are PRESERVED when redirecting between
    an implicit default port and an explicit default port for the same scheme.
    """
    session = requests.Session()
    # HTTP implicit port is 80. Explicit port is 80.
    old_url = "http://example.com/page"
    new_url = "http://example.com:80/page"
    
    # The function detects that both ports resolve to the default for 'http'.
    assert session.should_strip_auth(old_url, new_url) is False