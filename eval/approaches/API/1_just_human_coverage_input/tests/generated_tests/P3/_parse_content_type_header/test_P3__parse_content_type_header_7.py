import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_excessive_tokens():
    """
    Test parsing a header string containing an excessive number of delimiters (semicolons).
    This ensures that the token iteration logic does not hang or crash (Resource Exhaustion/DoS check).
    """
    # Generate a header with 5000 empty tokens
    header = "application/x-test" + ";" * 5000
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "application/x-test"
    # All tokens are empty, so params should remain empty
    assert params == {}