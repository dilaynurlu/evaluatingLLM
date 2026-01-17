import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_normalizes_keys_to_lowercase():
    # Parameter keys should be lowercased, but values should preserve case
    header = "text/html; Charset=UTF-8"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "UTF-8"}