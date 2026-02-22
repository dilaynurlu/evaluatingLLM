from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_false_positive():
    """Test UNC path unquoting when is_filename is False."""
    input_val = r'"\\server\share\file.txt"'
    # is_filename=False (default).
    # It *will* perform replacement.
    # \\ becomes \
    # The first \\ (start of string) becomes \
    expected = r'\server\share\file.txt'
    
    assert unquote_header_value(input_val, is_filename=False) == expected

