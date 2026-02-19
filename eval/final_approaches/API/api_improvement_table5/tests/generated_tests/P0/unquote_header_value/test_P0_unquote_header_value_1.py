from requests.utils import unquote_header_value

def test_unquote_header_value_simple_quoted():
    # Test a standard double-quoted string is unquoted correctly
    header_val = '"test_value"'
    assert unquote_header_value(header_val) == 'test_value'