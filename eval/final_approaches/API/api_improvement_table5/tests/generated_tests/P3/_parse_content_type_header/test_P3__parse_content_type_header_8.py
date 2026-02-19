import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_value():
    """
    Test parsing a parameter where the key is present but the value is empty.
    """
    header = "text/csv; header="
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/csv"
    assert params == {"header": ""}