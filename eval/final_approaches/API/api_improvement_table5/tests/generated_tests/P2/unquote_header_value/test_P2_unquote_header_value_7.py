import pytest
from requests.utils import unquote_header_value

def test_unquote_unc_default_behavior():
    """
    Test that when is_filename=False (default), a value starting with \\
    is treated as a normal string and unescaped (double slash becomes single slash).
    """
    # Input represents: "\\server\share" surrounded by quotes
    input_value = r'"\\server\share"'
    
    # Default is_filename=False
    result = unquote_header_value(input_value)
    
    # Logic:
    # 1. Strips quotes -> \\server\share
    # 2. is_filename is False -> enters replace block
    # 3. Replace \\ -> \
    # Returns: \server\share
    assert result == r"\server\share"