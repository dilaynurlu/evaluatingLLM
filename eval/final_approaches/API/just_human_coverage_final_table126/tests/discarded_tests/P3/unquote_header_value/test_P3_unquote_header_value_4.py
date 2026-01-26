from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """
    Test that escaped backslashes are unescaped, while non-special escapes
    and large inputs are handled robustly.
    """
    # 1. Standard double backslash: "foo\\bar" -> foo\bar
    input_val = r'"foo\\bar"'
    expected = r'foo\bar'
    assert unquote_header_value(input_val) == expected

    # 2. Non-special escaped characters (e.g., \z) should typically be preserved 
    #    or minimally processed. The implementation uses simple replacement, 
    #    so \z should remain \z.
    # Input: "\z" -> \z
    input_non_special = r'"\z"'
    expected_non_special = r'\z'
    assert unquote_header_value(input_non_special) == expected_non_special

    # 3. Trailing escaped backslash at the end of the content
    # Input: "foo\\" -> Content: foo\\ -> Unescaped: foo\
    input_trailing = r'"foo\\"'
    expected_trailing = r'foo\'
    assert unquote_header_value(input_trailing) == expected_trailing

    # 4. Robustness / DoS check
    # Ensure a large number of backslashes doesn't hang the function.
    # Input: " \\ ... \\ " (1000 pairs) -> 1000 singles
    safe_len = 2000
    large_input = '"' + (r'\\' * safe_len) + '"'
    expected_large = '\\' * safe_len
    assert unquote_header_value(large_input) == expected_large