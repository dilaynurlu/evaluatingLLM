from requests.utils import unquote_header_value

def test_unquote_header_value_5():
    # Test filename UNC path behavior
    # We want a string that looks like: "\\server\share\file" inside quotes.
    val = r'"\\server\share\file"'
    
    # Expected result is the unquoted string: \\server\share\file
    expected = r"\\server\share\file"
    
    assert unquote_header_value(val, is_filename=True) == expected