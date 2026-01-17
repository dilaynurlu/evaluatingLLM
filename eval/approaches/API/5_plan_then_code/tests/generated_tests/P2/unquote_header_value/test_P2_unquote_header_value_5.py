import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path_collapsed_default():
    """
    Test that when is_filename=False (default), a value starting with a UNC path pattern
    is treated as a regular escaped string, meaning double backslashes are collapsed.
    """
    # Input: "\\Server\Share"
    input_value = '"\\\\Server\\Share"'
    
    # Since is_filename is False, replace('\\\\', '\\') is executed.
    # \\Server -> \Server
    expected_value = '\\Server\\Share'
    
    result = unquote_header_value(input_value, is_filename=False)
    
    assert result == expected_value