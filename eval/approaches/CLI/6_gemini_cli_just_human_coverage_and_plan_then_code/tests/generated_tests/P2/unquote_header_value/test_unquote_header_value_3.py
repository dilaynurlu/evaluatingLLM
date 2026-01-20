import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped():
    # "val\"ue" -> val"ue
    val = r'"val\"ue"'
    assert unquote_header_value(val) == 'val"ue'
