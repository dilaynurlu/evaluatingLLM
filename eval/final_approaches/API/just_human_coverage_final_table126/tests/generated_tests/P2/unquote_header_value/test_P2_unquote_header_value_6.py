import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_default_behavior():
    """
    Test that if a UNC path is provided but is_filename is False (default),
    the function incorrectly treats it as escaped backslashes and mangles the leading double slash.
    This validates the documented behavior/bug fix requirement for is_filename=True.
    """
    # UNC path: \\server\share
    # Input wrapped in quotes: "\\server\share"
    # Since is_filename=False, it enters replace logic.
    # The leading \\\\ (double backslash) gets replaced by \\ (single backslash).
    
    unc_val = r'"\\server\share"'
    
    # Expected behavior: The leading double slash becomes a single slash
    # Result: \server\share
    expected = r"\server\share"
    
    assert unquote_header_value(unc_val, is_filename=False) == expected