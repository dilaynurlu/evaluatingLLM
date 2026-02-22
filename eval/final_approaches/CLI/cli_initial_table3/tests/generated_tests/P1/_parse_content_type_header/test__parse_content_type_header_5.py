from requests.utils import _parse_content_type_header

def test_parse_content_type_header_no_value():
    header = "text/html; secure"
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params == {"secure": True}
