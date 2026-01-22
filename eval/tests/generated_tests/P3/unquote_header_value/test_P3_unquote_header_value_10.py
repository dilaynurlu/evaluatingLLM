from requests.utils import unquote_header_value

def test_unquote_header_value_unc_path_mangled_if_not_filename():
    """
    Test that if is_filename is False (default), a UNC-like path 
    is unescaped (mangled), converting leading \\ to \.
    """
    # Input represents: "\\server\share"
    input_val = r'"\\server\share"'
    
    # Since is_filename=False, the special check is skipped, 
    # and replace('\\\\', '\\') is executed.
    # \\ becomes \
    expected = r'\server\share'
    
    assert unquote_header_value(input_val, is_filename=False) == expected