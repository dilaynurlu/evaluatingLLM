import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_regular():
    """
    Test unquoting of a UNC-like string when is_filename is False.
    Standard unescaping should occur, turning \\ into \.
    """
    # Input represents: "\\server\share"
    # Stripped: \\server\share
    # Since is_filename=False, replace('\\\\', '\\') is called.
    # \\ becomes \
    header_value = r'"\\server\share"'
    result = unquote_header_value(header_value, is_filename=False)
    assert result == r'\server\share'