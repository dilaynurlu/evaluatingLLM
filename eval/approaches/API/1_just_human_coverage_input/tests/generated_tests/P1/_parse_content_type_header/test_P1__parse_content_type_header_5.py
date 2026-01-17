from requests.utils import _parse_content_type_header

def test_parse_content_type_standalone_flag():
    """
    Test parsing a parameter that has no value (no equals sign).
    Verifies that such parameters are assigned a value of True.
    """
    header = "text/csv; header"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/csv"
    assert params == {"header": True}