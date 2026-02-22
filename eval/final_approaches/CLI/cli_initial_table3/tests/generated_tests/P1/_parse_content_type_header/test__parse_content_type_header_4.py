from requests.utils import _parse_content_type_header

def test_parse_content_type_header_single_quotes():
    header = "application/x; param='val'"
    ct, params = _parse_content_type_header(header)
    assert ct == "application/x"
    assert params == {"param": "val"}
