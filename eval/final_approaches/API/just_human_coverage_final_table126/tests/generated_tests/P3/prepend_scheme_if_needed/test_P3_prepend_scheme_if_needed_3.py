from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_protocol_relative_auth():
    """
    Test prepending a scheme to a protocol-relative URL containing authentication.
    Ensures that URLs starting with '//' are correctly handled as having no scheme.
    """
    # Standard protocol relative URL with auth
    url = "//user:password@db.internal:5432/production"
    new_scheme = "postgresql"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "postgresql://user:password@db.internal:5432/production"