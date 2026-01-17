from requests.utils import unquote_header_value

def test_unquote_header_value_unbalanced_quotes():
    # Scenario: If the string does not have matching quotes at start and end,
    # it is returned as is.
    input_val = '"unbalanced'
    # No change expected
    assert unquote_header_value(input_val) == input_val