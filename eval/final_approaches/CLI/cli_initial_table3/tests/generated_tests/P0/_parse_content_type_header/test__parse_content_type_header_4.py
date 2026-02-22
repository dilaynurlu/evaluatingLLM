from requests.utils import _parse_content_type_header

def test_parse_content_type_header_4():
    header = "multipart/form-data; boundary=something; charset=utf-8"
    result = _parse_content_type_header(header)
    assert result == ("multipart/form-data", {"boundary": "something", "charset": "utf-8"})
