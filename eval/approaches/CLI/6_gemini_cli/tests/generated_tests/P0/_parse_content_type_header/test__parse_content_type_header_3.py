
import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_extra_spaces():
    header = " text/html ;  charset = utf-8 "
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    assert params == {"charset": "utf-8"}
