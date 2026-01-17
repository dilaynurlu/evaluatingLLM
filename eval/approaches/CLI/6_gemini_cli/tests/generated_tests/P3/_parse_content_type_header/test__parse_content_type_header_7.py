from requests.utils import _parse_content_type_header

def test_parse_content_type_empty():
    header = ""
    # Code splits by ';', takes first as content_type.
    ct, params = _parse_content_type_header(header)
    assert ct == ""
    assert params == {}
