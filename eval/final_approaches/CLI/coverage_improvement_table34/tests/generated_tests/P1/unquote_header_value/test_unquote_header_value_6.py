import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal():
    """Test unquoting normal filename (should unescape)."""
    value = '"file.txt"'
    assert unquote_header_value(value, is_filename=True) == "file.txt"
