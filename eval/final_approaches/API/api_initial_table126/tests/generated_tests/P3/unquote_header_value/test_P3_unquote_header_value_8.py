from requests.utils import unquote_header_value

def test_unquote_header_value_empty_quotes():
    """Test that an empty quoted string returns an empty string."""
    input_val = '""'
    expected = ''
    assert unquote_header_value(input_val) == expected