from requests.utils import unquote_header_value

def test_unquote_header_value_multiple_backslashes():
    # Test that multiple sequential backslashes are unescaped correctly.
    # Input: "\\\\" inside quotes -> effectively 4 backslashes in the content.
    # Should replace every \\ with \.
    # Result should be \\ (2 backslashes).
    header_val = r'"\\\\"'
    expected = r'\\'
    assert unquote_header_value(header_val) == expected