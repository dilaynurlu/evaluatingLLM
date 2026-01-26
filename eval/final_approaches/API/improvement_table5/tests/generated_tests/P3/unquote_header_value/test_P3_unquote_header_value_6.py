from requests.utils import unquote_header_value

def test_unquote_header_value_non_filename_unc_mangled():
    """Test that UNC-like paths are unescaped (mangled) when is_filename is False."""
    header_value = r'"\\server\share"'
    result = unquote_header_value(header_value, is_filename=False)
    # Expect "\server\share" (first double backslash becomes single)
    assert result == r"\server\share"