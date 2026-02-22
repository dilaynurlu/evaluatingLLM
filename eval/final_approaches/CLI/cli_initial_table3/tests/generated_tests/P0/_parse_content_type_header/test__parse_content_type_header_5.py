from requests.utils import _parse_content_type_header

def test_parse_content_type_header_5():
    header = "text/html; myspecialparam"
    result = _parse_content_type_header(header)
    assert result == ("text/html", {"myspecialparam": True})
