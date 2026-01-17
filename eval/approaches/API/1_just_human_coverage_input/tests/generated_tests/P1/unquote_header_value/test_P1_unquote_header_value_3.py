from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslashes():
    # Scenario: Escaped backslashes should be unescaped (doubled backslashes become single)
    # when not triggering the special filename UNC logic.
    # Input corresponds to header value: "foo\\bar"
    # Inner content: foo\\bar
    # Expected result: foo\bar
    input_val = r'"foo\\bar"'
    expected = r'foo\bar'
    assert unquote_header_value(input_val) == expected