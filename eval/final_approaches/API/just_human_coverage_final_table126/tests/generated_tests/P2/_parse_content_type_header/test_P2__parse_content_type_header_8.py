from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_keys():
    """
    Test that quotes around parameter keys are also stripped.
    """
    header = "application/octet-stream; \"filename\"=data.bin"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/octet-stream"
    assert params == {"filename": "data.bin"}