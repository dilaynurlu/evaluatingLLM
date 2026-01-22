from requests.utils import _parse_content_type_header

def test_parse_content_type_irregular_whitespace():
    # Whitespace around keys/values and delimiters should be handled/stripped
    header = "  text/plain  ;  key  =  value  "
    result = _parse_content_type_header(header)
    assert result == ("text/plain", {"key": "value"})