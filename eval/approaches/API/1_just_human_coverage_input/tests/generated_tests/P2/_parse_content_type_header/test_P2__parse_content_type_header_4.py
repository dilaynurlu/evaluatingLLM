import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_strips_double_quotes_from_values():
    header = 'multipart/form-data; boundary="some-boundary-value"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {"boundary": "some-boundary-value"}