import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_duplicate_params():
    # Scenario: Duplicate parameters
    header = "text/html; charset=utf-8; charset=iso-8859-1"
    ctype, params = _parse_content_type_header(header)
    # Usually last one wins in dict overwrite
    assert params["charset"] == "iso-8859-1"
