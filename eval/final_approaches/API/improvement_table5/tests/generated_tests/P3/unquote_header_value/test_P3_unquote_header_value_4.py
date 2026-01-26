from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc_preserved():
    """Test that UNC paths are preserved (not unescaped) when is_filename is True."""
    # Input represents "\\server\share" inside quotes.
    header_value = r'"\\server\share"'
    result = unquote_header_value(header_value, is_filename=True)
    assert result == r"\\server\share"