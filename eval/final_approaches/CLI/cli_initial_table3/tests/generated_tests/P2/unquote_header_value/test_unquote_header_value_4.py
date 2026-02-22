from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc():
    """
    Test is_filename=True with UNC path.
    """
    # Input: "\server\share\file.txt" (with surrounding quotes)
    # Python repr: r'"\\server\share\file.txt"'
    value = r'"\\server\share\file.txt"'
    
    # Without is_filename=True (default False)
    # \\server becomes \server
    result_default = unquote_header_value(value)
    # Expected: \server\share\file.txt
    assert result_default == r"\server\share\file.txt"
    
    # With is_filename=True
    # Should preserve double backslash at start
    result_filename = unquote_header_value(value, is_filename=True)
    # Expected: \\server\share\file.txt
    assert result_filename == r"\\server\share\file.txt"

