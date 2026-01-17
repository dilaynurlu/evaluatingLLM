import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quote():
    """
    Test that escaped double quotes within the header value are correctly unescaped.
    Input: "Foo\"Bar" -> Expected: Foo"Bar
    """
    # The raw string r'"Foo\"Bar"' represents the literal characters: " F o o \ " B a r "
    input_value = r'"Foo\"Bar"'
    expected_value = 'Foo"Bar'
    
    result = unquote_header_value(input_value)
    
    assert result == expected_value