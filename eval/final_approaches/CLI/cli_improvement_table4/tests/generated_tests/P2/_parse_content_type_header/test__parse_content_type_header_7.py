from requests.utils import _parse_content_type_header

def test_parse_content_type_value_with_equals():
    header = "text/plain; key=value=more"
    # Implementation splits on first '='
    expected = ("text/plain", {"key": "value=more"})
    assert _parse_content_type_header(header) == expected
