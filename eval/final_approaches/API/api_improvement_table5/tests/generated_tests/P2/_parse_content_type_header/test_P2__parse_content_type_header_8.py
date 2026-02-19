from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_value():
    """
    Test a parameter where the key is followed by an equals sign but no value.
    This should result in an empty string value, not True.
    """
    header = "text/xml; key="
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/xml"
    assert params == {"key": ""}