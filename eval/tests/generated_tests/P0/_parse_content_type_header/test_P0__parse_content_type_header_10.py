from requests.utils import _parse_content_type_header

def test_parse_content_type_missing_type():
    # Tests input starting with a semicolon (no content type)
    header = "; charset=utf-8"
    content_type, params = _parse_content_type_header(header)
    assert content_type == ""
    assert params == {"charset": "utf-8"}