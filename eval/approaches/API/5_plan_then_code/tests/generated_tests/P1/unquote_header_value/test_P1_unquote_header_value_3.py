import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unc_filename():
    """
    Test unquoting of a UNC path filename (starts with \\).
    When is_filename is True, the leading double backslash should be preserved
    and no unescaping should happen to avoid breaking the path.
    """
    # Input represents: "\\server\share"
    # Stripped: \\server\share
    # Since it starts with \\ and is_filename=True, it returns stripped value directly.
    header_value = r'"\\server\share"'
    result = unquote_header_value(header_value, is_filename=True)
    assert result == r'\\server\share'