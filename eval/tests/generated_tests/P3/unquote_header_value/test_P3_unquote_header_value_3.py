import pytest
from requests.utils import unquote_header_value

def test_unquote_escaped_characters_and_robustness():
    """
    Test unquoting strings with:
    1. Standard escapes (quotes, backslashes).
    2. Non-standard escapes (orphaned backslashes should be preserved).
    3. Large inputs to verify performance/robustness.
    """
    # Standard escapes: \" -> " and \\ -> \
    header_value = r'"foo\"bar\\baz"'
    expected = r'foo"bar\baz'
    assert unquote_header_value(header_value) == expected

    # Non-standard escape: \z is not a special escape, backslash should remain
    # Input: "foo\z" -> Output: foo\z
    header_value_weird = r'"foo\z"'
    expected_weird = r'foo\z'
    assert unquote_header_value(header_value_weird) == expected_weird

    # Large input check (DoS prevention check)
    # Create a string with many escaped backslashes
    base = r'a\\b\"c'
    large_header = '"' + (base * 5000) + '"'
    # Expected: a\b"c repeated
    large_expected = (r'a\b"c' * 5000)
    assert unquote_header_value(large_header) == large_expected