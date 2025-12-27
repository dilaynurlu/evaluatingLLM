from requests.utils import unquote_header_value

def test_unquote_header_value_mixed_escapes():
    """
    Test a complex string containing both escaped quotes and escaped backslashes.
    """
    # Input represents: "quote\" and backslash\\"
    header = r'"quote\" and backslash\\"'
    
    # Expected: quote" and backslash\
    expected = r'quote" and backslash\'
    
    result = unquote_header_value(header)
    assert result == expected


'''
SnytaxError: unterminated string literal
'''