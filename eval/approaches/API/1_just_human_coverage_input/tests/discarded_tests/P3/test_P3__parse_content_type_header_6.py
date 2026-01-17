import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_invalid_types():
    """
    Test robustness when passing non-string inputs (e.g., None, Integers).
    Since the function relies on string methods like .split(), passing invalid types
    should raise a standard exception (AttributeError or TypeError) rather than failing silently.
    """
    # Test None
    with pytest.raises((AttributeError, TypeError)):
        _parse_content_type_header(None)

    # Test Integer
    with pytest.raises((AttributeError, TypeError)):
        _parse_content_type_header(12345)