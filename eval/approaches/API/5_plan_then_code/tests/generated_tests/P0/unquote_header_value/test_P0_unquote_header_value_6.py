import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_looking_not_filename():
    """
    Test unquoting a string that looks like a UNC path but is_filename=False.
    Should apply standard unescaping (converting \\ to \).
    """
    # Input represents: "\\server\share"
    # Stripped: \\server\share
    # Since is_filename=False, it should process escapes.
    # \\ (double backslash char) -> \ (single backslash char)
    input_val = r'"\\server\share"'
    
    # \ matches the first slash, \ matches the second. 
    # Wait, the input string (stripped) is: \ \ s e r v e r \ s h a r e
    # replace('\\\\', '\\') looks for TWO backslashes.
    # It finds them at the start. Replaces with ONE backslash.
    # Result: \server\share
    expected = r'\server\share'
    
    result = unquote_header_value(input_val, is_filename=False)
    assert result == expected