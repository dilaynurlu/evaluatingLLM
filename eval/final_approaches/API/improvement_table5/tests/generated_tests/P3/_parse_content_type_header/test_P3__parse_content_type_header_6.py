import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitive_keys():
    """
    Test that parameter keys are normalized to lowercase, 
    but values preserve their case.
    """
    header = "image/png; BoundAry=---ABC; Format=Wide"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "image/png"
    assert params == {"boundary": "---ABC", "format": "Wide"}