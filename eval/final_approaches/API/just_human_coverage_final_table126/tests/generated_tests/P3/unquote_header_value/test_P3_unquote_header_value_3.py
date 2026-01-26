from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quote():
    """
    Test that escaped quotes within the string are unescaped.
    Also verifies handling of control characters inside the string.
    """
    # Standard escaped quote: "foo\"bar" -> foo"bar
    input_val = r'"foo\"bar"'
    expected = 'foo"bar'
    assert unquote_header_value(input_val) == expected

    # Multiple escaped quotes
    input_multi = r'"\"quoted\" within"'
    expected_multi = '"quoted" within'
    assert unquote_header_value(input_multi) == expected_multi

    # Control characters (e.g., newlines) should be preserved if they exist literally
    # Case: "Line\nBreak"
    input_ctrl = '"Line\nBreak"'
    expected_ctrl = 'Line\nBreak'
    assert unquote_header_value(input_ctrl) == expected_ctrl