
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_is_filename():
    value = '"filename.txt"'
    assert unquote_header_value(value, is_filename=True) == "filename.txt"
