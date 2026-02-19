import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_escaped_backslash():
    """Test unquoting string with escaped backslashes."""
    value = '"foo\\bar"'
    # Inner: foo\bar -> replace \ with \ -> foo\bar
    assert unquote_header_value(value) == 'foo\\bar'

