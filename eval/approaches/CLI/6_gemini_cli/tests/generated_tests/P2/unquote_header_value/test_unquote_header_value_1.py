import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_quoted():
    val = '"value"'
    assert unquote_header_value(val) == "value"
