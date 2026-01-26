from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_processed_if_not_filename():
    """
    Test that a string starting with a UNC-like path is fully unescaped 
    if is_filename is False.
    """
    # Input represents: "\\server\share" wrapped in quotes.
    value = r'"\\server\share"'
    
    # When is_filename=False, standard unescaping applies.
    # \\ matches \\\\ in replace pattern? No, the code does .replace('\\\\', '\\')
    # Since input string is raw literal r"...", it contains literal backslashes.
    # value[1:-1] is \\server\share
    # .replace('\\\\', '\\') turns the first two backslashes into one.
    
    expected = r'\server\share'
    assert unquote_header_value(value, is_filename=False) == expected