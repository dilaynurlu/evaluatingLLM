from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_protocol_relative():
    """
    Test prepending a scheme to a protocol-relative URL containing authentication.
    Using '//' ensures the input is parsed as an authority (user:pass@host) rather than a scheme.
    The function must correctly reconstruct the URL including the auth info.
    """
    # '//' forces 'user:pass@db.local' to be parsed as netloc components, not scheme.
    url = "//user:pass@db.local:5432/my_db"
    new_scheme = "postgresql"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    # Expected: scheme is added, auth and port are preserved in the correct format.
    assert result == "postgresql://user:pass@db.local:5432/my_db"