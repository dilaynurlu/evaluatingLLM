from requests.utils import unquote_header_value

def test_unquote_header_value_normal_filename():
    """
    Test that non-UNC filenames (e.g., C:\...) are unescaped even if is_filename is True.
    """
    # Input: "C:\\path\to\file" enclosed in quotes.
    # In a quoted string, \\ represents a literal \.
    # So "C:\\path" -> C:\path
    value = r'"C:\\path\to\file"'
    expected = r'C:\path\to\file'
    
    assert unquote_header_value(value, is_filename=True) == expected