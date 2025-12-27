import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_with_quoted_params():
    """
    Test that parameters with quoted values have the quotes stripped correctly.
    This checks both double quotes and ensures multiple parameters are handled.
    """
    header = 'multipart/form-data; boundary="---boundary"; charset="utf-8"'
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "multipart/form-data"
    assert params == {
        "boundary": "---boundary",
        "charset": "utf-8"
    }