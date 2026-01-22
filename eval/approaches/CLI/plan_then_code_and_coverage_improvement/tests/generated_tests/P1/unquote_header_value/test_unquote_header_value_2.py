import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unquoted():
    """Test string that is not quoted remains unchanged."""
    value = "foo"
    assert unquote_header_value(value) == "foo"
