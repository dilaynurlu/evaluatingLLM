import pytest
from requests.utils import unquote_header_value

def test_unquote_unc_like_value_collapsed_when_not_filename():
    """
    Test that a value starting with \\ is collapsed to start with \ if is_filename=False.
    This exercises the default behavior where backslashes are unescaped.
    """
    # Input represents: "\\server\share" inside quotes.
    input_value = r'"\\server\share"'
    
    # Expected: Outer quotes stripped.
    # The double backslash \\\\ (escaped backslash) is replaced by single backslash \\.
    # So \\server becomes \server.
    expected_value = r'\server\share'
    
    # is_filename defaults to False
    result = unquote_header_value(input_value)
    
    assert result == expected_value