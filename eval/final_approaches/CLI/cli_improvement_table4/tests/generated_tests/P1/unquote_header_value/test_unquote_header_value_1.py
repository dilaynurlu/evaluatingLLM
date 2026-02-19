import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_quoted():
    """Test unquoting a simple quoted string."""
    value = '"foo"'
    assert unquote_header_value(value) == "foo"
