from requests.utils import unquote_header_value

def test_unquote_header_value_unicode_and_whitespace():
    """
    Test that strings containing Unicode characters and preserving whitespace 
    are correctly unquoted.
    """
    # Input: "  café \u2603  " (includes spaces, unicode e-acute, and snowman)
    value = '"  café \u2603  "'
    result = unquote_header_value(value)
    
    # Whitespace and Unicode should be preserved exactly as is
    expected = '  café \u2603  '
    assert result == expected