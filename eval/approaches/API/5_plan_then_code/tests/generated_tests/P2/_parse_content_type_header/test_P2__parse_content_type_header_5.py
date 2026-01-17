from requests.utils import _parse_content_type_header

def test_parse_content_type_header_whitespace_and_empty_segments():
    """
    Test that the parser handles excessive whitespace and empty segments (consecutive semicolons) correctly.
    """
    header = "  text/plain  ;  ;  format  =  flowed  ;  "
    expected_content_type = "text/plain"
    expected_params = {"format": "flowed"}
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params