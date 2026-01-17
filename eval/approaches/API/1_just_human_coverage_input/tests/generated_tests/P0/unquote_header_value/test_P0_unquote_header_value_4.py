from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preservation():
    # Test that when is_filename=True, UNC-style paths (starting with \\) 
    # are NOT unescaped, to preserve the path structure.
    # Input represents: "\\server\share"
    value = r'"\\server\share"'
    
    # Expected: quotes stripped, but backslashes preserved
    expected = r'\\server\share'
    
    assert unquote_header_value(value, is_filename=True) == expected