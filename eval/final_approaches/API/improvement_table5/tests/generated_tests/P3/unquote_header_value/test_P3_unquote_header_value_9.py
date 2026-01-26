from requests.utils import unquote_header_value

def test_unquote_header_value_unbalanced_quotes():
    """Test that strings with unbalanced quotes are returned unchanged."""
    # Case 1: Start quote only
    assert unquote_header_value('"start_only') == '"start_only'
    # Case 2: End quote only
    assert unquote_header_value('end_only"') == 'end_only"'