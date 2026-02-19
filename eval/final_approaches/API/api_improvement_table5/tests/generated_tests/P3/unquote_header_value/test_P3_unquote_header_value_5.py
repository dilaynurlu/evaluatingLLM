from requests.utils import unquote_header_value

def test_unquote_header_value_filename_normal_unescaped():
    """Test that non-UNC filenames are unescaped normally when is_filename is True."""
    # Standard: "C:\\path\\file" -> "C:\path\file"
    header_value = r'"C:\\path\\file"'
    result = unquote_header_value(header_value, is_filename=True)
    assert result == r"C:\path\file"

    # Mixed: "foo\"bar.txt" -> foo"bar.txt
    # Verifies that standard escape sequences (like \") are handled even if is_filename is True,
    # provided it's not a UNC path.
    header_value_quotes = r'"foo\"bar.txt"'
    result_quotes = unquote_header_value(header_value_quotes, is_filename=True)
    assert result_quotes == 'foo"bar.txt'