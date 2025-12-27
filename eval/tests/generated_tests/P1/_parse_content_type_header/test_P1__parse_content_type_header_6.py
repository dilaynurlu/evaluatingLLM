import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitive_keys():
    """
    Test that parameter keys are converted to lowercase, but values preserve case.
    """
    header = "application/json; CharSet=UTF-8; VERSION=1.2"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/json"
    # Keys become lowercase
    assert "charset" in params
    assert "version" in params
    # Values preserve case
    assert params["charset"] == "UTF-8"
    assert params["version"] == "1.2"