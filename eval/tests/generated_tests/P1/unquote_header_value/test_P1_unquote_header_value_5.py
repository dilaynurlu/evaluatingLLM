from requests.utils import unquote_header_value

def test_unquote_header_value_ie_full_path_filename():
    """
    Test the specific workaround for Internet Explorer uploading files with full paths.
    If the path contains escaped backslashes but does not start with a UNC pattern (e.g. C:\\),
    it should be unescaped properly.
    """
    # Input represents: "C:\\path\\file.txt"
    value = '"C:\\\\path\\\\file.txt"'
    
    # Starts with "C:", not "\\", so unescaping proceeds even if is_filename=True.
    # C:\\path\\file.txt -> C:\path\file.txt
    result = unquote_header_value(value, is_filename=True)
    
    assert result == 'C:\\path\\file.txt'