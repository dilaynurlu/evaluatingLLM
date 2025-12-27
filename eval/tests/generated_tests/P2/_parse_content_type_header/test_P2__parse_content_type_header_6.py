import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_header_case_insensitive_keys():
    """
    Test that parameter keys are converted to lowercase in the result dictionary.
    """
    header = "text/plain; CharSet=UTF-8; VERSION=1.0"
    expected_content_type = "text/plain"
    # Keys should be lowercased, values preserve case (unless processed otherwise)
    expected_params = {"charset": "UTF-8", "version": "1.0"}
    
    result_type, result_params = _parse_content_type_header(header)
    
    assert result_type == expected_content_type
    assert result_params == expected_params