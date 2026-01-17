from requests.utils import _parse_content_type_header

def test_parse_content_type_header_mixed_quotes():
    """
    Test parsing mixed single and double quotes in different parameters.
    """
    header = "application/example; foo='bar'; baz=\"qux\""
    expected_content_type = "application/example"
    expected_params = {
        "foo": "bar",
        "baz": "qux"
    }
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params