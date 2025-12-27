import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_aggressive_strip_behavior():
    """
    Test the specific stripping behavior of the function.
    The function strips single quotes, double quotes, and spaces from both ends of the value.
    This test verifies that mixed quotes and spaces at boundaries are removed.
    """
    # The function uses items_to_strip = "\"' "
    # param 1: ' "val" ' -> strips ', ", space -> result: val
    # param 2: "foo bar" -> strips " -> result: foo bar (internal space preserved)
    header = "foo/bar; p1=' \"val\" '; p2=\"foo bar\""
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "foo/bar"
    assert params["p1"] == "val"
    assert params["p2"] == "foo bar"