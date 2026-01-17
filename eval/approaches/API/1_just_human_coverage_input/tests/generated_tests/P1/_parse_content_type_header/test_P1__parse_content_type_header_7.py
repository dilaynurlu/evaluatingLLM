from requests.utils import _parse_content_type_header

def test_parse_content_type_single_quotes():
    """
    Test parsing parameters with single-quoted values.
    Verifies that single quotes are also stripped from the value.
    """
    header = "application/javascript; version='1.0'"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/javascript"
    assert params == {"version": "1.0"}