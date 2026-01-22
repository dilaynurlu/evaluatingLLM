from requests.utils import _parse_content_type_header

def test_parse_content_type_header_5():
    # Test empty string
    ct, params = _parse_content_type_header("")
    assert ct == ""
    assert params == {}
