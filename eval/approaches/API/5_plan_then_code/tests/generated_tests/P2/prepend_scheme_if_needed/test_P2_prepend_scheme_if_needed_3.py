from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_with_auth_protocol_relative():
    """
    Test prepending a scheme to a protocol-relative URL that includes authentication.
    The function contains specific logic to reconstruct the netloc with auth info.
    """
    # Using // ensures parse_url identifies the authority correctly without a scheme.
    url = "//user:secret@db.internal:5432/db"
    new_scheme = "postgresql"
    expected = "postgresql://user:secret@db.internal:5432/db"
    
    assert prepend_scheme_if_needed(url, new_scheme) == expected