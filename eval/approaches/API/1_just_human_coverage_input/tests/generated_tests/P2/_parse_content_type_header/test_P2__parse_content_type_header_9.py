import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_complex_mixed_parameters():
    # Combination of quoted values, flags, and multiple parameters
    header = 'multipart/form-data; boundary="boundary"; version=1.0; immutable'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {
        "boundary": "boundary",
        "version": "1.0",
        "immutable": True
    }