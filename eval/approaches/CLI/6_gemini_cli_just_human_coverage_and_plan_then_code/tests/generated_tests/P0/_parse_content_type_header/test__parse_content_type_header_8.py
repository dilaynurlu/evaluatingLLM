
import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_empty():
    header = ""
    # tokens = header.split(";") -> [""]
    # content_type = ""
    ct, params = _parse_content_type_header(header)
    assert ct == ""
    assert params == {}
