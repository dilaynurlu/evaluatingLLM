import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_empty_quotes():
    val = '""'
    assert unquote_header_value(val) == ""
