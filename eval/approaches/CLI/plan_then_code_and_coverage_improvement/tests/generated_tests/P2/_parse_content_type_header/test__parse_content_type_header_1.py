from requests.utils import _parse_content_type_header

def test_parse_content_type_simple():
    header = "text/html"
    expected = ("text/html", {})
    assert _parse_content_type_header(header) == expected
