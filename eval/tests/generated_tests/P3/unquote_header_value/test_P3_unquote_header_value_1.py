import pytest
from requests.utils import unquote_header_value

def test_unquote_simple_quoted_string_with_unicode():
    """
    Test unquoting a simple string surrounded by double quotes, 
    including Unicode characters to ensure encoding is handled correctly.
    """
    # Simple ASCII
    assert unquote_header_value('"simple_value"') == 'simple_value'
    
    # Unicode characters (e.g., thumbs up emoji and accented chars)
    # Input: "filename_👍_café.txt"
    header_value = '"filename_👍_café.txt"'
    expected = 'filename_👍_café.txt'
    
    result = unquote_header_value(header_value)
    assert result == expected