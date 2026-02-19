from requests.utils import unquote_header_value

def test_unquote_unc_non_filename_normalizes():
    """
    Test that if is_filename is False (default), even UNC-looking paths are unescaped
    according to standard rules (\\ becomes \).
    """
    # Input represents: "\\server\share"
    # Stripped: \\server\share
    # is_filename=False -> The check (not is_filename) is True -> Enter replacement block.
    # \\server becomes \server
    # \share remains \share (single backslash)
    input_val = r'"\\server\share"'
    assert unquote_header_value(input_val, is_filename=False) == r'\server\share'