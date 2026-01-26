import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_complex_stripping():
    """
    Test complex stripping scenarios:
    - Whitespace around delimiters.
    - Quotes around keys.
    - Semicolons inside quotes (Tests naive splitting behavior).
    """
    # This test characterizes the naive splitting on ';' mentioned in the critique/analysis.
    # 'key="val;ue"' splits into 'key="val' and 'ue"'.
    header = " application/json ;  \"version\" = 2 ; test=\"val;ue\" "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    assert params.get("version") == "2"
    
    # Asserting the naive split behavior as per static analysis of the function
    # loop over split(';').
    # Segment 1: test="val -> key: test, value: val (stripped of quote)
    # Segment 2: ue" -> flag: ue (stripped of quote)
    assert params.get("test") == "val" 
    assert params.get("ue") is True