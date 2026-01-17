from requests.utils import _parse_content_type_header

def test_parse_content_type_malformed_semicolon():
    header = ";"
    ct, params = _parse_content_type_header(header)
    assert ct == ""
    assert params == {}
