import pytest
from requests.utils import unquote_header_value

def test_non_filename_unc_path_replacement():
    """
    Test that UNC-like strings are unescaped (double backslashes to single)
    when is_filename is False. The special UNC preservation logic should not trigger.
    """
    # Input: "\\server\share" (inside quotes)
    # This acts as an escaped backslash followed by server...
    header_value = r'"\\server\share"'
    
    # Logic: 
    # 1. Strip quotes -> \\server\share
    # 2. is_filename=False -> Replace \\ with \
    # Result: \server\share
    expected = r'\server\share'
    
    result = unquote_header_value(header_value, is_filename=False)
    assert result == expected