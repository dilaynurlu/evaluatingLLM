import pytest
from requests.utils import unquote_header_value

def test_return_original_if_not_quoted_variants():
    """
    Test that strings not strictly surrounded by double quotes are returned as is.
    This includes:
    1. Plain strings.
    2. Single-quoted strings (treated as literals).
    3. Strings with surrounding whitespace (prevents quote matching).
    """
    # Plain
    assert unquote_header_value('simple_value') == 'simple_value'
    
    # Single quotes - should NOT be unquoted
    assert unquote_header_value("'single_quoted'") == "'single_quoted'"
    
    # Whitespace surrounding double quotes
    # The function expects the very first and last characters to be quotes.
    padded_value = ' "spaced_value" '
    assert unquote_header_value(padded_value) == padded_value