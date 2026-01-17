from requests.utils import unquote_header_value

def test_unquote_header_value_literals_and_single_quotes():
    """
    Test that strings without double quotes, empty strings, and single-quoted strings 
    are returned as-is. This addresses critiques regarding single quotes and empty unquoted strings.
    """
    # Standard unquoted
    assert unquote_header_value("simple_value") == "simple_value"
    
    # Empty unquoted string
    assert unquote_header_value("") == ""
    
    # Single quotes should be treated as literal characters, not delimiters
    assert unquote_header_value("'single_quoted'") == "'single_quoted'"