from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    """
    Test that strings with only one quote (start or end) or mismatched types are returned as-is.
    """
    # Start quote only
    assert unquote_header_value('"start_only') == '"start_only'
    
    # End quote only
    assert unquote_header_value('end_only"') == 'end_only"'