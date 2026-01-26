from requests.utils import unquote_header_value

def test_unquote_header_value_empty_quoted():
    # Test that an empty quoted string returns an empty string
    header_val = '""'
    assert unquote_header_value(header_val) == ''