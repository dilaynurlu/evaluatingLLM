from requests.utils import unquote_header_value

def test_unquote_header_value_unc_like_non_filename():
    # Scenario: When is_filename=False (default), even if content looks like a UNC path,
    # it should be unescaped (backslashes reduced).
    # Input corresponds to: "\\server\share"
    # Inner content: \\server\share
    input_val = r'"\\server\share"'
    # Expected: \server\share (first \\ becomes \)
    expected = r'\server\share'
    assert unquote_header_value(input_val, is_filename=False) == expected