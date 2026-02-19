import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_flag_parameters():
    """
    Test parsing parameters that do not have an equals sign.
    Refined to include mixed case and irregular spacing.
    """
    header = "text/plain;  SeCuRe ;   VERBOSE "
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    # Assuming flags result in True as per initial test expectations
    # Keys should be lowercased
    assert params == {"secure": True, "verbose": True}