import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none_input():
    """
    Test that passing None returns None.
    """
    assert unquote_header_value(None) is None