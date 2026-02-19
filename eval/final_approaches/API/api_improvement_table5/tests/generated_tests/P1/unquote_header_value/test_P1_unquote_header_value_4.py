from requests.utils import unquote_header_value

def test_unquote_unc_filename_preserves_backslashes():
    """
    Test that if is_filename is True and the value starts with a UNC path (double backslash),
    unquoting does NOT normalize the backslashes.
    """
    # Input represents: "\\server\share"
    # Stripped: \\server\share
    # Since it starts with \\ and is_filename=True, the replacement of \\ to \ is skipped.
    input_val = r'"\\server\share"'
    assert unquote_header_value(input_val, is_filename=True) == r'\\server\share'