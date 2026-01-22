from requests.utils import _parse_content_type_header

def test_parse_content_type_flag():
    header = "text/plain; no_equals"
    expected = ("text/plain", {"no_equals": True})
    assert _parse_content_type_header(header) == expected
