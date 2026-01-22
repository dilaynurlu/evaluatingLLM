import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_quoted_keys():
    """
    Test that quotes around parameter keys are stripped.
    Refined to test garbage/fuzzing inputs to ensure no crashes.
    """
    header = "application/json; 'version'=1"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "application/json"
    assert params == {'version': '1'}

    # Refinement: Garbage input
    # Strings that look like binary or random delimiters
    header_garbage = "application/???; @#$%=^&*();"
    ct, p_garbage = _parse_content_type_header(header_garbage)
    assert ct == "application/???"
    # Just ensure it parsed something without crashing
    assert isinstance(p_garbage, dict)
    assert '@#$%' in p_garbage or '"@#$%"' in p_garbage or p_garbage.get('@#$%') == '^&*()'