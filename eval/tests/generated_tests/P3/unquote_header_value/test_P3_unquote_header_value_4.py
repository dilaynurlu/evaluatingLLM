import pytest
from requests.utils import unquote_header_value

def test_filename_unc_path_preservation_robustness():
    """
    Test that UNC paths (starting with \\) are preserved when is_filename is True.
    Also verifies that directory traversal sequences like '..' are not stripped,
    as this function's job is unquoting, not sanitization.
    """
    # Standard UNC path
    header_value = r'"\\server\share"'
    expected = r'\\server\share'
    assert unquote_header_value(header_value, is_filename=True) == expected

    # UNC path with traversal dots
    # Logic: Should strip outer quotes, see \\ at start, and return the rest as-is.
    header_traversal = r'"\\server\share\..\secret"'
    expected_traversal = r'\\server\share\..\secret'
    assert unquote_header_value(header_traversal, is_filename=True) == expected_traversal