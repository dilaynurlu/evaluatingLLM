from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    # Test that a string with mismatched quotes is returned as is
    header_val = '"mismatched'
    assert unquote_header_value(header_val) == header_val