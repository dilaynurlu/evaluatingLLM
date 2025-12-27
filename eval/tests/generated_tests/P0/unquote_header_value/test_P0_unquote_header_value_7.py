from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_path():
    """
    Test that when is_filename=True but the value is a normal path (not starting with UNC \\\\),
    standard unescaping rules apply.
    """
    # Input represents: "C:\\path\\file.txt"
    header = r'"C:\\path\\file.txt"'
    
    # Expected: Quotes stripped, double backslashes unescaped to single.
    expected = r'C:\path\file.txt'
    
    result = unquote_header_value(header, is_filename=True)
    assert result == expected