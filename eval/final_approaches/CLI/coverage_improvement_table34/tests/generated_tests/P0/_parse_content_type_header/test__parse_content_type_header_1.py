from requests.utils import _parse_content_type_header

def test_parse_content_type_header_1():
    header = "application/json"
    ct, params = _parse_content_type_header(header)
    assert ct == "application/json"
    assert params == {}
