import pytest
from requests.utils import unquote_header_value

@pytest.mark.parametrize("input_val, expected", [
    (r'"foo\\bar"', r'foo\bar'),           # Single escaped backslash
    (r'"foo\\\\bar"', r'foo\\bar'),        # Double escaped backslash
    (r'"\\"', r'\ '),                      # Escaped backslash at start (ignoring space for clarity: "\\" -> "\")
                                           # Note: "\\" inside quotes is a literal backslash.
    (r'"C:\\Program Files"', r'C:\Program Files') 
])
def test_unquote_header_value_escaped_backslash(input_val, expected):
    """
    Refined test for backslash unescaping logic.
    Ensures that literal backslashes represented as '\\' in the quoted string
    are correctly unescaped to '\'.
    """
    # Note: Using strip() to handle the specific case of lonely backslash if needed, 
    # but strictly "\\" -> \
    if input_val == r'"\\"':
        expected = '\\'
        
    assert unquote_header_value(input_val, is_filename=False) == expected