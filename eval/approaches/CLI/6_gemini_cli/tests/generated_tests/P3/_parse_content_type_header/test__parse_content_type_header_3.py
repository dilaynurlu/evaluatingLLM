from requests.utils import _parse_content_type_header

def test_parse_content_type_multiple_params():
    header = "multipart/form-data; boundary=something; charset=utf-8"
    ct, params = _parse_content_type_header(header)
    assert ct == "multipart/form-data"
    assert params == {"boundary": "something", "charset": "utf-8"}
