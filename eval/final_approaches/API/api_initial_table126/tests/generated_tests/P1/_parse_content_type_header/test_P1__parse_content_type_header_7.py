from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_segments():
    # Double semicolons (empty segments) should be ignored
    header = "text/css;; charset=utf-8"
    result = _parse_content_type_header(header)
    assert result == ("text/css", {"charset": "utf-8"})