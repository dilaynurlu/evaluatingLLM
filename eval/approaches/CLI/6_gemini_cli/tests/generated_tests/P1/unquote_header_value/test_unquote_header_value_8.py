import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_non_filename_unc():
    # Input represents "\\server\share"
    # Inner value: \server\share
    # Not a filename, so it should attempt to unescape backslashes.
    # replace("\\", "\") changes leading \ to \
    value = r'"\\server\share"'
    assert unquote_header_value(value, is_filename=False) == r'\server\share'
