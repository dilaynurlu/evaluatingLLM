import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_flag_param():
    # Scenario: Parameter without value (flag)
    header = "text/html; flag; charset=utf-8"
    ctype, params = _parse_content_type_header(header)
    assert ctype == "text/html"
    # Implicit value is True (boolean), wait, code says: key, value = param, True
    # But then string slicing doesn't happen.
    assert params["flag"] is True
    assert params["charset"] == "utf-8"
