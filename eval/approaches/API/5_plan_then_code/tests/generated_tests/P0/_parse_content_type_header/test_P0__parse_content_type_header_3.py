from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_values():
    """Test that quotes and surrounding whitespace are stripped from keys and values."""
    # The function strips single quotes, double quotes, and spaces from the tokens
    header = "application/xml; 'key'=\"value\"; foo= ' bar ' "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/xml"
    assert params == {
        "key": "value",
        "foo": "bar"
    }