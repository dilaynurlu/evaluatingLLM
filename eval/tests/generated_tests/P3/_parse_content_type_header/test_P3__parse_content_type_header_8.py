import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_empty_input():
    """
    Test parsing an empty string.
    Refined to test Non-String inputs (None, bytes) for robustness.
    """
    header = ""
    content_type, params = _parse_content_type_header(header)
    assert content_type == ""
    assert params == {}

    # Refinement: Test with None
    # Depending on implementation, this might raise an AttributeError or return empty.
    # We assert it raises an exception rather than returning garbage, 
    # enforcing type expectations.
    with pytest.raises(AttributeError):
        _parse_content_type_header(None)

    # Refinement: Test with bytes (if not supported, should raise)
    with pytest.raises((AttributeError, TypeError)):
        _parse_content_type_header(b"application/json")