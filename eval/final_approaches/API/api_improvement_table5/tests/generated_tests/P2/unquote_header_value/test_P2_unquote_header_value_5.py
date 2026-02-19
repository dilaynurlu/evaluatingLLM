import pytest
from requests.utils import unquote_header_value

def test_unquote_filename_unc_preservation():
    """
    Test that when is_filename=True, a value starting with a UNC path (\\)
    strips the quotes but does NOT perform unescape replacements (to preserve the UNC double slash).
    """
    # Input represents: "\\server\share" surrounded by quotes
    # Python string literal for input: '"\\\\server\\share"'
    input_value = r'"\\server\share"'
    
    result = unquote_header_value(input_value, is_filename=True)
    
    # Logic: 
    # 1. Strips quotes -> \\server\share
    # 2. Checks is_filename (True) and starts with \\ (True)
    # 3. Skips replace logic.
    # Returns: \\server\share
    assert result == r"\\server\share"