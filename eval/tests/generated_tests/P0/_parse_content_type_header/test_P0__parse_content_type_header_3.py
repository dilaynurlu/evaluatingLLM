import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_boolean_param():
    # Validates handling of parameters without values (flags), which should default to True
    header = "text/plain; verbose; secure"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    # Keys are lowercased, values for flag parameters are boolean True
    assert params == {"verbose": True, "secure": True}