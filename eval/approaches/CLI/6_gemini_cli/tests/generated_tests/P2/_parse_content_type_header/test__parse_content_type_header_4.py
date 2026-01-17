import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_multiple_params():
    # Scenario: Multiple parameters
    header = "multipart/form-data; boundary=something; charset=utf-8"
    ctype, params = _parse_content_type_header(header)
    assert ctype == "multipart/form-data"
    assert params == {"boundary": "something", "charset": "utf-8"}
