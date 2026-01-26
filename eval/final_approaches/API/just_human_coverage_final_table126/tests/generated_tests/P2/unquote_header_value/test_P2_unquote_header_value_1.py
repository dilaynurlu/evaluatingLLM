import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_passthrough():
    """
    Test that values which are not properly quoted (start and end with ")
    are returned exactly as provided, including None and empty strings.
    """
    assert unquote_header_value(None) is None
    assert unquote_header_value("") == ""
    assert unquote_header_value("text") == "text"
    assert unquote_header_value('"text') == '"text'
    assert unquote_header_value('text"') == 'text"'
    assert unquote_header_value("'text'") == "'text'"  # Single quotes are not handled