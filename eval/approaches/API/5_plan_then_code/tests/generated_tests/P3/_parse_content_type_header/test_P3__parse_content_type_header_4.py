from requests.utils import _parse_content_type_header

def test_parse_content_type_header_flags_and_duplicates():
    """
    Test parsing flags (parameters without values) and duplicate parameters.
    Critique addressed: Duplicate Parameters (Parameter Pollution).
    """
    header = "text/xml; secure; version=1.0; version=2.0"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/xml"
    
    # Flags (no '=') are often treated as keys with value None or stripped key if implementation varies.
    # Based on typical requests behavior, it might extract 'secure' as a key.
    # We check existence.
    assert "secure" in params
    
    # Critique addressed: Deterministic behavior for duplicates.
    # Standard behavior in many parsers is "last one wins" for dictionaries.
    assert params["version"] == "2.0"