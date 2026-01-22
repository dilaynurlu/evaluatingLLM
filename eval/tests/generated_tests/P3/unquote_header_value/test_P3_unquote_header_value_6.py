from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_unescaped():
    """
    Test that a filename NOT starting with a UNC path is still unescaped normally.
    This handles cases like "C:\\path" becoming C:\path.
    """
    # Input represents: "C:\\path\\file.txt"
    input_val = r'"C:\\path\\file.txt"'
    
    # Expected: C:\path\file.txt
    expected = r'C:\path\file.txt'
    
    assert unquote_header_value(input_val, is_filename=True) == expected
    
    # Test with Mixed usage (quotes in filename)
    # Input: "file\"name.txt" -> file"name.txt
    input_mixed = r'"file\"name.txt"'
    expected_mixed = 'file"name.txt'
    assert unquote_header_value(input_mixed, is_filename=True) == expected_mixed