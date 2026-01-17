
import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mixed_quotes():
    value = "'foo'"
    # Only double quotes are handled
    assert unquote_header_value(value) == "'foo'"
