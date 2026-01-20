import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mismatched_quotes():
    value = '"foo'
    assert unquote_header_value(value) == '"foo'
