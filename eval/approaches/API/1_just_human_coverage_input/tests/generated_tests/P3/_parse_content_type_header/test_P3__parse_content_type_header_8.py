import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_mixed_casing():
    """
    Test that parameter keys are normalized to lowercase to handle mixed-case inputs,
    while parameter values and the MIME type preserve their original case.
    """
    header = "TEXT/HTML; CharSet=UTF-8; Boundary=---123"
    content_type, params = _parse_content_type_header(header)
    
    # Content type case is preserved
    assert content_type == "TEXT/HTML"
    
    # Parameter keys are lowercased
    assert "charset" in params
    assert "boundary" in params
    
    # Parameter values preserve case
    assert params["charset"] == "UTF-8"
    assert params["boundary"] == "---123"