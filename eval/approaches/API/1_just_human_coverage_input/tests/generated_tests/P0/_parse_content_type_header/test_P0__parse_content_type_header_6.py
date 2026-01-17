from requests.utils import _parse_content_type_header

def test_parse_content_type_header_multiple_params():
    """
    Test parsing a Content-Type header with multiple parameters.
    """
    header = "multipart/form-data; boundary=something; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {'boundary': 'something', 'charset': 'utf-8'}