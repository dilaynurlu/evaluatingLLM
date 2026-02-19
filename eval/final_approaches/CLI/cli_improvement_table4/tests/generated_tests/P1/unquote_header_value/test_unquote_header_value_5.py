import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_filename_unc():
    """Test unquoting UNC filename (should not unescape backslashes)."""
    # UNC path: \\server\share
    # Quoted: "\\\\server\\share"
    value = '"\\\\server\\share"'
    # Inner: \\server\share (in python string literal terms)
    # is_filename=True
    # Should NOT unescape
    assert unquote_header_value(value, is_filename=True) == '\\\\server\\share'

