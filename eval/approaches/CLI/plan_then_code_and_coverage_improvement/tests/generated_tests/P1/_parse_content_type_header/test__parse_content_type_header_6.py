import pytest
from requests.utils import _parse_content_type_header

def test__parse_content_type_header_malformed_param():
    """Test parsing a parameter without an equals sign."""
    header = "text/html; invalidparam"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/html"
    # The code treats 'invalidparam' as key and value as True (boolean) if no '=' found?
    # Let's check code: 
    # if index_of_equals != -1: ... 
    # else: key, value = param, True
    assert params == {"invalidparam": True}
