from requests.utils import unquote_header_value

def test_unquote_header_value_complex_escaping():
    """
    Test unquoting of strings with complex escaping, including trailing escaped backslashes.
    """
    # Case 1: Standard escape sequences
    # Input: "a\\b\"c" -> represents content: a\b"c
    value_orig = r'"a\\b\"c"'
    assert unquote_header_value(value_orig) == r'a\b"c'

    # Case 2: Trailing escaped backslash
    # Input represents: "end\\" (inside quotes is: end\\)
    # The unquoter should convert the double backslash to a single backslash.
    value_trailing = r'"end\\"'
    result_trailing = unquote_header_value(value_trailing)
    # Expected result: end\
    assert result_trailing == "end\\"