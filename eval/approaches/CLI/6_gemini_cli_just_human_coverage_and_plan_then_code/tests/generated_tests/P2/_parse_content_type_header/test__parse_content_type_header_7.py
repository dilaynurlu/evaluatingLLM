import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitive_params():
    # Scenario: Params keys are case insensitive
    header = "text/html; CHARSET=utf-8"
    ctype, params = _parse_content_type_header(header)
    assert params["charset"] == "utf-8"
