
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_empty():
    value = ""
    assert unquote_header_value(value) == ""
