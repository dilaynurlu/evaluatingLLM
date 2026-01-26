from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preservation():
    # Test that when is_filename=True and the value looks like a UNC path (starts with \\),
    # the function strips quotes but does NOT unescape the backslashes.
    # Input represented as: "\\server\share\file.txt"
    header_val = r'"\\server\share\file.txt"'
    expected = r'\\server\share\file.txt'
    assert unquote_header_value(header_val, is_filename=True) == expected