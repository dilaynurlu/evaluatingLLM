from requests.utils import _parse_content_type_header

def test_parse_content_type_header_6():
    # Test no subtype or invalid format
    header = "application"
    ct, params = _parse_content_type_header(header)
    assert ct == "application"
    assert params == {}
