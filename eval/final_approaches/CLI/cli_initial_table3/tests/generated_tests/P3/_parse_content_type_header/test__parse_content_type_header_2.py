import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_2():
    header = "text/html; charset=utf-8; boundary=something"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    assert params["charset"] == "utf-8"
    assert params["boundary"] == "something"
