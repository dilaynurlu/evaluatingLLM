from requests.utils import unquote_header_value

def test_unquote_no_quotes():
    """Test that a string without surrounding quotes is returned unchanged."""
    input_val = 'plain_text'
    assert unquote_header_value(input_val) == 'plain_text'