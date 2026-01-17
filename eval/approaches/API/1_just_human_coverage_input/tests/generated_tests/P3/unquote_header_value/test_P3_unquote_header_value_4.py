from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename_preserved():
    """
    Test that if is_filename is True and the value looks like a UNC path (starts with \\),
    the backslashes are NOT unescaped. This preserves UNC paths.
    """
    # Input represents: "\\server\share" surrounded by quotes
    value = r'"\\server\share"'
    
    # is_filename=True triggers the special UNC check
    result = unquote_header_value(value, is_filename=True)
    
    # The double backslashes at the start should remain double backslashes
    assert result == r"\\server\share"