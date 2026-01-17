from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_protocol_relative_complex_auth():
    # Scenario: URL is protocol-relative with complex authentication (e.g. multiple @ symbols).
    # Critique addressed: Malformed URLs/Fuzzing style inputs.
    # Ensure correct parsing of user info even when special characters are present.
    url = "//user:p@ssword@db.internal"
    new_scheme = "postgresql"
    
    result = prepend_scheme_if_needed(url, new_scheme)
    
    assert result == "postgresql://user:p@ssword@db.internal"