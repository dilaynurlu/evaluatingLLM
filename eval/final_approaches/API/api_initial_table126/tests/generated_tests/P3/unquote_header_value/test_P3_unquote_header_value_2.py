from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """
    Test that strings without valid surrounding double quotes are returned unchanged.
    This includes strings with single quotes or surrounding whitespace.
    """
    # Plain string
    assert unquote_header_value('simple_value') == 'simple_value'
    
    # Single quotes are not stripped
    assert unquote_header_value("'single_quoted'") == "'single_quoted'"
    
    # Whitespace outside double quotes invalidates the check (implementation does not trim)
    # Input: ' "quoted" ' -> returns as-is because it doesn't start/end with "
    assert unquote_header_value(' "quoted" ') == ' "quoted" '