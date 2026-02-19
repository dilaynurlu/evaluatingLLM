from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preserved():
    """
    Test that when is_filename=True, a string starting with a UNC path (\\)
    preserves its backslashes and skips unescaping to avoid corruption.
    """
    # Input represents: "\\server\share"
    # Wrapped in quotes: " \\server\share "
    input_val = r'"\\server\share"'
    
    # If standard unescaping ran, \\ would become \. 
    # Since it is a filename and starts with \\, it should remain \\.
    expected = r'\\server\share'
    
    assert unquote_header_value(input_val, is_filename=True) == expected

    # Extended UNC path check
    input_long = r'"\\?\UNC\server\share"'
    expected_long = r'\\?\UNC\server\share'
    assert unquote_header_value(input_long, is_filename=True) == expected_long