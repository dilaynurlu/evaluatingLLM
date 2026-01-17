from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_escaping():
    # Test that when is_filename=True, normal paths (NOT starting with \\)
    # ARE unescaped normally.
    # Input represents: "C:\\foo"
    value = r'"C:\\foo"'
    
    # Expected: quotes stripped, backslashes unescaped
    expected = r'C:\foo'
    
    assert unquote_header_value(value, is_filename=True) == expected