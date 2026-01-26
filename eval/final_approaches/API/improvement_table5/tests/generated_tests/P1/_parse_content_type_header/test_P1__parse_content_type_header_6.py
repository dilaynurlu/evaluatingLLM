import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_case_sensitivity():
    """Test that parameter keys are lowercased but values are case-preserved."""
    header = "Text/Html; CharSet=UTF-8; Boundary=ABC"
    content_type, params = _parse_content_type_header(header)
    
    # Note: The content_type itself preserves case in the return value (it's just stripped)
    assert content_type == "Text/Html"
    # Keys should be lowercased, values should retain original case
    assert params == {"charset": "UTF-8", "boundary": "ABC"}