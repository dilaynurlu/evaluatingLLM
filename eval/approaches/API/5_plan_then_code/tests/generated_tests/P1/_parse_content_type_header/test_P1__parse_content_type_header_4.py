from requests.utils import _parse_content_type_header

def test_parse_content_type_boolean_param():
    """Test parsing a parameter that has no value assignment (no equals sign), resulting in True."""
    header = "text/xml; secure"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/xml"
    assert params == {"secure": True}