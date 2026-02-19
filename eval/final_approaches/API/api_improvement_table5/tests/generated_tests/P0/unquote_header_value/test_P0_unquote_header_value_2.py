from requests.utils import unquote_header_value

def test_unquote_header_value_unquoted():
    # Test that a string without quotes is returned unchanged
    header_val = 'test_value'
    assert unquote_header_value(header_val) == 'test_value'