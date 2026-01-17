from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_quotes():
    # Scenario: Escaped quotes inside the quoted string should be unescaped
    # Input corresponds to header value: "foo\"bar"
    # The inner content is: foo\"bar
    # Expected result: foo"bar
    input_val = r'"foo\"bar"'
    expected = 'foo"bar'
    assert unquote_header_value(input_val) == expected