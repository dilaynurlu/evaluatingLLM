from requests.utils import _parse_content_type_header

def test_parse_content_type_header_1():
    header = "text/html"
    result = _parse_content_type_header(header)
    assert result == ("text/html", {})
