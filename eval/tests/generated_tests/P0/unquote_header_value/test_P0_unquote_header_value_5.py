from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_path():
    """
    Test that when is_filename=True and the unquoted value starts with a UNC path (\\\\),
    escaped backslashes are NOT replaced to preserve the UNC path structure.
    This corresponds to the fix for IE behavior mentioned in the function comments.
    """
    # Input represents: "\\server\share" wrapped in quotes
    # The actual string content inside quotes is: \\server\share
    header = r'"\\server\share"'
    
    # Expected: The quotes are stripped, but the double backslash remains double 
    # because is_filename=True detects the UNC prefix.
    expected = r'\\server\share'
    
    result = unquote_header_value(header, is_filename=True)
    assert result == expected