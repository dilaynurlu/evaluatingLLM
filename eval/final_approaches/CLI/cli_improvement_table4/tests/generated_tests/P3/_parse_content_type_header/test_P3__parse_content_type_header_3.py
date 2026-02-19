import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_quoted_params():
    header = 'multipart/form-data; boundary="foo;bar"'
    content_type, params = _parse_content_type_header(header)
    assert content_type == "multipart/form-data"
    # Actual behavior splits on semicolon even inside quotes
    assert params == {'boundary': 'foo', 'bar"': True}
