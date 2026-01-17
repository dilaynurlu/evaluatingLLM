from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path():
    """
    Test that UNC paths (starting with \\) are preserved when is_filename is True.
    
    Addresses critique:
    - Path Traversal/Security: Ensures \\server is not converted to \server
      which could alter the meaning of the path.
    """
    # Input: "\\server\share" enclosed in quotes
    # The function should strip quotes. Normal unquoting converts \\ to \.
    # But is_filename=True detects the leading UNC double-slash and preserves it.
    value = r'"\\server\share"'
    expected = r'\\server\share'
    
    assert unquote_header_value(value, is_filename=True) == expected