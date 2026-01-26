from requests.utils import unquote_header_value

def test_unquote_mismatched_quotes():
    """Test that a string with mismatched quotes is returned unchanged."""
    input_val = '"mismatched'
    assert unquote_header_value(input_val) == '"mismatched'