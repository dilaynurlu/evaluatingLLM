import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_flag_parameter():
    """
    Test that a parameter without an equals sign is treated as a flag with value True.
    """
    header = "text/plain; secure; version=1.0"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    # 'secure' has no '=', so it becomes a key with value True
    assert params["secure"] is True
    assert params["version"] == "1.0"