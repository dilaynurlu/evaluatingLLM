import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_mixed_quotes():
    # 'val"ue' -> 'val"ue' (no surrounding quotes to strip)
    val = "'val\"ue'"
    assert unquote_header_value(val) == "'val\"ue'"
