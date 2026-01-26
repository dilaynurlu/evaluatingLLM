import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_case_insensitive_keys():
    """
    Test that parameter keys are case-insensitive and stored as lowercase.
    Refined to include control characters in keys/values to ensure robustness.
    """
    header = "text/plain; CHARset=UTF-8; Format=Flowed"
    content_type, params = _parse_content_type_header(header)
    
    assert content_type == "text/plain"
    assert params == {'charset': 'UTF-8', 'format': 'Flowed'}

    # Refinement: Control characters (Security: Log Forging / Splitting potential)
    # Python strings can contain control chars. The parser should store them as is 
    # or handle them without crashing.
    header_ctrl = "text/plain; para\nm=val\rue"
    ct, p_ctrl = _parse_content_type_header(header_ctrl)
    assert ct == "text/plain"
    # Ensure keys are lowercased even with control chars if they pass through
    assert 'para\nm' in p_ctrl or 'para\nm'.lower() in p_ctrl
    assert p_ctrl.get('para\nm') == 'val\rue'