from requests.utils import _parse_content_type_header

def test__parse_content_type_header_8():
    # Trailing semicolon
    ct, params = _parse_content_type_header("text/html;")
    assert ct == "text/html"
    assert params == {}
