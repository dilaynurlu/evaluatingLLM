from requests.utils import _parse_content_type_header

def test_parse_content_type_value_containing_equals():
    # Only the first equals sign separates key/value
    header = "text/x-dvi; name=foo=bar"
    result = _parse_content_type_header(header)
    assert result == ("text/x-dvi", {"name": "foo=bar"})