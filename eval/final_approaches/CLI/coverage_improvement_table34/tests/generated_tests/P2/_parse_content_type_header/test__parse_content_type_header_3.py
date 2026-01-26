from requests.utils import _parse_content_type_header

def test_parse_content_type_multiple_params_whitespace():
    header = " multipart/form-data ; boundary=something ; charset=utf-8 "
    expected = ("multipart/form-data", {"boundary": "something", "charset": "utf-8"})
    assert _parse_content_type_header(header) == expected
