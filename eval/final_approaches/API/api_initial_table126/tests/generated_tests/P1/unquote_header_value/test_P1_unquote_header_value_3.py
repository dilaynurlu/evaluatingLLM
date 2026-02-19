from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename_preservation():
    """
    Test that if the value is a filename and starts with a UNC path (double backslash),
    the backslashes are NOT unescaped to preserve the UNC path.
    """
    # Input represents: "\\server\share" wrapped in quotes.
    value = '"\\\\server\\share"'
    
    # Since is_filename=True and it starts with \\, it should just strip quotes
    # and NOT replace \\\\ with \\.
    result = unquote_header_value(value, is_filename=True)
    
    assert result == '\\\\server\\share'