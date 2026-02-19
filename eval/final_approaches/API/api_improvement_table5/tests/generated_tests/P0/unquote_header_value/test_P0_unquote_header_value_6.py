from requests.utils import unquote_header_value

def test_unquote_header_value_non_filename_unc_unescape():
    # Test that when is_filename=False (default), even if the value looks like a UNC path,
    # the function unescapes the double backslashes.
    # Input represented as: "\\escaped\\start"
    header_val = r'"\\escaped\\start"'
    # Should become: \escaped\start
    expected = r'\escaped\start'
    assert unquote_header_value(header_val, is_filename=False) == expected