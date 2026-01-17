import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename_preserved():
    """
    Test that when is_filename=True, a value starting with a UNC path pattern (double backslash)
    is stripped of quotes but NOT unescaped. This preserves the UNC path structure.
    """
    # Input: "\\Server\Share"
    # In Python string literal, backslashes must be escaped.
    # We want the string content to be: " \ \ S e r v e r \ S h a r e "
    input_value = '"\\\\Server\\Share"'
    
    # Expected: \\Server\Share (quotes removed, backslashes preserved)
    # The function avoids replacing '\\\\' with '\\' in this specific case.
    expected_value = '\\\\Server\\Share'
    
    result = unquote_header_value(input_value, is_filename=True)
    
    assert result == expected_value