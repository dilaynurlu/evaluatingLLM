from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_string():
    # Empty string should result in empty content type and empty params
    header = ""
    result = _parse_content_type_header(header)
    assert result == ("", {})