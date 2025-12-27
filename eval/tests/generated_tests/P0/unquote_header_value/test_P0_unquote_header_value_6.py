from requests.utils import unquote_header_value

def test_unquote_header_value_not_filename_unc_like():
    """
    Test that when is_filename=False (default), even if the value looks like a UNC path,
    standard unescaping rules apply (double backslashes become single backslashes).
    """
    # Input represents: "\\server\share" wrapped in quotes
    header = r'"\\server\share"'
    
    # Expected: Standard unescaping applies. 
    # \\ becomes \
    expected = r'\server\share'
    
    result = unquote_header_value(header, is_filename=False)
    assert result == expected