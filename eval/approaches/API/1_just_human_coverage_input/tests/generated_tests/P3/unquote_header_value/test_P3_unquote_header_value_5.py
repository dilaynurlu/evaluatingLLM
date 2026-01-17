from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path_not_filename():
    """
    Test that if is_filename is False, a value that looks like a UNC path (starts with \\)
    IS unescaped (double backslashes become single), treating it as normal text.
    """
    # Input represents: "\\server\share" surrounded by quotes
    value = r'"\\server\share"'
    
    # is_filename=False (default) should apply standard replacement
    result = unquote_header_value(value, is_filename=False)
    
    # The double backslashes should be replaced by single backslashes
    assert result == r"\server\share"