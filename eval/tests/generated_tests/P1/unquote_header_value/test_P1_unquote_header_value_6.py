import pytest
from requests.utils import unquote_header_value

def test_unquote_none_input():
    """
    Test that passing None to the function returns None.
    """
    result = unquote_header_value(None)
    assert result is None