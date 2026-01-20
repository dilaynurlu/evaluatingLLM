import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_single_quote_mark():
    val = '"'
    # Matches [0] == [-1] == '"' because length 1
    assert unquote_header_value(val) == ""
