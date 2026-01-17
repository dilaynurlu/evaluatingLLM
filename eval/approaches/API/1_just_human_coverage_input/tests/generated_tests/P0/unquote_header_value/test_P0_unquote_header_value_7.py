from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    # Test that a string without surrounding quotes is returned as-is
    value = 'no_quotes'
    assert unquote_header_value(value) == value