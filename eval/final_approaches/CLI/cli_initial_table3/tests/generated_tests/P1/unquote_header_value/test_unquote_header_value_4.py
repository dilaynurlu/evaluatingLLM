from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc():
    """Test preserving UNC paths when is_filename is True."""
    # A UNC path starts with \\
    # If is_filename=True, unquote_header_value should preserve the double backslash
    # even if it's inside quotes.
    
    input_val = r'"\\server\share\file.txt"'
    # Expected: outer quotes removed, but internal backslashes NOT unescaped because it starts with \\
    expected = r'\\server\share\file.txt'
    
    assert unquote_header_value(input_val, is_filename=True) == expected

