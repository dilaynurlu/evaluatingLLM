import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """
    Test unquoting None.
    Should return None.
    """
    assert unquote_header_value(None) is None