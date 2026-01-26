from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preserved():
    """
    Test that a filename starting with a UNC path (double backslash) 
    is returned without attempting to unescape backslashes, 
    to prevent corrupting the UNC path.
    """
    # Input represents: "\\server\share" wrapped in quotes.
    # The inner content starts with \\.
    value = r'"\\server\share"'
    
    # When is_filename=True, and it starts with \\, no replacement is done.
    # If replacement were done, \\ would become \.
    assert unquote_header_value(value, is_filename=True) == r'\\server\share'