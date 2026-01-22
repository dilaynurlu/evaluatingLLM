from requests.utils import _parse_content_type_header

def test_parse_content_type_whitespace_stripping():
    # Tests extensive whitespace around keys, values, and delimiters
    header = "text/html ;  key  =  value  "
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params == {"key": "value"}