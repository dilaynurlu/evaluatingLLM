
import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_simple():
    header = "application/json"
    ct, params = _parse_content_type_header(header)
    assert ct == "application/json"
    assert params == {}
