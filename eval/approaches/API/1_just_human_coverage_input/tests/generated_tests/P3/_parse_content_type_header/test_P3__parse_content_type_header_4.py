import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_malformed_pairs():
    """
    Test parsing malformed parameters including:
    - Keys with empty values (key=)
    - Values missing keys (=value)
    - Multiple equals signs (key=val1=val2)
    - Flags without equals
    """
    header = "text/plain; empty_val=; =missing_key; double=val1=val2; simple_flag"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    
    # Expect empty string for key with empty value
    assert params["empty_val"] == ""
    
    # Expect empty string key for missing key
    assert params[""] == "missing_key"
    
    # Expect split limit of 1, preserving the second equals in the value
    assert params["double"] == "val1=val2"
    
    # Flag should map to True
    assert params["simple_flag"] is True