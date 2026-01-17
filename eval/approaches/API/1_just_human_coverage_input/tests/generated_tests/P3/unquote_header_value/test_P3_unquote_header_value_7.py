from requests.utils import unquote_header_value

def test_unquote_header_value_empty_and_large_input():
    """
    Test that an empty pair of quotes results in an empty string, and verify handling
    of large inputs to check for performance stability.
    """
    # Empty quoted string
    assert unquote_header_value('""') == ""
    
    # Large input with many escapes
    # Construct a large string: "a\\a\\...a\\"
    # 5000 repetitions of 'a' followed by an escaped backslash
    inner_content = r'a\\' * 5000
    large_value = f'"{inner_content}"'
    
    result = unquote_header_value(large_value)
    
    # Logic: Each '\\' becomes '\'
    expected_inner = "a\\" * 5000
    assert result == expected_inner