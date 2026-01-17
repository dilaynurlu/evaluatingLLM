import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_none():
    """
    Test that passing None returns None.
    Also verifies that the function does not fail on non-string input validation if applicable,
    though None is the primary non-string case handled by requests utils.
    """
    assert unquote_header_value(None) is None