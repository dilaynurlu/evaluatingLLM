from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_unescape():
    # Test that when is_filename=True and the value does NOT look like a UNC path (e.g. C:\\),
    # the function strips quotes AND unescapes double backslashes to single backslashes.
    # Input represented as: "C:\\Users\\Name\\file.txt"
    header_val = r'"C:\\Users\\Name\\file.txt"'
    expected = r'C:\Users\Name\file.txt'
    assert unquote_header_value(header_val, is_filename=True) == expected