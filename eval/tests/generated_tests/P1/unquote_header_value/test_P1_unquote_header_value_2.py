import pytest
from requests.utils import unquote_header_value

def test_unquote_escaped_characters():
    """
    Test that escaped quotes and backslashes are correctly unescaped.
    Scenario: Input contains escaped quote (\") and escaped backslash (\\\\).
    Input header: "foo\"bar\\baz"
    Expected result: foo"bar\baz
    """
    # Represents the string: "foo\"bar\\baz"
    input_value = r'"foo\"bar\\baz"'
    
    # Expected unquoted: foo"bar\baz
    expected_value = r'foo"bar\baz'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value