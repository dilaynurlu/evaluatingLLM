from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_params():
    header = "application/json; ; ; charset=utf-8"
    expected = ("application/json", {"charset": "utf-8"})
    assert _parse_content_type_header(header) == expected
