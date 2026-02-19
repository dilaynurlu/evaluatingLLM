from requests.utils import unquote_header_value

def test_unquote_header_value_unbalanced_quotes():
    """Test that a string with unbalanced quotes is returned unchanged."""
    # Only starting quote
    value = '"start_only'
    assert unquote_header_value(value) == '"start_only'