from requests.utils import unquote_header_value

def test_unquote_header_value_non_filename_unc_unescaping():
    # Test that when is_filename=False (default), UNC-like strings
    # are treated as standard content and unescaped.
    # Input represents: "\\server\share"
    value = r'"\\server\share"'
    
    # Expected: quotes stripped, double backslashes replaced by single
    expected = r'\server\share'
    
    assert unquote_header_value(value, is_filename=False) == expected