from requests.utils import unquote_header_value

def test_unquote_header_value_simple_quotes():
    # Scenario: A simple quoted string should have its surrounding quotes removed
    input_val = '"simple"'
    expected = 'simple'
    assert unquote_header_value(input_val) == expected