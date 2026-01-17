from requests.utils import unquote_header_value

def test_unquote_header_value_filename_security():
    """
    Test that is_filename=True handles security-critical characters (Null bytes, CRLF)
    without crashing, preserving them in the output string for the caller to validate.
    """
    # Null byte injection check
    # We expect the function to return the unquoted string containing the null byte,
    # rather than crashing or truncating at the null byte.
    value_null = '"file\x00name.txt"'
    result_null = unquote_header_value(value_null, is_filename=True)
    assert result_null == "file\x00name.txt"

    # CRLF check
    value_crlf = '"file\r\nname.txt"'
    result_crlf = unquote_header_value(value_crlf, is_filename=True)
    assert result_crlf == "file\r\nname.txt"