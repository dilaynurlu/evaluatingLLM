from requests.utils import unquote_header_value

def test_unquote_header_value_filename_ie_path():
    """
    Test that a normal Windows path (e.g. from IE upload) is correctly unescaped
    when is_filename=True, provided it doesn't start with a UNC prefix.
    """
    # IE uploads files with "C:\\foo\\bar.txt" as filename.
    # The backslashes are escaped in the header value.
    value = r'"C:\\foo\\bar.txt"'
    
    # Should strip quotes and unescape \\ to \
    expected = r'C:\foo\bar.txt'
    assert unquote_header_value(value, is_filename=True) == expected