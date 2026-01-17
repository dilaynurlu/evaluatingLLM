from requests.utils import unquote_header_value

def test_unquote_header_value_basic_quoted_string():
    # Test unquoting a simple string without any escape characters
    value = '"simple_value"'
    expected = 'simple_value'
    assert unquote_header_value(value) == expected