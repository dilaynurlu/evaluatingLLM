from requests.utils import _parse_content_type_header

def test_parse_content_type_header_flag_parameter():
    """
    Test parsing a content-type header containing a parameter with no value (no equals sign).
    The function should treat this as a flag with a boolean True value.
    """
    header = "multipart/form-data; boundary=something; immutable"
    expected_content_type = "multipart/form-data"
    expected_params = {
        "boundary": "something",
        "immutable": True
    }
    
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == expected_content_type
    assert params == expected_params