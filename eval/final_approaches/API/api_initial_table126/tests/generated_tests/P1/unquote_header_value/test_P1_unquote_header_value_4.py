from requests.utils import unquote_header_value

def test_unquote_header_value_unc_non_filename_replacement():
    """
    Test that if the value starts with a UNC path pattern but is NOT marked as a filename,
    standard unescaping rules apply (double backslashes become single).
    """
    # Input represents: "\\server\share" wrapped in quotes.
    value = '"\\\\server\\share"'
    
    # Since is_filename=False, the leading \\\\ is treated as an escaped backslash
    # and replaced by \\.
    # \\server\share -> \server\share
    result = unquote_header_value(value, is_filename=False)
    
    assert result == '\\server\\share'