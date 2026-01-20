
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_quotes_with_spaces():
    value = '"foo bar"'
    assert unquote_header_value(value) == "foo bar"
