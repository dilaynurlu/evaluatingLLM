import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    value = None
    assert unquote_header_value(value) is None
