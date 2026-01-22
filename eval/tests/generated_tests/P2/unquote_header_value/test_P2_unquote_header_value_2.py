import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_simple_unquote():
    """
    Test that strings surrounded by double quotes are stripped of the quotes.
    """
    assert unquote_header_value('"simple"') == "simple"
    assert unquote_header_value('"with spaces"') == "with spaces"
    assert unquote_header_value('""') == ""  # Empty quoted string