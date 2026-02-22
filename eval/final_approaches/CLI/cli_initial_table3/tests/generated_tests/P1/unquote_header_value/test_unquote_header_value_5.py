from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal():
    """Test unquoting normal filenames (not UNC)."""
    input_val = r'"C:\\path\\to\\file.txt"'
    # Not UNC (doesn't start with \), so it should unescape.
    # \\ becomes \
    expected = r'C:\path\to\file.txt'
    
    assert unquote_header_value(input_val, is_filename=True) == expected

