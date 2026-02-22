from requests.utils import _parse_content_type_header

def test_parse_content_type_header_3():
    header = 'text/html; charset="utf-8"'
    result = _parse_content_type_header(header)
    assert result == ("text/html", {"charset": "utf-8"})
