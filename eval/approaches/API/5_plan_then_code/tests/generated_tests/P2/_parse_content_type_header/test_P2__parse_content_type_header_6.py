from requests.utils import _parse_content_type_header

def test_parse_content_type_header_strips_quotes_from_keys():
    """
    Test that the parser strips quotes from parameter keys as well as values.
    """
    header = 'text/csv; "header"="present"'
    expected_content_type = "text/csv"
    expected_params = {"header": "present"}
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params