import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_no_subtype():
    # Scenario: "text" instead of "text/html"
    header = "text; charset=utf-8"
    ctype, params = _parse_content_type_header(header)
    assert ctype == "text"
    assert params["charset"] == "utf-8"
