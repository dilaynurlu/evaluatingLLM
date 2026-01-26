import pytest
from requests.utils import _parse_content_type_header

def test_parse_content_type_flag_parameter():
    """
    Test parsing parameters that do not have an equals sign (flags).
    Refined to test consecutive delimiters (empty flags).
    """
    header = "text/plain; verbose; check"
    content_type, params = _parse_content_type_header(header)
    assert content_type == "text/plain"
    assert params == {'verbose': True, 'check': True}

    # Refinement: Consecutive delimiters / Malformed separators
    header_malformed = "text/plain; ; verbose; ; ; check"
    _, params_m = _parse_content_type_header(header_malformed)
    # Empty strings between semicolons should be ignored or handled gracefully
    # If they are treated as empty keys, we verify strict behavior.
    # In many implementations, empty segments result in empty strings.
    # 'verbose' and 'check' should still be present.
    assert params_m.get('verbose') is True
    assert params_m.get('check') is True