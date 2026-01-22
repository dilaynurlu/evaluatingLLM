from requests.utils import _parse_content_type_header

def test_parse_content_type_header_2():
    header = "text/html; charset=utf-8"
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params == {"charset": "utf-8"}
