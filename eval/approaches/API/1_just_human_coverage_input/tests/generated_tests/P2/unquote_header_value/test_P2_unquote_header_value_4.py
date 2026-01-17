import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path_as_non_filename_unescapes():
    """
    Test that when is_filename is False (default), a value looking like a UNC path
    IS unescaped (double backslashes become single).
    """
    # Input represents quoted string "\\server\share"
    # Content: \\server\share
    # is_filename=False -> Replacements occur.
    # \\ (at start) matches \\\\ pattern in replace (which matches 2 backslashes)
    # Replaced by \
    # Result: \server\share
    value = r'"\\server\share"'
    expected = r"\server\share"
    
    assert unquote_header_value(value, is_filename=False) == expected