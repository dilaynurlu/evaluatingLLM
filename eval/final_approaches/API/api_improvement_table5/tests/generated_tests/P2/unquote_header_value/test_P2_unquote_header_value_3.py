import pytest
from requests.utils import unquote_header_value

def test_unquote_handles_escaped_quotes():
    """
    Test that escaped double quotes (\") inside the string are converted 
    to literal double quotes (") when unquoting.
    """
    # Input represents: "text with \" quote"
    input_value = r'"text with \" quote"'
    result = unquote_header_value(input_value)
    assert result == 'text with " quote'