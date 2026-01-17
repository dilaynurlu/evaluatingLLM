import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """
    Test that escaped backslashes are correctly unescaped when is_filename is False (default).
    Input: "Foo\\Bar" -> Expected: Foo\Bar
    """
    # Input literal: "Foo\\Bar" (quoted)
    # Python string for input: '"Foo\\\\Bar"' -> memory: "Foo\\Bar"
    input_value = '"Foo\\\\Bar"'
    
    # Expected: Foo\Bar
    expected_value = 'Foo\\Bar'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value