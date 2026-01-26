import pytest
from requests.utils import unquote_header_value

def test_unquote_handles_escaped_backslashes():
    """
    Test that escaped backslashes (\\) inside the string are converted
    to literal backslashes (\) when unquoting.
    """
    # Input represents: "path \\ to \\ file"
    input_value = r'"path \\ to \\ file"'
    result = unquote_header_value(input_value)
    # Expected: path \ to \ file
    assert result == r"path \ to \ file"