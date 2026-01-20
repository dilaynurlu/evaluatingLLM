
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_partial_quotes():
    value = '"foo'
    # Does not start AND end with quotes, so no unquoting
    assert unquote_header_value(value) == '"foo'
