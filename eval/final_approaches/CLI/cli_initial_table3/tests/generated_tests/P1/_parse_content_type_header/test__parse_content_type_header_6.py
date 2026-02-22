from requests.utils import _parse_content_type_header

def test_parse_content_type_header_multiple():
    header = "type/subtype; p1=v1; p2=v2"
    ct, params = _parse_content_type_header(header)
    assert ct == "type/subtype"
    assert params == {"p1": "v1", "p2": "v2"}
