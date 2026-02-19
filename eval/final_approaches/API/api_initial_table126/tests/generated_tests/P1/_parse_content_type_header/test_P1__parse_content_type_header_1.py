from requests.utils import _parse_content_type_header

def test_parse_simple_content_type():
    header = "application/json"
    result = _parse_content_type_header(header)
    assert result == ("application/json", {})