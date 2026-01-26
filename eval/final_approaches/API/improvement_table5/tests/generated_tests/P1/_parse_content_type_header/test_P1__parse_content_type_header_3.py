import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_strips_quotes_and_spaces():
    """Test that quotes and extra spaces are stripped from keys and values."""
    # This covers the items_to_strip = "\"' " logic for both keys and values
    header = "text/html;  charset = \"utf-8\" "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/html"
    assert params == {"charset": "utf-8"}