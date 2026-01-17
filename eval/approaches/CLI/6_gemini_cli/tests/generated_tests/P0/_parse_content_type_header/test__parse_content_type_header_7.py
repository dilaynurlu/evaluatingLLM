
import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_param_no_value():
    header = "text/html; valid"
    ct, params = _parse_content_type_header(header)
    assert ct == "text/html"
    # The implementation treats params without = as keys with True value?
    # Let's check implementation:
    # key, value = param, True
    # if index_of_equals != -1: ...
    # So yes.
    assert params == {"valid": True}
